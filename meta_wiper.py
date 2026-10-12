import os
import sys
import shutil
import subprocess
from PIL import Image

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_path(path_input):
    """Cleans drag-and-drop formatting quirks across platforms."""
    path = path_input.strip()
    if (path.startswith('"') and path.endswith('"')) or (path.startswith("'") and path.endswith("'")):
        path = path[1:-1]
    return path

def wipe_image_metadata(file_path, tmp_path):
    """Saves image pixel data into a fresh temporary payload, discarding EXIF."""
    try:
        with Image.open(file_path) as img:
            data_format = img.format
            
            # Create a completely fresh image matrix stripped of internal structures
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(img.getdata())
            
            # Save to temporary path without passing down source configurations
            clean_img.save(tmp_path, format=data_format)
        return True, None
    except Exception as e:
        return False, str(e)

def wipe_video_metadata(file_path, tmp_path):
    """Uses FFmpeg stream mapping to strip out global and local metadata atoms."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "FFmpeg utility is missing on this machine. Essential for video operations."

    try:
        command = [
            "ffmpeg", "-y", "-i", file_path,
            "-map_metadata", "-1",         # Drop all global tags
            "-map_chapters", "-1",         # Drop structural markers
            "-c", "copy",                  # Direct copy stream context (Zero quality loss)
            "-bitexact",                   # Wipe vendor and container generation markers
            tmp_path
        ]
        
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"FFmpeg processing failed: {str(e)}"

def process_file(file_path):
    file_path = clean_path(file_path)
    
    if not os.path.exists(file_path):
        print(f"\n❌ Error: The file path '{file_path}' does not exist.")
        return

    dir_name, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    ext_lower = ext.lower()
    
    # Create a unique temporary file path in the same directory
    tmp_filename = f".tmp_wipe_{base_name}{ext}"
    tmp_path = os.path.join(dir_name, tmp_filename)

    image_exts = ['.jpg', '.jpeg', '.png', '.webp', '.tiff', '.bmp']
    video_exts = ['.mp4', '.mkv', '.mov', '.avi', '.m4v']

    print("\n" + "="*50)
    print(f"🧹 WIPING & OVERWRITING: {file_name}")
    print("="*50)

    # Step 1: Generate the stripped version in a temporary file
    success = False
    error_msg = None
    
    if ext_lower in image_exts:
        print("📸 Target type identified: Image")
        success, error_msg = wipe_image_metadata(file_path, tmp_path)
    elif ext_lower in video_exts:
        print("🎬 Target type identified: Video")
        success, error_msg = wipe_video_metadata(file_path, tmp_path)
    else:
        error_msg = "Unsupported file extension format."

    # Step 2: Atomic Swap (If the clean file was built successfully, replace the original)
    if success and os.path.exists(tmp_path):
        try:
            # Safely replace the original file with the clean temp file
            shutil.move(tmp_path, file_path)
            print(f"\n✅ SUCCESS: Metadata completely scrubbed!")
            print(f"💾 Original file safely overwritten: {file_path}")
        except Exception as e:
            print(f"\n❌ FAILED to overwrite original file: {str(e)}")
            if os.path.exists(tmp_path):
                os.remove(tmp_path) # Clean up temp file if move fails
    else:
        print(f"\n❌ FAILED: {error_msg}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    print("="*50 + "\n")

def main():
    clear_screen()
    print("====================================================")
    print("    🧼 AUTOMATIC OVERWRITE: METADATA & EXIF WIPER   ")
    print("====================================================")
    print("⚠️ WARNING: This tool directly overwrites original files.")
    print("====================================================")
    
    while True:
        try:
            print("👇 Drag and drop your image or video file directly into this terminal")
            print("   (Or type 'exit' to quit)")
            user_input = input("\nFile Path: ")
            
            if user_input.strip().lower() == 'exit':
                print("Exiting tool. Privacy preserved.")
                break
                
            if not user_input.strip():
                continue
                
            process_file(user_input)
            print("-" * 50)
        except KeyboardInterrupt:
            print("\nExiting tool.")
            sys.exit(0)

if __name__ == "__main__":
    main()
