#!/bin/bash
# Build script for NFL DFS Visualizer (macOS/Linux)

echo "========================================"
echo "NFL DFS Visualizer - Build Script"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

echo "Building standalone application..."
echo ""

# Build command
pyinstaller --name "NFL DFS Visualizer" \
            --windowed \
            --onefile \
            --add-data "nfl_dfs_visualizer.py:." \
            --clean \
            nfl_dfs_visualizer_gui.py

echo ""
echo "========================================"
echo "Build complete!"
echo "========================================"
echo ""
echo "Your app is ready at:"
echo "  → dist/NFL DFS Visualizer.app"
echo ""
echo "You can now:"
echo "  1. Test it by double-clicking the app"
echo "  2. Zip it for distribution"
echo "  3. Create a DMG (see DISTRIBUTION_GUIDE.md)"
echo ""
