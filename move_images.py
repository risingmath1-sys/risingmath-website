import shutil
import os

# Source and Destination Paths
# Source: C:\Users\dongw\.gemini\antigravity\brain\bf595a0e-9358-4dc7-b181-97701fac7504\
# Dest: c:\Users\dongw\OneDrive\바탕 화면\홈피만들기\홈피6\images\

SOURCE_DIR = r"C:\Users\dongw\.gemini\antigravity\brain\bf595a0e-9358-4dc7-b181-97701fac7504"
DEST_DIR = r"c:\Users\dongw\OneDrive\바탕 화면\홈피만들기\홈피6\images"

# Map uploaded filenames to target filenames
# 0 -> nsu (Crown)
# 1 -> high (Cap)
# 2 -> director (Suit)
# 3 -> middle (Book)

moves = [
    ("uploaded_image_0_1765788230306.png", "btn_nsu_hover.png"),
    ("uploaded_image_1_1765788230306.png", "btn_high_hover.png"),
    ("uploaded_image_2_1765788230306.png", "btn_director_hover.png"),
    ("uploaded_image_3_1765788230306.png", "btn_middle_hover.png")
]

def main():
    if not os.path.exists(DEST_DIR):
        print(f"Error: Destination directory {DEST_DIR} does not exist.")
        return

    print("Starting file move...")
    for src_name, dest_name in moves:
        src_path = os.path.join(SOURCE_DIR, src_name)
        dest_path = os.path.join(DEST_DIR, dest_name)
        
        if os.path.exists(src_path):
            try:
                shutil.copy2(src_path, dest_path)
                print(f"Success: Copied {src_name} -> {dest_name}")
            except Exception as e:
                print(f"Error copying {src_name}: {e}")
        else:
            print(f"Warning: Source file {src_path} not found.")

if __name__ == "__main__":
    main()
