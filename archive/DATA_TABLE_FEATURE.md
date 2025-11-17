# Data Table Feature Guide

## Overview

The NFL DFS Visualizer now includes a **two-tab interface** that lets you switch between a visual chart and a comprehensive data table. Both views are completely independent and show your CSV data in different ways.

---

## Features

### Tab 1: Chart View (Existing)
- Interactive scatter plot visualization
- Customizable axes and bubble sizes
- Zoom and pan functionality
- Position filtering
- Team and salary range filters
- Export as PNG

### Tab 2: Data Table (NEW!)
- **All Players**: Shows every player from your CSV (all positions)
- **Sortable Columns**: Click any column header to sort ascending/descending
- **Search/Filter**: Real-time search by player name or team
- **Column Visibility**: Show/hide columns using the "Columns" dropdown
- **Pagination**: 25 players per page with Previous/Next navigation
- **Player Headshots**: Thumbnail images in the Player column
- **Formatted Data**: Proper currency and percentage formatting

---

## Using the Data Table

### Switching Tabs

Immediately below the title, you'll see two tabs:
- **Chart View**: Shows filters and interactive scatter plot
- **Data Table**: Shows ONLY the data table (no filters)

Click either tab to switch views. Each tab maintains its own state independently.

**Important**: When you click "Data Table", the entire page switches to show just the table - no chart configuration or filters. This gives you a clean, focused view of your data.

### Searching and Filtering

1. **Global Search Box**: Type in the search field to filter by:
   - Player name (e.g., "Patrick Mahomes")
   - Team abbreviation (e.g., "KC")

2. **Column Filters**: Click the filter icon (☰) in any column header to:
   - **Position**: Select positions via checkboxes (QB, RB, WR, TE, DST)
   - **Team**: Select multiple teams via checkboxes
   - **Numeric Columns**: Set Min/Max ranges for:
     - Salary ($3,000 - $12,000)
     - Projection, Std Dev, Ceiling
     - Boom %, Bust %, Own %, Optimal %
     - Leverage

3. **Active Filter Indicator**: Columns with active filters show:
   - Filled dot (●) instead of filter icon (☰)
   - Light blue background highlight

4. **Clear Filters Button**: Resets search, sorting, column filters, and pagination

### Sorting Data

- Click any column header to sort by that column
- First click: Sort ascending (▲)
- Second click: Sort descending (▼)
- Works on all columns (text and numbers)

### Column Visibility

1. Click the **"Columns ▾"** button
2. A dropdown menu appears with all available columns
3. Check/uncheck columns to show/hide them
4. Player Name is always visible (locked)

Available columns:
- Player (with headshot)
- Team (logo display)
- Position (color-coded badge: QB=Red, RB=Green, WR=Blue, TE=Orange, DST=Gray)
- Salary
- Projection
- Std Dev
- Ceiling
- Boom %
- Bust %
- Own %
- Optimal %
- Leverage

### Pagination

- **25 players per page**
- Use **Previous/Next** buttons to navigate
- See current page and total pages
- View count shows: "Showing 1-25 of 263 players"

---

## Table vs Chart: Key Differences

### Data Table Tab:
- Shows **ALL players** from your CSV (not filtered by position)
- Independent from chart filters
- Salary/ownership range filters **do not** affect the table
- Great for reviewing raw data
- Sortable by any stat
- Search functionality

### Chart View Tab:
- Respects position filter (QB, RB, WR, TE, DST, ALL)
- Applies team, salary, and ownership filters
- Visual representation of relationships
- Zoom and pan for detailed analysis
- Export as image

---

## Data Included

Every row in your CSV is shown with these fields:

| Column | Description | Format |
|--------|-------------|--------|
| Player | Player name with headshot (team-colored border) | Text + Image |
| Team | Team logo | Logo Image |
| Pos | Player position with color badge | Red QB, Green RB, Blue WR, Orange TE, Gray DST |
| Salary | DraftKings salary | $8,500 |
| Projection | Projected points | 15.3 |
| Std Dev | Standard deviation | 3.2 |
| Ceiling | Ceiling projection | 25.5 |
| Boom % | Boom percentage | 15.3% |
| Bust % | Bust percentage | 22.1% |
| Own % | Ownership percentage | 8.5% |
| Optimal % | Optimal percentage | 12.3% |
| Leverage | Leverage score | 3.8 |

