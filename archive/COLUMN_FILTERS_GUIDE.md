# Column Filters Guide

## Overview

Each column in the Data Table now has its own inline filter. Click the filter icon (☰) in any column header to set filters specific to that column.

---

## How to Use Column Filters

### Opening a Filter

1. Switch to the **Data Table** tab
2. Look at any column header
3. Click the **☰** icon (next to the column name)
4. A dropdown appears below the header

### Filter Types

#### Team Column (Checkboxes)

When you click the filter on the **Team** column:
- A dropdown with all teams appears (ARI, ATL, BAL, BUF, etc.)
- Team names shown as abbreviations in the filter (logos displayed in table)
- **Check** one or more teams to include
- **Uncheck** to exclude
- Only players from selected teams will show
- Select multiple teams to compare (e.g., KC + PHI + SF)

**Example:**
```
☑ KC
☑ BUF
☑ BAL
☐ All others...
```
Result: Shows only Chiefs, Bills, and Ravens players

#### Numeric Columns (Min/Max Range)

For all stat columns (Salary, Projection, Boom %, etc.):
- Two input fields appear: **Min** and **Max**
- Enter minimum value (or leave blank for no minimum)
- Enter maximum value (or leave blank for no maximum)
- Players outside this range are filtered out

**Example: Salary Filter**
```
Min: 7000
Max: 9500
```
Result: Shows only players priced $7,000-$9,500

**Example: Ownership Filter**
```
Min:
Max: 15
```
Result: Shows only players with under 15% ownership

---

## Filter Indicators

### Active Filter Visual Cues:

1. **Filled Dot (●)**: Filter icon changes from ☰ to ●
2. **Blue Background**: Column header gets light blue background
3. **Stays Active**: Filter persists as you sort, search, or change pages

### Multiple Filters

You can have **multiple column filters active** at once:
- Filter Team to KC + BUF
- Filter Salary to $5,000-$8,000
- Filter Boom% to Min 20
- All filters apply simultaneously (AND logic)

---

## Examples

### Example 1: Value Plays
**Goal**: Find affordable high-projection players

1. Click ☰ on **Salary**
   - Set Max: **6500**
2. Click ☰ on **Projection**
   - Set Min: **12**
3. Result: Players under $6,500 projected for 12+ points

### Example 2: GPP Leverage
**Goal**: Find low-owned ceiling plays

1. Click ☰ on **Own %**
   - Set Max: **10**
2. Click ☰ on **Boom %**
   - Set Min: **25**
3. Click ☰ on **Leverage**
   - Set Min: **2**
4. Result: Under-owned players with high upside

### Example 3: Stack Comparison
**Goal**: Compare two offensive stacks

1. Click ☰ on **Team**
   - Check: **KC**, **SF**
2. Click ☰ on **Salary**
   - Set Min: **5000**
3. Result: View Chiefs and 49ers players over $5K

### Example 4: Consistent Floor
**Goal**: Find safe cash game plays

1. Click ☰ on **Std Dev**
   - Set Max: **6**
2. Click ☰ on **Bust %**
   - Set Max: **20**
3. Click ☰ on **Projection**
   - Set Min: **10**
4. Result: Consistent performers with low bust rate

---

## Clearing Filters

### Clear Individual Filter:
1. Click ☰ on the filtered column
2. Uncheck all teams OR clear Min/Max values
3. Filter dropdown stays open

### Clear All Filters:
1. Click **"Clear Filters"** button at top
2. Resets:
   - All column filters
   - Global search
   - Sort order
   - Page number

---

## Filter Combinations

Filters work together in powerful ways:

### Cash Game Lineup:
```
Team: Select your game stack teams
Salary: Min 3000, Max 10000
Bust%: Max 25
Projection: Min 8
```

### Tournament Leverage:
```
Ownership%: Max 15
Leverage: Min 1.5
Ceiling: Min 25
```

### Position-Specific (using search):
```
Search: "WR" in position column
Boom%: Min 30
Salary: Max 7000
```

### Correlation Plays:
```
Team: Check 2-3 teams
Projection: Min 12
Ownership%: Max 20
```

---

## Tips and Tricks

1. **Start Broad, Then Narrow**:
   - Apply Team filter first
   - Then add stat filters
   - Easier to visualize results

2. **One Filter at a Time**:
   - Add filters incrementally
   - See how each affects results
   - Adjust ranges as needed

3. **Use "No Max" Strategy**:
   - Only set Min on good stats (Projection, Boom%)
   - Only set Max on bad stats (Bust%, Own%)

4. **Combine with Sort**:
   - Apply filters
   - Then sort by your key metric
   - Best of both worlds

5. **Save Mental Notes**:
   - Remember winning filter combinations
   - Recreate them each week
   - Adjust for slate size

---

## Filter Persistence

### What Persists:
- Filters stay active while browsing pages
- Filters remain when sorting
- Filters work with global search

### What Resets:
- Filters clear when clicking "Clear Filters"
- Filters reset when closing the HTML file
- Filters don't save between sessions (by design)

---

## Technical Details

### Performance:
- Filters apply instantly (client-side)
- No lag even with 263 players
- Works offline

### Filter Logic:
- Multiple team checkboxes = OR logic (KC OR BUF OR BAL)
- Multiple column filters = AND logic (Salary AND Projection AND Boom%)
- Min/Max both optional (can use just one)

### Input Validation:
- Numeric fields only accept numbers
- Decimal values allowed for percentages
- Invalid input ignored gracefully

---

## Comparison: Column Filters vs. Chart Filters

| Feature | Chart Tab Filters | Table Column Filters |
|---------|------------------|---------------------|
| **Location** | Top of page | Inside column headers |
| **Affects** | Chart visualization | Table rows |
| **Position Filter** | ✓ Dropdown (QB, RB, etc.) | ✗ Use search box |
| **Team Filter** | ✓ Multi-select list | ✓ Checkboxes in header |
| **Stat Ranges** | ✓ Dual sliders | ✓ Min/Max inputs |
| **Visibility** | Always visible | Click to open |
| **Active Indicator** | N/A | ● in header |

---

## Keyboard Shortcuts

- **Tab**: Navigate between Min/Max inputs
- **Enter**: Applies filter and closes dropdown
- **Escape**: Closes filter dropdown
- **Click outside**: Closes filter dropdown

---

## Mobile Behavior

On smaller screens (< 768px):
- Filter dropdowns adjust to stay on screen
- Touch-friendly checkbox sizes
- Number inputs optimized for mobile keyboards
- Horizontal scroll for wide tables

---

## Summary

Column filters give you **surgical precision** for finding exactly the players you need:

✓ Team: Pick specific teams to analyze
✓ Salary: Find value plays in your price range
✓ Stats: Set min/max thresholds for any metric
✓ Visual: See active filters at a glance
✓ Flexible: Combine any number of filters
✓ Fast: Instant results, no page reload

Use column filters for advanced player pool construction and detailed lineup research!
