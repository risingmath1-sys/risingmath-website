
import urllib.request
from PIL import Image
import io

def process_logo():
    url = "https://cdn.imweb.me/thumbnail/20250820/767c0197cab4c.png"
    save_path = "c:/Users/dongw/OneDrive/바탕 화면/홈피만들기/상승수학_홈피 - 2/images/logo_transparent.png"
    
    try:
        # Download image
        print(f"Downloading logo from {url}...")
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        
        img = Image.open(io.BytesIO(image_data))
        img = img.convert("RGBA")
        
        datas = img.getdata()
        
        new_data = []
        for item in datas:
            # Change all white pixels to transparent
            # Threshold: > 200 for R, G, B
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        
        # Save new image
        img.save(save_path, "PNG")
        print(f"Successfully saved transparent logo to {save_path}")
        
    except ImportError:
        print("Error: PIL (Pillow) library is not installed.")
    except Exception as e:
        print(f"Error processing logo: {e}")

if __name__ == "__main__":
    process_logo()
