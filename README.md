# OPSEC EXIF Wiper

**OPSEC level 100** — Securely remove metadata and EXIF data from images and videos.

This tool helps protect your privacy by stripping sensitive metadata from files before you share them.

---

## Installation

### 1) Install Python

#### macOS

Using Homebrew:
```bash
brew install python3
```

Verify installation:
```bash
python3 --version
```

#### Windows

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. Check the box that says **Add Python to PATH**
4. Complete the installation

Verify installation in Command Prompt or PowerShell:
```cmd
python --version
```

---

### 2) Install the required dependencies

Install Pillow:

#### macOS
```bash
pip3 install Pillow
```

#### Windows
```cmd
pip install Pillow
```

Install FFmpeg:

#### macOS
```bash
brew install ffmpeg
```

#### Windows

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract it to a folder such as `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Open a new terminal and verify:

```cmd
ffmpeg -version
```

---

## Running the script

Open terminal.

### macOS

```bash
python3 meta_wiper.py
```

### Windows

```cmd
python meta_wiper.py
```

Then:
1. Drag and drop the file you want to clean into the terminal window
2. Press Enter
3. The script will overwrite the original file with a cleaned version

You do not need to type the full file path manually.

---

## Supported file types

- Images: JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP
- Videos: MP4, MOV, AVI, MKV, WebM

---

## Warning

- Back up your files before running this tool
- The original files will be overwritten
- Metadata removal is permanent

---

## License

MIT License
