# CSV Upload Feature - Implementation Complete ✅

## Overview

Your NFL DFS Boom/Bust visualization now has a **CSV upload feature** that allows you to update player data directly from the website without needing to regenerate the HTML file locally!

## What Was Added

### 1. **Upload Button (Top Right Corner)**
- Blue "Upload CSV" button positioned in the top right
- Clean, modern design that matches your existing visualization
- Click to select and upload new CSV files

### 2. **Reset Data Button**
- Red "Reset Data" button (appears only after uploading data)
- Clears uploaded data and returns to original embedded data
- Includes confirmation dialog to prevent accidental resets

### 3. **CSV Parsing Engine**
- Integrated PapaParse library for robust CSV parsing
- Automatically maps common column names to internal format
- Supports variations like "Name" / "player_name", "Boom%" / "boom_pct", etc.

### 4. **Smart Headshot Fetching**
The system tries multiple sources to get player headshots (in order):
1. **Embedded data** - Uses headshots from original HTML (instant)
2. **Server folder** - Checks `/nfl-dfs/headshots/` on your website (fast)
3. **ESPN API** - Attempts to fetch from ESPN (may have CORS issues)
4. **Team logo fallback** - Uses team logo if player headshot unavailable
5. **Placeholder** - Generic placeholder as final fallback

