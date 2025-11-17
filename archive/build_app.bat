@echo off
REM Build script for NFL DFS Visualizer (Windows)

echo ========================================
echo NFL DFS Visualizer - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo Building standalone application...
echo.

REM Build command
pyinstaller --name "NFL DFS Visualizer" ^
            --windowed ^
            --onefile ^
            --add-data "nfl_dfs_visualizer.py;." ^
            --clean ^
            nfl_dfs_visualizer_gui.py

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Your executable is ready at:
echo   → dist\NFL DFS Visualizer.exe
echo.
echo You can now:
echo   1. Test it by double-clicking the exe
echo   2. Zip it for distribution
echo   3. Share it with others!
echo.
pause
