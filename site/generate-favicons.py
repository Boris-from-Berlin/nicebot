"""Generate two PNG favicons (eyes open + closed) for JS-based animation."""
from PIL import Image, ImageDraw
import base64

GREEN = (111, 216, 121)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PX = 2  # pixel multiplier for 32x32ish
W, H = 19, 18

def px(draw, x, y, color):
    draw.rectangle([x*PX, y*PX, (x+1)*PX-1, (y+1)*PX-1], fill=color)

def rect(draw, x, y, w, h, color):
    for dy in range(h):
        for dx in range(w):
            px(draw, x+dx, y+dy, color)

def draw_base(draw):
    # Head black border
    for x in range(4, 15): px(draw, x, 0, BLACK); px(draw, x, 13, BLACK)
    for y in range(1, 13):
        for x in range(3, 16): px(draw, x, y, BLACK)
    # Head green fill
    for x in range(5, 14): px(draw, x, 1, GREEN); px(draw, x, 12, GREEN)
    for y in range(2, 12):
        for x in range(4, 15): px(draw, x, y, GREEN)
    # Arms
    rect(draw, 1, 8, 2, 4, BLACK); px(draw, 2, 9, GREEN); px(draw, 2, 10, GREEN)
    rect(draw, 16, 8, 2, 4, BLACK); px(draw, 16, 9, GREEN); px(draw, 16, 10, GREEN)
    # Legs
    rect(draw, 6, 14, 4, 2, BLACK); px(draw, 7, 14, GREEN); px(draw, 8, 14, GREEN)
    rect(draw, 10, 14, 4, 2, BLACK); px(draw, 11, 14, GREEN); px(draw, 12, 14, GREEN)
    # Feet
    rect(draw, 5, 15, 5, 2, BLACK); rect(draw, 6, 15, 3, 1, GREEN)
    rect(draw, 10, 15, 5, 2, BLACK); rect(draw, 11, 15, 3, 1, GREEN)

def make(eyes):
    img = Image.new('RGBA', (W*PX, H*PX), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw_base(draw)
    if eyes == 'open':
        for dy in range(4):
            px(draw, 6, 4+dy, WHITE); px(draw, 7, 4+dy, WHITE)
            px(draw, 11, 4+dy, WHITE); px(draw, 12, 4+dy, WHITE)
    else:
        for dx in range(3):
            px(draw, 6+dx, 6, WHITE); px(draw, 10+dx, 6, WHITE)
    return img.resize((32, 32), Image.NEAREST)

# Save PNGs
make('open').save('/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/fav-open.png')
make('closed').save('/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/fav-closed.png')

# Also generate base64 data URIs for inline JS (no extra HTTP requests)
import io
for name, eyes in [('open', 'open'), ('closed', 'closed')]:
    buf = io.BytesIO()
    make(eyes).save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    print(f"const FAV_{name.upper()} = 'data:image/png;base64,{b64}';")

print("\nDone!")
