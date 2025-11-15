# Quick Start Guide

## For You (Developer):

### Option 1: Run the GUI directly
```bash
python nfl_dfs_visualizer_gui.py
```

### Option 2: Build a standalone app to share

**macOS/Linux:**
```bash
./build_app.sh
```

**Windows:**
```batch
build_app.bat
```

The app will be created in the `dist/` folder. You can then share this with anyone!

---

## For Your Users (No Python Needed):

1. **Get the app** (you'll provide them with `NFL DFS Visualizer.app` or `.exe`)
2. **Double-click** to open it
3. **Click "Browse"** to select their CSV file
4. **(Optional) Click "Check Name Matches"** to fix any player name mismatches
5. **Click "Generate Visualization"**
6. **Done!** The visualization opens automatically in their browser

---

## What's Included:

- **nfl_dfs_visualizer_gui.py**: Graphical interface with name matching (user-friendly)
- **nfl_dfs_visualizer.py**: Original command-line tool (still works!)
- **build_app.sh / .bat**: One-click build scripts
- **name_mappings.json**: Stores player name mappings (auto-created)
- **DISTRIBUTION_GUIDE.md**: Detailed distribution instructions
- **NAME_MATCHING_GUIDE.md**: Guide for mapping player names
- **QUICK_START.md**: This file

---

## Features:

- **Two-Tab Interface**: Switch between Chart View and Data Table
- **Interactive Chart**: Scatter plot with zoom, filters, and export
- **Responsive Data Table**: All your CSV data with:
  - Color-coded position badges (🔴 QB, 🟢 RB, 🔵 WR, 🟠 TE, ⚫ DST)
  - Team logos (not just abbreviations)
  - Player headshots with team-colored borders
  - Sortable columns (click headers)
  - **Per-column filters** (click ☰ icon in headers)
    - Position: Multi-select checkboxes (QB, RB, WR, TE, DST)
    - Team: Multi-select checkboxes (by abbreviation)
    - Stats: Min/Max range filters
  - Global search by player or team
  - Column visibility toggles
  - Pagination (25 players per page)
- **Name Matching**: Map mismatched player names
- **Standalone**: No internet required after generation

## The Difference:

### Before:
```bash
# Users had to run this in terminal:
python nfl_dfs_visualizer.py --csv "NFL DK Boom Bust.csv" --output boom_bust.html
```

### Now:
Users just **double-click the app** and select their file. No terminal, no Python installation needed!
