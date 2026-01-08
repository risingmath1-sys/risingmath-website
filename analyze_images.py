from PIL import Image
import os

IMG_DIR = r"c:\Users\dongw\OneDrive\바탕 화면\홈피만들기\홈피6\images"
TARGETS = ["quick_menu_location.png", "quick_menu_blog.png", "quick_menu_phone.png"]

def analyze_image(filename):
    path = os.path.join(IMG_DIR, filename)
    if not os.path.exists(path):
        print(f"{filename}: Not found")
        return

    try:
        img = Image.open(path)
        print(f"--- {filename} ---")
        print(f"Format: {img.format}")
        print(f"Mode: {img.mode}")
        print(f"Size: {img.size}")
        
        # Check corners for transparency or color to guess background
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((img.width-1, 0)),
            img.getpixel((0, img.height-1)),
            img.getpixel((img.width-1, img.height-1))
        ]
        print(f"Corners: {corners}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for t in TARGETS:
        analyze_image(t)
