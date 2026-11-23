"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Canvas 1200x675 (16:9). Judge sees it shrunk to fit 768x480, so every
element is large: the official make.fun ghost mark at 340px tall, two
bold caption lines with a heavy black stroke, and the words make.fun.
Background is a Vice City sunset gradient (hot pink up top, teal below).
Five visual elements only: gradient, ghost, top line, bottom line, name.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TOP_TEXT = "13 YEARS WAITING FOR GTA 6"
BOTTOM_TEXT = "MY AI AGENT GOT PAID IN 13 MINUTES"
NAME_TEXT = "make.fun"

# Sunset gradient stops (top -> bottom)
TOP_COLOR = (255, 46, 136)     # hot pink
MID_COLOR = (255, 138, 76)     # sunset orange
BOTTOM_COLOR = (0, 190, 200)   # teal


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_gradient(w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        color = lerp(TOP_COLOR, MID_COLOR, t * 2) if t < 0.5 else lerp(MID_COLOR, BOTTOM_COLOR, (t - 0.5) * 2)
        for x in range(w):
            px[x, y] = color
    return img


def fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, size)


def centered_text(draw, text, y, font, fill=(255, 255, 255), stroke=6):
    width = draw.textlength(text, font=font)
    draw.text(((W - width) / 2, y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=(0, 0, 0))


def main():
    img = make_gradient(W, H)
    draw = ImageDraw.Draw(img)

    # Ghost mark, large and centered
    mark = Image.open("mark-1024.png").convert("RGBA")
    ghost_h = 360
    ghost_w = round(mark.width * ghost_h / mark.height)
    ghost = mark.resize((ghost_w, ghost_h), Image.LANCZOS)
    img.paste(ghost, ((W - ghost_w) // 2, 138), ghost)
    draw = ImageDraw.Draw(img)

    # Caption lines, kept clear of the edges
    top_font = fit_font(draw, TOP_TEXT, W - 140, 68)
    centered_text(draw, TOP_TEXT, 30, top_font)
    bottom_font = fit_font(draw, BOTTOM_TEXT, W - 140, 68)
    centered_text(draw, BOTTOM_TEXT, H - 105, bottom_font)

    # Site name under the ghost, big enough to read when shrunk
    name_font = ImageFont.truetype(FONT_PATH, 56)
    centered_text(draw, NAME_TEXT, 502, name_font, stroke=6)

    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
