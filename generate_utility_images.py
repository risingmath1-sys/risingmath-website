from PIL import Image, ImageOps, ImageDraw
import os

# Source Directory (Originals)
IMG_DIR = r"c:\Users\dongw\OneDrive\바탕 화면\홈피만들기\홈피6\images"
# Output Directory
OUT_DIR = IMG_DIR

# Mapping: Source -> Destination
TASKS = [
    ("quick_menu_location.png", "btn_location_hover.png"),
    ("quick_menu_blog.png", "btn_blog_hover.png"),
    ("quick_menu_phone.png", "btn_phone_hover.png")
]

# Colors
BLUE = (0, 68, 204) # #0044cc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def process_image(src_name, dest_name):
    src_path = os.path.join(IMG_DIR, src_name)
    dest_path = os.path.join(OUT_DIR, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Skipping {src_name}: Not found.")
        return

    try:
        img = Image.open(src_path).convert("RGBA")
        
        # 1. Handle Transparency: Composite over White or detect bg
        # But wait, we want to know the *content* shape.
        # If transparent, background is effectively "None".
        # Let's verify average corner brightness to decide if we invert.
        
        # Get flattened data to check "background" color (corners)
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((img.width-1, 0)),
            img.getpixel((0, img.height-1)),
            img.getpixel((img.width-1, img.height-1))
        ]
        
        # Calculate brightness of corners (ignoring alpha for now, assuming composed on white)
        # Or better, just composition on white first.
        bg_check_img = Image.new("RGB", img.size, WHITE)
        bg_check_img.paste(img, mask=img.split()[3]) # Use alpha channel as mask
        
        # Now check corners of flattened image
        corner_brightness = []
        for xy in [(0,0), (img.width-1, 0), (0, img.height-1), (img.width-1, img.height-1)]:
            r, g, b = bg_check_img.getpixel(xy)
            corner_brightness.append((r+g+b)/3)
        
        avg_bg_brightness = sum(corner_brightness) / 4
        print(f"{src_name}: Avg BG Brightness = {avg_bg_brightness}")

        # If BG is darker/colored (e.g. < 240), we assume "Colored BG, White Text".
        # We want "White BG, Blue Text". So we keep the "White Text" shape as the "Blue Content".
        # If BG is Light (e.g. > 240), we assume "White BG, Dark Text".
        # We want "White BG, Blue Text". So we keep the "Dark Text" shape as "Blue Content".

        gray = bg_check_img.convert("L")
        
        if avg_bg_brightness < 200:
            # Colored/Dark BG. Content is likely Lighter.
            # We want Content (Light pixels) to become Blue. Background (Dark pixels) to become White.
            # colorize(black=..., white=...) maps 0->black_arg, 255->white_arg.
            # Here:
            # Dark (Bg) -> White (Target Bg)
            # Light (Content) -> Blue (Target Content)
            
            # So: map 0 (Dark) -> WHITE
            # map 255 (Light) -> BLUE
            res = ImageOps.colorize(gray, black=WHITE, white=BLUE)
            
        else:
            # Light/White BG. Content is Darker.
            # We want Content (Dark) to become Blue. Background (Light) to become White.
            
            # So: map 0 (Dark) -> BLUE
            # map 255 (Light) -> WHITE
            res = ImageOps.colorize(gray, black=BLUE, white=WHITE)

        # 2. Add Black Border (REMOVED per user request)
        # draw = ImageDraw.Draw(res)
        # border_width = 4
        # Draw rectangle stroke. w-1 because 0-indexed.
        # draw.rectangle([(0,0), (res.width-1, res.height-1)], outline=BLACK, width=border_width)
        
        res.save(dest_path)
        print(f"Generated: {dest_path}")

    except Exception as e:
        print(f"Error processing {src_name}: {e}")

if __name__ == "__main__":
    for s, d in TASKS:
        process_image(s, d)
