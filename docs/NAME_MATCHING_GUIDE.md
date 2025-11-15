# Player Name Matching Guide

## Overview

The Name Matching feature helps you resolve player name mismatches between your CSV data and the NFL roster database. Sometimes player names are formatted differently (e.g., "D.K. Metcalf" vs "DK Metcalf"), and this tool makes it easy to create mappings.

---

## How It Works

### Step 1: Check for Unmatched Names

1. Open the GUI and select your CSV file
2. Click the **"Check Name Matches"** button
3. The app will analyze your CSV and compare player names to the NFL roster data
4. If any names don't match, the Name Matching dialog will open

### Step 2: Map Unmatched Names

The Name Matching dialog shows:
- **CSV Name**: The player name as it appears in your CSV
- **Team**: The team abbreviation
- **Position**: The player's position
- **Mapped To**: The NFL roster name (if already mapped)
- **Status**: "Unmatched" or "Mapped"

### Step 3: Create Mappings

For each unmatched player:

#### Option A: Use Suggested Matches
1. Click on a player in the list
2. Review the "Suggested Matches" dropdown (auto-populated based on last name and team)
3. Select the correct match
4. Click "Use This Match"

#### Option B: Enter Manually
1. Click on a player in the list
2. Type the exact NFL roster name in the "Or Enter Manually" field
3. Click "Use Manual Entry"

#### Option C: Clear a Mapping
1. Click on a mapped player
2. Click "Clear Mapping" to remove the mapping

### Step 4: Save Mappings

1. Click "Save Mappings" to persist your mappings to disk
2. Close the dialog

---

## Mapping Storage

Mappings are stored in `name_mappings.json` in the following format:

```json
{
  "mappings": {
    "D.K. Metcalf|SEA": "DK Metcalf",
    "Gabe Davis|JAX": "Gabriel Davis",
    "Travis Etienne Jr.|JAX": "Travis Etienne"
  },
  "notes": "This file stores manual player name mappings from CSV to NFL roster data"
}
```

**Key Format**: `CSV_Name|TEAM_ABBR`
**Value**: Exact NFL roster name

---

## Common Mapping Scenarios

### 1. Initial/Middle Name Differences
- **CSV**: "D.K. Metcalf"
- **NFL Roster**: "DK Metcalf"
- **Solution**: Map "D.K. Metcalf|SEA" → "DK Metcalf"

### 2. Nickname vs Full Name
- **CSV**: "Gabe Davis"
- **NFL Roster**: "Gabriel Davis"
- **Solution**: Map "Gabe Davis|JAX" → "Gabriel Davis"

### 3. Suffix Differences
- **CSV**: "Travis Etienne Jr."
- **NFL Roster**: "Travis Etienne"
- **Solution**: Map "Travis Etienne Jr.|JAX" → "Travis Etienne"

### 4. Name Format Changes
- **CSV**: "AJ Brown"
- **NFL Roster**: "A.J. Brown"
- **Solution**: Map "AJ Brown|PHI" → "A.J. Brown"

---

## Best Practices

### Before Generating Visualizations
1. Always run "Check Name Matches" first with a new CSV
2. Map any unmatched names
3. Then generate your visualization

### Maintaining Mappings
- Mappings are persistent across sessions
- The same `name_mappings.json` file is used for all CSVs
- You can manually edit the JSON file if needed
- Mappings are specific to team+name combinations (handles trades)

### Finding the Correct Name
The app provides suggestions, but if you're unsure:
1. Check [NFL.com](https://www.nfl.com/players/) for official spellings
2. Search by last name and team in the suggestions dropdown
3. Look at the player's position to confirm it's the right person

---

## What Happens If You Don't Map Names?

If a player name can't be matched:
- The visualization will still generate
- That player will use their **team logo** instead of their headshot
- The data/stats will still be correct
- You'll see a note in the log about unmatched players

---

## Workflow Example

### First Time Using New CSV:

```
1. Open GUI
2. Select CSV: "NFL DK Boom Bust.csv"
3. Click "Check Name Matches"
   → Dialog shows 5 unmatched players
4. Map each player:
   - "D.K. Metcalf|SEA" → "DK Metcalf" ✓
   - "Gabe Davis|JAX" → "Gabriel Davis" ✓
   - "Travis Etienne Jr.|JAX" → "Travis Etienne" ✓
   - "AJ Brown|PHI" → "A.J. Brown" ✓
   - "DJ Moore|CHI" → "D.J. Moore" ✓
5. Click "Save Mappings"
6. Close dialog
7. Click "Generate Visualization"
   → All players now have headshots! 🎉
```

### Next Time (Same Week):
```
1. Open GUI
2. Select new CSV
3. Click "Check Name Matches"
   → "All player names matched successfully!"
   → (Uses saved mappings from last time)
4. Click "Generate Visualization"
   → Done! ✓
```

---

## Troubleshooting

### Problem: Suggestions are empty
- **Cause**: Last name doesn't match any roster players
- **Solution**: Manually type the correct NFL roster name

### Problem: Mapping doesn't work
- **Cause**: Incorrect spelling or the player isn't in the 2025 roster
- **Solution**: Double-check spelling, verify player is active this season

### Problem: Same player on different teams
- **Cause**: Player was traded mid-season
- **Solution**: Create separate mappings for each team combination
  ```json
  "Player Name|OLD": "NFL Roster Name",
  "Player Name|NEW": "NFL Roster Name"
  ```

### Problem: Lost all my mappings
- **Cause**: Deleted `name_mappings.json` file
- **Solution**: The file is in your project directory. Don't delete it!
  - You can back it up periodically
  - You can share it with others using the same CSV format

---

## Advanced: Bulk Editing

You can manually edit `name_mappings.json` for bulk changes:

```json
{
  "mappings": {
    "D.K. Metcalf|SEA": "DK Metcalf",
    "A.J. Brown|PHI": "A.J. Brown",
    "D.J. Moore|CHI": "D.J. Moore",
    "J.K. Dobbins|LAC": "JK Dobbins"
  }
}
```

**Tips:**
- Use a JSON validator to check syntax
- Keep the file format exactly as shown
- Use the exact team abbreviations from your CSV
- Names are case-sensitive

---

## Summary

The Name Matching feature:
- ✓ Automatically finds mismatched player names
- ✓ Suggests correct matches based on last name and team
- ✓ Allows manual entry for edge cases
- ✓ Saves mappings persistently
- ✓ Reuses mappings for future CSVs
- ✓ Makes your visualizations look professional with player headshots!

---

## Questions?

Check the log window in the main GUI for detailed information about which players were matched or unmatched during generation.
