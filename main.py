"""AI Excited - generates an image that excites an AI judge."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, os

W, H = 1024, 1024

def create():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2

    # Cosmic energy rings
    for r in range(30, 480, 2):
        hue = (r * 3 + 128) % 360
        sat, val = 0.95, 0.6 + 0.4 * math.sin(r * 0.04)
        c = val * sat
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = val - c
        if hue < 60:   rgb = (c, x, 0)
        elif hue < 120: rgb = (x, c, 0)
        elif hue < 180: rgb = (0, c, x)
        elif hue < 240: rgb = (0, x, c)
        elif hue < 300: rgb = (x, 0, c)
        else:           rgb = (c, 0, x)
        clr = tuple(int((v + m) * 255) for v in rgb)
        wave = 1 + 0.12 * math.sin(r * 0.08 + 4 * math.sin(r * 0.015))
        rr = int(r * wave)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=clr, width=2)

    # Stars
    for _ in range(600):
        x = random.gauss(cx, 280)
        y = random.gauss(cy, 280)
        b = int(random.random() * 200 + 55)
        s = random.randint(1, 3)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(b, b, b + 30))

    # Central burst
    for i in range(150):
        a = i * (2 * math.pi / 150)
        ln = 50 + random.random() * 180
        ex = cx + math.cos(a) * ln
        ey = cy + math.sin(a) * ln
        b = int(180 + random.random() * 75)
        d.line([cx, cy, ex, ey], fill=(b, b, 255), width=2)

    # Neon circuits
    for _ in range(25):
        px = random.randint(50, W - 50)
        py = random.randint(50, H - 50)
        pts = [(px, py)]
        for _ in range(4):
            px = max(20, min(W - 20, px + random.randint(-100, 100)))
            py = max(20, min(H - 20, py + random.randint(-100, 100)))
            pts.append((px, py))
        clr = (random.randint(0, 80), random.randint(200, 255), random.randint(200, 255))
        for j in range(len(pts) - 1):
            d.line([pts[j], pts[j + 1]], fill=clr, width=3)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png")
    print("entry.png created")

if __name__ == "__main__":
    try: create()
    except ImportError: print("Pillow required: pip install Pillow")