---

## Common Use Cases

### Use Case 1: Find Specific Players
**Scenario**: You want to find all Ravens players

1. Switch to **Data Table** tab
2. Click the filter icon (☰) in the **Team** column header
3. Check the "BAL" checkbox
4. View all Baltimore Ravens players
5. Sort by Salary or Projection as needed

**Alternative**: Type "BAL" in the global search box

### Use Case 2: Compare Stats Across Positions
**Scenario**: Who has the highest leverage across all positions?

1. Switch to **Data Table** tab
2. Click the **Leverage** column header
3. Table sorts by leverage (highest first)
4. See top leverage plays regardless of position

### Use Case 3: Export Data to Excel
**Scenario**: You want to work with the data in a spreadsheet

1. Switch to **Data Table** tab
2. Use your browser's "Select All" (Cmd+A / Ctrl+A)
3. Copy the table
4. Paste into Excel/Google Sheets

### Use Case 4: Hidden Gem Hunting
**Scenario**: Find low-owned, high-projection players

1. Switch to **Data Table** tab
2. Click filter icon (☰) on **Own %** column
3. Set Max to **10** (players under 10% ownership)
4. Click filter icon (☰) on **Projection** column
5. Set Min to **15** (projected 15+ points)
6. View only low-owned, high-upside plays
7. Sort by Boom % to find ceiling plays

---

## Responsive Design

The data table adapts to your screen size:

### Desktop (> 768px):
- Full table with all columns
- Horizontal scroll if needed
- Larger text and padding

### Mobile/Tablet (< 768px):
- Smaller font size for better fit
- Reduced padding
- Horizontal scroll enabled
- Controls stack vertically

---

## Tips and Tricks

1. **Quick Player Lookup**: Use the search box instead of scrolling through pages

2. **Multi-Sort Workaround**: Sort by one column, then note the players, then sort by another

3. **Column Visibility for Screenshots**: Hide columns you don't need before taking a screenshot

4. **Pagination Shortcut**: Type in the search box to filter, reducing total pages

5. **Headshot Fallback**: If a player headshot doesn't load, you'll see team logos instead

6. **Name Matching**: Players with custom name mappings will display correctly with their headshots

---

## Technical Details

### Performance
- Loads instantly (data is embedded in HTML)
- No server required
- Sorts and filters happen client-side
- Handles 200+ players smoothly

### Browser Compatibility
- Chrome, Firefox, Safari, Edge (modern versions)
- Requires JavaScript enabled
- Works offline after HTML is generated

### Data Source
- All data comes from your uploaded CSV
- Table shows exact values from the CSV
- Formatting is applied for display only (original values unchanged)

---

## Troubleshooting

### Problem: Table shows "0 players"
**Solution**: Check that your CSV was processed correctly. Refresh the page.

### Problem: Sort doesn't work as expected
**Solution**: Click the column header again to toggle between ascending/descending.

### Problem: Search returns no results
**Solution**: Check spelling, try searching by team abbreviation instead.

### Problem: Columns dropdown stays open
**Solution**: Click anywhere outside the dropdown to close it.

### Problem: Can't see all columns
**Solution**:
- Use horizontal scroll in the table wrapper
- Or hide some columns using the Columns menu
- Or expand your browser window

### Problem: Player headshots not showing
**Solution**: This is normal for players with name mismatches. Use the name matching feature in the GUI to map them.

---

## Keyboard Shortcuts

While no dedicated keyboard shortcuts exist, you can use standard browser shortcuts:

- **Cmd/Ctrl + F**: Browser find (searches visible page content)
- **Tab**: Navigate between controls
- **Enter**: Activate focused button
- **Escape**: Close dropdown menus

---

## Summary

The Data Table feature provides:
✓ Complete view of all CSV data
✓ Flexible sorting and filtering
✓ Column customization
✓ Easy data exploration
✓ Independent from chart filters
✓ Professional, clean design
✓ Fully responsive
✓ No internet required

Use it alongside the Chart View for comprehensive DFS analysis!