### 5. **localStorage Persistence**
- Uploaded data persists in your browser
- Survives page refreshes and browser restarts
- Specific to your browser only (doesn't affect other users)
- Can store ~5-10MB of data (hundreds of players)

### 6. **Status Messages**
- Real-time feedback during upload process
- Shows progress: "Processing 50 players..." → "Fetching images: 45/50"
- Success/error messages with color coding (green/red/blue)
- Auto-dismisses after 3 seconds

## How to Use

### Uploading New Data

1. **Prepare your CSV file** with these columns:
   ```
   Name, Position, Team, Salary, Projection, Std Dev, Ceiling,
   Bust%, Boom%, Own%, Optimal%, Leverage
   ```

2. **Click "Upload CSV"** button (top right)

3. **Select your CSV file** from your computer

4. **Wait for processing** (status messages will show progress)
   - Parsing CSV...
   - Processing X players...
   - Fetching images: X/Y
   - Upload successful! Reloading...

5. **Page automatically reloads** with your new data

### Resetting to Original Data

1. **Click "Reset Data"** button (top right, appears after upload)

2. **Confirm** in the dialog box

3. **Page reloads** with original embedded data

## CSV Format Requirements

### Required Columns (flexible naming):
- **Player Name:** "Name", "name", or "player_name"
- **Position:** "Position", "position", or "Pos"
- **Team:** "Team", "team", or "team_abbr"
- **Salary:** "Salary" or "salary"
- **Projection:** "Projection", "projection", or "dk_projection"
- **Std Dev:** "Std Dev", "std_dev", or "StdDev"
- **Ceiling:** "Ceiling" or "ceiling"
- **Bust%:** "Bust%", "bust_pct", or "Bust"
- **Boom%:** "Boom%", "boom_pct", or "Boom"
- **Ownership%:** "Own%", "ownership_pct", or "Ownership"
- **Optimal%:** "Optimal%", "optimal_pct", or "Optimal"
- **Leverage:** "Leverage" or "leverage"

### Example CSV:
```csv
Name,Position,Team,Salary,Projection,Std Dev,Ceiling,Bust%,Boom%,Own%,Optimal%,Leverage
Trey McBride,TE,ARI,6300,19.9,8.9,25.9,22.1,31.8,28.6,29.27,0.7
Christian McCaffrey,RB,SF,9000,26.8,8.5,32.6,19.9,28.8,36.9,38.83,1.97
```

## Technical Details

### Data Storage
- **Original data:** Embedded in HTML (~269KB)
- **Uploaded data:** Stored in browser's localStorage
- **Headshot cache:** Separate localStorage entry
- **Total storage:** ~5-10MB available (browser-dependent)

### Performance
- **Initial load:** Same as before (uses original embedded data)
- **After upload:** Slightly slower first load while fetching headshots
- **Subsequent loads:** Fast (data cached in localStorage)

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer (not supported - use modern browser)

### Data Privacy
- All data stored locally in YOUR browser only
- Not shared with other users
- Not uploaded to any server
- Cleared when you clear browser data

## Deployment Instructions

### Step 1: Deploy Updated index.html
Upload the new `index.html` file to your GoDaddy hosting:
- Location: `/public_html/nfl-dfs/index.html`
- This file now includes all upload functionality

### Step 2: Deploy Headshot Cache (Optional but Recommended)
Follow the `HEADSHOT_DEPLOYMENT_GUIDE.md` to upload headshots:
- Create `/public_html/nfl-dfs/headshots/` folder
- Upload all `.png` files from local `headshot_cache/` folder
- This enables faster headshot loading for existing players

### Step 3: Test
1. Visit `https://joshengleman.com/nfl-dfs/`
2. Click "Upload CSV" button
3. Upload a test CSV file
4. Verify data loads correctly

## Files Modified

1. **index.html** - Main visualization file
   - Added PapaParse library (CDN)
   - Added upload button UI styles
   - Added upload/reset buttons HTML
   - Added CSV parsing logic
   - Added localStorage persistence
   - Added headshot fetching functions
   - Added status messaging system

## Files Created

1. **add_upload_feature.py** - Python script that added the feature
2. **index.html.backup** - Backup of original file
3. **HEADSHOT_DEPLOYMENT_GUIDE.md** - Guide for deploying headshots
4. **UPLOAD_FEATURE_README.md** - This file

## Troubleshooting

### Upload Button Not Visible
- Check if page loaded correctly
- Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for errors (F12)

### CSV Upload Fails
- Verify CSV has required columns
- Check CSV is properly formatted (no extra quotes, commas in data)
- Ensure file size is reasonable (<5MB recommended)

### Headshots Not Loading
- Check browser console for CORS errors
- Deploy headshot_cache folder to server (see guide)
- Wait for fallback to team logos (takes a few seconds)

### "Data Too Large for Browser Storage" Error
- Reduce number of players in CSV
- Clear browser localStorage and try again
- Some browsers have stricter storage limits

### Reset Button Not Appearing
- Button only shows after uploading data
- Check browser console for errors
- Try manually: Open browser console (F12) and run:
  ```javascript
  localStorage.removeItem('nflDfsUploadedData');
  location.reload();
  ```

### Data Doesn't Persist After Upload
- Check if browser allows localStorage
- Check if in private/incognito mode (localStorage may be disabled)
- Try a different browser

## Advanced Usage

### Programmatic Data Update
You can update data programmatically via browser console:

```javascript
// Example: Add custom data
const customData = {
    ALL: [
        {
            player_name: "Custom Player",
            position: "QB",
            team_abbr: "SF",
            salary: 7000,
            // ... other fields
        }
        // ... more players
    ]
};

localStorage.setItem('nflDfsUploadedData', JSON.stringify(customData));
location.reload();
```

### Clearing All Data
```javascript
localStorage.removeItem('nflDfsUploadedData');
localStorage.removeItem('nflDfsHeadshotCache');
location.reload();
```

### Checking Current Data Source
```javascript
console.log(localStorage.getItem('nflDfsUploadedData') ? 'Using uploaded data' : 'Using original data');
```

## Benefits

✅ **No local regeneration** - Update data directly from the website
✅ **No file uploads to server** - Data stored in browser
✅ **Quick updates** - Upload new CSV in seconds
✅ **Persistent** - Data survives browser restarts
✅ **Safe** - Original data always available via Reset button
✅ **Multi-device** - Upload different data on different devices
✅ **Fast** - Server headshots load instantly when available

## Limitations

⚠️ **Browser-specific** - Each browser has its own localStorage
⚠️ **Not shared** - Other users won't see your uploaded data
⚠️ **Storage limit** - ~5-10MB depending on browser
⚠️ **CORS issues** - ESPN API fetches may fail (fallback to team logos)
⚠️ **Manual sync** - New headshots need manual deployment to server

## Future Enhancements (Optional)

Ideas for potential future additions:
- Export current data back to CSV
- Multiple saved datasets (named saves)
- Automatic headshot fetching from local cache
- Drag-and-drop CSV upload
- CSV validation with detailed error messages
- Batch upload multiple slates

---

## Summary

Your NFL DFS visualization is now a **fully functional web app** that allows CSV uploads directly from the browser!

**Next Steps:**
1. Deploy updated `index.html` to GoDaddy
2. (Optional) Deploy `headshot_cache/` folder as `/nfl-dfs/headshots/`
3. Test the upload feature with a sample CSV
4. Enjoy easy data updates without regenerating HTML!

🎉 **Feature complete and ready to deploy!**
