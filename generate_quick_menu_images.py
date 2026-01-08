import os
from PIL import Image, ImageDraw, ImageFont

# Configuration for Quick Access Buttons
# Based on existing "Big Box" style, likely square-ish or rectangular
# Text: White bg, Blue text (#0044cc)

MENU_ITEMS = [
    {"filename": "btn_director_hover.png", "text": "원장직강"},
    {"filename": "btn_nsu_hover.png", "text": "재수·N수"},
    {"filename": "btn_high_hover.png", "text": "고등부"},
    {"filename": "btn_middle_hover.png", "text": "중등부"},
    {"filename": "btn_location_hover.png", "text": "위치"},
    {"filename": "btn_blog_hover.png", "text": "블로그\n바로가기"}, # Blog has 2 lines in alt text? Let's check alt text "블로그 바로가기"
    {"filename": "btn_phone_hover.png", "text": "상담전화"}
]

BG_COLOR = (255, 255, 255) # White
TEXT_COLOR = (0, 68, 204)   # Blue #0044cc

# Target size roughly based on current images? 
# Current images: menu_director.png etc. 
# Let's make them standard large size, they are responsive in CSS usually.
# Assuming a safe size like 400x300 or similar, but text-only doesn't need huge canvas 
# unless it's creating the *entire* button look. 
# Current HTML has <img src> inside <a>. So the image IS the content.
# I should generate images that have the same aspect ratio or sufficient size.
# Since I can't see the exact aspect ratio without opening the image, I will guess a landscape rectangle.
# Actually, let's make them adaptive to text but with padding.

FONT_SIZE = 40 # Larger for main body buttons
PADDING = (50, 40) 

# Font path
FONT_PATH = "C:/Windows/Fonts/malgunbd.ttf" # Malgun Gothic Bold
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
    if not os.path.exists(FONT_PATH):
        FONT_PATH = "C:/Windows/Fonts/arial.ttf"

OUTPUT_DIR = "images" 
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_image(item):
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()
    
    lines = item["text"].split('\n')
    
    # Calculate dimensions
    max_width = 0
    total_height = 0
    line_spacing = 10
    
    for line in lines:
        try:
            left, top, right, bottom = font.getbbox(line)
            w = right - left
            h = bottom - top
        except AttributeError:
             w, h = font.getsize(line)
        max_width = max(max_width, w)
        total_height += h
    
    if len(lines) > 1:
        total_height += (len(lines) - 1) * line_spacing

    img_width = max_width + PADDING[0] * 2
    img_height = total_height + PADDING[1] * 2

    # Forced Minimum Size for uniformity?
    # Let's stick to text tight fit + padding, CSS `width: 100%` will scale it.
    
    img = Image.new('RGB', (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    current_y = PADDING[1]
    for line in lines:
        try:
             left, top, right, bottom = font.getbbox(line)
             w = right - left
             h = bottom - top
        except:
             w, h = font.getsize(line)
        
        # Center text horizontally
        x = (img_width - w) // 2
        draw.text((x, current_y), line, fill=TEXT_COLOR, font=font)
        current_y += h + line_spacing

    save_path = os.path.join(OUTPUT_DIR, item["filename"])
    img.save(save_path)
    print(f"Generated: {save_path}")

def main():
    print("Starting Quick Access image generation...")
    for item in MENU_ITEMS:
        create_image(item)
    print("All Quick Access images generated.")

if __name__ == "__main__":
    main()
