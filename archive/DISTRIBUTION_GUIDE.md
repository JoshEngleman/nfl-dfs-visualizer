# NFL DFS Visualizer - Distribution Guide

## Overview

This guide explains how to use the GUI application and package it as a standalone executable for distribution to non-technical users.

---

## Option 1: Using the GUI (Python Required)

If you have Python installed, you can run the GUI directly:

### Steps:

1. **Install Dependencies** (one-time setup):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GUI**:
   ```bash
   python nfl_dfs_visualizer_gui.py
   ```

3. **Use the Application**:
   - Click "Browse..." next to CSV File to select your data file
   - (Optional) Change the output filename or location
   - (Optional) Select a specific position filter (QB, RB, WR, TE, DST, or ALL)
   - Click "Generate Visualization"
   - The app will process your data and open the HTML file automatically

---

## Option 2: Creating a Standalone Executable (Recommended for Distribution)

Package the application as a standalone executable that can run on any computer **without requiring Python**.

### Prerequisites:

- Python 3.8+ installed on your computer
- All dependencies installed: `pip install -r requirements.txt`

### For macOS:

#### Build the Application:

```bash
pyinstaller --name "NFL DFS Visualizer" \
            --windowed \
            --onefile \
            --icon=app_icon.icns \
            --add-data "nfl_dfs_visualizer.py:." \
            nfl_dfs_visualizer_gui.py
```

**Note:** If you don't have an icon file, remove the `--icon` line.

#### What This Creates:

- A single `.app` file in the `dist/` folder
- Users can double-click this app to run it (no Python needed)
- The app is about 150-300 MB (includes Python + all libraries)

#### Distribution:

1. Find the app in `dist/NFL DFS Visualizer.app`
2. You can:
   - **Zip it**: Right-click → Compress
   - **Share via USB/Cloud**: Copy the entire .app to any Mac
   - **Create a DMG** (more professional):
     ```bash
     hdiutil create -volname "NFL DFS Visualizer" \
                    -srcfolder "dist/NFL DFS Visualizer.app" \
                    -ov -format UDZO "NFL_DFS_Visualizer.dmg"
     ```

### For Windows:

#### Build the Executable:

```bash
pyinstaller --name "NFL DFS Visualizer" ^
            --windowed ^
            --onefile ^
            --icon=app_icon.ico ^
            --add-data "nfl_dfs_visualizer.py;." ^
            nfl_dfs_visualizer_gui.py
```

**Note:** If you don't have an icon file, remove the `--icon` line.

#### What This Creates:

- A single `.exe` file in the `dist/` folder
- Users can double-click this executable (no Python needed)
- The exe is about 150-300 MB

#### Distribution:

1. Find the executable in `dist/NFL DFS Visualizer.exe`
2. You can:
   - **Zip it** for easy sharing
   - **Create an installer** using NSIS or Inno Setup (optional, more advanced)
   - Share directly via USB/Cloud/Email

---

## Troubleshooting

### Build Issues:

1. **"ModuleNotFoundError" during build**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **Hidden imports missing**:
   If the app crashes when run, you may need to specify hidden imports:
   ```bash
   pyinstaller --hidden-import nfl_data_py \
               --hidden-import PIL \
               [... rest of command ...]
   ```

3. **"Operation not permitted" on macOS**:
   - Go to System Preferences → Security & Privacy → Privacy
   - Grant Terminal/PyCharm access to files

### Runtime Issues:

1. **"File not found" errors**:
   - Make sure the app and CSV file are in accessible locations
   - Avoid network drives or restricted folders

2. **Slow first run**:
   - The app needs to download NFL roster data on first run
   - This is normal and only happens once

3. **Antivirus warnings (Windows)**:
   - PyInstaller executables sometimes trigger false positives
   - You may need to add an exception or code-sign the executable

---

## File Size Optimization

The default executable is large because it includes Python + all libraries. To reduce size:

```bash
# Use --onedir instead of --onefile
pyinstaller --windowed \
            --onedir \
            nfl_dfs_visualizer_gui.py
```

This creates a folder with the executable + supporting files. Smaller individual executable, but more files to distribute.

---

## Advanced: Code Signing (Professional Distribution)

### macOS:

To avoid "unidentified developer" warnings:

1. Get an Apple Developer account ($99/year)
2. Sign the app:
   ```bash
   codesign --deep --force --verify --verbose \
            --sign "Developer ID Application: Your Name" \
            "dist/NFL DFS Visualizer.app"
   ```
3. Notarize with Apple:
   ```bash
   xcrun notarytool submit "NFL_DFS_Visualizer.dmg" \
                           --apple-id "your@email.com" \
                           --password "app-specific-password" \
                           --team-id "TEAMID" \
                           --wait
   ```

### Windows:

To avoid "unknown publisher" warnings:

1. Get a code signing certificate
2. Sign the executable using `signtool`

---

## Quick Start for Your User

Create a simple README for your users:

### For the End User:

#### macOS:
1. Download `NFL DFS Visualizer.app` (or extract from .zip/.dmg)
2. Double-click the app
3. Click "Browse..." to select your CSV file
4. Click "Generate Visualization"
5. The visualization will open automatically in your browser

#### Windows:
1. Download `NFL DFS Visualizer.exe`
2. Double-click the executable
3. If Windows SmartScreen appears, click "More info" → "Run anyway"
4. Click "Browse..." to select your CSV file
5. Click "Generate Visualization"
6. The visualization will open automatically in your browser

---

## File Structure

After building, your project will look like:

```
random-utilities/
├── nfl_dfs_visualizer.py          # Original CLI script
├── nfl_dfs_visualizer_gui.py      # GUI wrapper
├── requirements.txt                # Dependencies
├── DISTRIBUTION_GUIDE.md           # This file
├── build/                          # Build artifacts (can delete)
├── dist/                           # Your distributable app/exe
│   └── NFL DFS Visualizer.app/.exe
└── NFL DFS Visualizer.spec         # PyInstaller config (auto-generated)
```

---

## Summary

- **For yourself**: Run `python nfl_dfs_visualizer_gui.py` directly
- **For others (no Python)**: Build with PyInstaller and share the app/exe
- **File size**: 150-300 MB (includes everything)
- **No installation needed**: Just double-click and go!

---

## Questions?

- The GUI shows detailed logs during processing
- Check the "Log" section in the app for any errors
- All output goes to the same location as the input CSV by default
