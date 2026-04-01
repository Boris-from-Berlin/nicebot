"""Generate animated GIF favicon and static PNG for NiceBot pixel mascot."""
from PIL import Image, ImageDraw

BG = (10, 10, 15, 0)  # transparent
GREEN = (111, 216, 121)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PX = 4  # pixel size multiplier
W, H = 19, 18  # grid size

def draw_base(draw):
    """Draw the bot body (head, arms, legs, feet) — shared between frames."""
    def px(x, y, color):
        draw.rectangle([x*PX, y*PX, (x+1)*PX-1, (y+1)*PX-1], fill=color)

    def rect(x, y, w, h, color):
        for dy in range(h):
            for dx in range(w):
                px(x+dx, y+dy, color)

    # Head black border (stepped corners)
    # Top row (narrower)
    rect(4, 0, 11, 1, BLACK)
    # Full rows
    rect(3, 1, 13, 12, BLACK)
    # Bottom row (narrower)
    rect(4, 13, 11, 1, BLACK)

    # Head green fill
    rect(5, 1, 9, 1, GREEN)   # top (narrower, corner step)
    rect(4, 2, 11, 9, GREEN)  # main
    rect(5, 11, 9, 1, GREEN)  # bottom (narrower, corner step) -- wait let me recalc

    # Actually let me match the SVG paths exactly:
    # Black: M4,0 H15 V1 H16 V13 H15 V14 H4 V13 H3 V1 H4
    # This means: y=0: x=4-14 (11w), y=1-12: x=3-15 (13w), y=13: x=4-14 (11w)

    # Clear and redo properly
    # Black outline
    for x in range(4, 15):
        px(x, 0, BLACK)        # top border
        px(x, 13, BLACK)       # bottom border
    for y in range(1, 13):
        px(3, y, BLACK)        # left border
        px(15, y, BLACK)       # right border
    for y in range(1, 13):
        for x in range(4, 15):
            px(x, y, BLACK)    # fill (will be overwritten by green)

    # Green fill: M5,1 H14 V2 H15 V12 H14 V13 H5 V12 H4 V2 H5
    # y=1: x=5-13 (9w), y=2-11: x=4-14 (11w), y=12: x=5-13 (9w)
    for x in range(5, 14):
        px(x, 1, GREEN)       # top row green
        px(x, 12, GREEN)      # bottom row green
    for y in range(2, 12):
        for x in range(4, 15):
            px(x, y, GREEN)

    # Left arm
    rect(1, 7, 2, 5, BLACK)
    px(2, 8, GREEN)
    px(2, 9, GREEN)
    px(2, 10, GREEN)

    # Right arm
    rect(16, 7, 2, 5, BLACK)
    px(16, 8, GREEN)
    px(16, 9, GREEN)
    px(16, 10, GREEN)

    # Left leg
    rect(6, 14, 4, 2, BLACK)
    px(7, 14, GREEN)
    px(8, 14, GREEN)

    # Right leg
    rect(10, 14, 4, 2, BLACK)
    px(11, 14, GREEN)
    px(12, 14, GREEN)

    # Left foot
    rect(5, 15, 5, 2, BLACK)
    px(6, 15, GREEN)
    px(7, 15, GREEN)
    px(8, 15, GREEN)

    # Right foot
    rect(10, 15, 5, 2, BLACK)
    px(11, 15, GREEN)
    px(12, 15, GREEN)
    px(13, 15, GREEN)


def draw_eyes_open(draw):
    """Eyes open: 2px wide, 4px tall vertical white rectangles."""
    def px(x, y, color):
        draw.rectangle([x*PX, y*PX, (x+1)*PX-1, (y+1)*PX-1], fill=color)
    for dy in range(4):
        px(6, 4+dy, WHITE)
        px(7, 4+dy, WHITE)
        px(11, 4+dy, WHITE)
        px(12, 4+dy, WHITE)


def draw_eyes_closed(draw):
    """Eyes closed: 3px wide, 1px tall horizontal white dashes."""
    def px(x, y, color):
        draw.rectangle([x*PX, y*PX, (x+1)*PX-1, (y+1)*PX-1], fill=color)
    for dx in range(3):
        px(6+dx, 6, WHITE)
        px(10+dx, 6, WHITE)


def make_frame(eyes='open'):
    img = Image.new('RGBA', (W*PX, H*PX), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_base(draw)
    if eyes == 'open':
        draw_eyes_open(draw)
    else:
        draw_eyes_closed(draw)
    return img


# Generate frames
frame_open = make_frame('open')
frame_closed = make_frame('closed')

# Animated GIF (blink every ~3.5s)
# Frame durations in ms: open=3500, closed=150, open=100 (quick reopen)
frames = [frame_open, frame_closed, frame_open]
durations = [3500, 150, 100]

# Save animated GIF
frame_open_rgb = frame_open.convert('RGBA')
frames_rgb = [f.convert('RGBA') for f in frames]

# For GIF we need to handle transparency
frame_open_gif = frame_open.copy()
frames_gif = [f.copy() for f in frames]

frame_open_gif.save(
    '/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/nicebot.gif',
    save_all=True,
    append_images=frames_gif[1:],
    duration=durations,
    loop=0,
    transparency=0,
    disposal=2
)

# Save static PNG (for fallback)
frame_open.save('/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/nicebot.png')

# Save 32x32 favicon versions
favicon_open = frame_open.resize((32, 32), Image.NEAREST)
favicon_closed = frame_closed.resize((32, 32), Image.NEAREST)

favicons = [favicon_open, favicon_closed, favicon_open]
favicon_open.save(
    '/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/favicon.gif',
    save_all=True,
    append_images=[favicon_closed, favicon_open],
    duration=durations,
    loop=0,
    transparency=0,
    disposal=2
)

# Also a static ICO
favicon_open.save('/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/favicon.ico')

# Larger version for apple-touch-icon
apple = frame_open.resize((180, 180), Image.NEAREST)
apple.save('/Users/borisdittberner/Claude-Code-Projekte/Nicebot/site/apple-touch-icon.png')

print("Generated:")
print("  site/nicebot.gif (animated, full size)")
print("  site/nicebot.png (static, full size)")
print("  site/favicon.gif (animated, 32x32)")
print("  site/favicon.ico (static, 32x32)")
print("  site/apple-touch-icon.png (180x180)")
