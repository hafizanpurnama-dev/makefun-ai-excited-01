"""AI Excited - generates an image that excites an AI judge."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, os

W, H = 1024, 1024

def hsv_to_rgb(h, s, v):
    """h in [0,360], s,v in [0,1]."""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if h < 60:   r, g, b = c, x, 0
    elif h < 120: r, g, b = x, c, 0
    elif h < 180: r, g, b = 0, c, x
    elif h < 240: r, g, b = 0, x, c
    elif h < 300: r, g, b = x, 0, c
    else:        r, g, b = c, 0, x
    return tuple(int((v + m) * 255) for v in (r, g, b))


def create():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    cx, cy = W // 2, H // 2

    # ── Radial glow background ──
    for y in range(H):
        for x in range(W):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy) / (W * 0.7)
            if dist < 1:
                fade = max(0, 1 - dist) ** 2.5
                r = int(20 * fade)
                g = int(8 * fade)
                b = int(40 * fade)
                img.putpixel((x, y), (r, g, b))

    d = ImageDraw.Draw(img)

    # ── Cosmic energy rings ──
    for r in range(30, 480, 2):
        hue = (r * 3 + 128) % 360
        sat, val = 0.95, 0.6 + 0.4 * math.sin(r * 0.04)
        wave = 1 + 0.12 * math.sin(r * 0.08 + 4 * math.sin(r * 0.015))
        rr = int(r * wave)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=hsv_to_rgb(hue, sat, val), width=2)

    # ── Neural network nodes & connections ──
    random.seed(42)
    nodes = []
    for _ in range(80):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.gauss(250, 120)
        dist = max(40, min(490, abs(dist)))
        nx = cx + math.cos(angle) * dist
        ny = cy + math.sin(angle) * dist
        nodes.append((nx, ny, random.uniform(3, 8)))

    for i in range(len(nodes)):
        xi, yi, si = nodes[i]
        for j in range(i + 1, len(nodes)):
            xj, yj, sj = nodes[j]
            dd = math.sqrt((xi - xj)**2 + (yi - yj)**2)
            if dd < 140:
                alpha = max(0, 1 - dd / 140)
                hue = (dd * 0.5 + 200) % 360
                clr = hsv_to_rgb(hue, 0.7, alpha * 0.6)
                d.line([(xi, yi), (xj, yj)], fill=clr, width=1)

    for nx, ny, size in nodes:
        d.ellipse([nx - size*2, ny - size*2, nx + size*2, ny + size*2],
                  fill=(20, 230, 255, 30))
        d.ellipse([nx - size, ny - size, nx + size, ny + size],
                  fill=(80, 240, 255))

    # ── Stars with color variety ──
    for _ in range(600):
        x = random.gauss(cx, 280)
        y = random.gauss(cy, 280)
        hue = random.uniform(0, 360)
        s = random.randint(1, 3)
        clr = hsv_to_rgb(hue, 0.3, random.uniform(0.4, 1.0))
        d.ellipse([x - s, y - s, x + s, y + s], fill=clr)

    # ── Particle trails ──
    for _ in range(40):
        angle = random.uniform(0, 2 * math.pi)
        start_r = random.uniform(50, 200)
        sx = cx + math.cos(angle) * start_r
        sy = cy + math.sin(angle) * start_r
        end_r = start_r + random.uniform(100, 300)
        ex = cx + math.cos(angle) * end_r
        ey = cy + math.sin(angle) * end_r
        steps = 30
        for step in range(steps):
            t = step / steps
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t
            fade = 1 - t
            hue = (angle * 180 / math.pi + t * 120) % 360
            clr = hsv_to_rgb(hue, 0.9, fade * 0.8)
            rad = int(3 * fade)
            d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=clr)

    # ── Central burst ──
    for i in range(200):
        a = i * (2 * math.pi / 200)
        ln = 40 + random.random() * 200
        ex = cx + math.cos(a) * ln
        ey = cy + math.sin(a) * ln
        hue = (a * 180 / math.pi + 240) % 360
        clr = hsv_to_rgb(hue, 0.7, 0.9)
        d.line([cx, cy, ex, ey], fill=clr, width=2)

    # ── Neon circuits ──
    for _ in range(25):
        px = random.randint(50, W - 50)
        py = random.randint(50, H - 50)
        pts = [(px, py)]
        for _ in range(4):
            px = max(20, min(W - 20, px + random.randint(-100, 100)))
            py = max(20, min(H - 20, py + random.randint(-100, 100)))
            pts.append((px, py))
        hue = random.uniform(160, 200)
        clr = hsv_to_rgb(hue, 0.8, 0.9)
        for j in range(len(pts) - 1):
            d.line([pts[j], pts[j + 1]], fill=clr, width=3)

    # ── Final touches ──
    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"))
    print("entry.png created (1024x1024)")


if __name__ == "__main__":
    try:
        create()
    except ImportError:
        print("Pillow required: pip install Pillow")