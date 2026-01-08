import os
from PIL import Image, ImageDraw, ImageFont

# Configuration
MENU_ITEMS = [
    {"filename": "nav_overview_hover.png", "text": "Overview"},
    {"filename": "nav_director_hover.png", "text": "원장직강"},
    {"filename": "nav_nsu_hover.png", "text": "재수•N수"},
    {"filename": "nav_high_hover.png", "text": "고등부"},
    {"filename": "nav_middle_hover.png", "text": "중등부"},
    {"filename": "nav_location_hover.png", "text": "위치및약도"},
    {"filename": "nav_notice_hover.png", "text": "공지사항"}
]

BG_COLOR = (255, 255, 255) # White
TEXT_COLOR = (0, 68, 204)   # Blue #0044cc -> (0, 68, 204)
FONT_SIZE = 18 # Match website font size (approximate for bold)
PADDING = (0, 0) # Minimal padding, let CSS handle spacing

# Font path - Windows default
FONT_PATH = "C:/Windows/Fonts/malgun.ttf" # Malgun Gothic
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/arial.ttf" # Fallback

OUTPUT_DIR = "images" 
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_image(item):
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()
        print(f"Warning: Could not load font {FONT_PATH}, using default.")

    # Calculate text size
    # Using getbbox for newer Pillow, or getsize for older
    try:
        left, top, right, bottom = font.getbbox(item["text"])
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
         text_width, text_height = font.getsize(item["text"])

    # Image size
    img_width = text_width + PADDING[0] * 2
    img_height = text_height + PADDING[1] * 2 + 10 # Extra height for baseline

    img = Image.new('RGB', (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw text centered
    position = (PADDING[0], PADDING[1])
    draw.text(position, item["text"], fill=TEXT_COLOR, font=font)

    # Save
    save_path = os.path.join(OUTPUT_DIR, item["filename"])
    img.save(save_path)
    print(f"Generated: {save_path}")

def main():
    print("Starting image generation...")
    for item in MENU_ITEMS:
        create_image(item)
    print("All images generated.")

if __name__ == "__main__":
    main()
