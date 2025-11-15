# NFL DFS Visualization - Simple Weekly Workflow

## 🎯 Your New Workflow (No Python Required!)

### Weekly Data Updates

**Every week when you get new DFS data:**

1. **Get your CSV file** from DraftKings/Stokastic/your DFS tool

2. **Visit your website**
   ```
   https://joshengleman.com/nfl-dfs/
   ```

3. **Click "Upload CSV" button** (blue button in top right)

4. **Select your CSV file** from your computer

5. **Wait 10-30 seconds** while it processes
   - You'll see status messages: "Processing X players..."
   - Then: "Fetching images: X/Y"
   - Finally: "Upload successful! Reloading..."

6. **Done!** Page reloads with your new data

**Time: 30 seconds** ⚡️

---

## 💾 Data Persistence

- Your uploaded data is saved in your browser's localStorage
- Data persists across page refreshes and browser restarts
- Data is specific to YOUR browser only (not shared with others)
- Different browsers/devices can have different data

---

## 🔄 Reset to Original Data

If you want to go back to the original embedded data:

1. Click the **"Reset Data"** button (red button in top right)
2. Confirm in the dialog
3. Page reloads with original data

---

## 📸 Player Headshots

Headshots load automatically in this order:

1. **Embedded data** (players from original dataset) - Instant ✅
2. **Server folder** (`/nfl-dfs/headshots/`) - Fast ✅
3. **ESPN API** - Slower, may have CORS issues ⚠️
4. **Team logo fallback** - Always works ✅

Most players should load instantly from the server folder you uploaded.

---

## 🖥️ CSV Format Requirements

Your CSV must have these columns (exact names may vary):

**Required:**
- Name / player_name
- Position / Pos
- Team / team_abbr
- Salary
- Projection / dk_projection
- Std Dev / std_dev / StdDev
- Ceiling
- Bust% / bust_pct / Bust
- Boom% / boom_pct / Boom
- Own% / ownership_pct / Ownership
- Optimal% / optimal_pct / Optimal
- Leverage

**Example:**
```csv
Name,Position,Team,Salary,Projection,Std Dev,Ceiling,Bust%,Boom%,Own%,Optimal%,Leverage
Trey McBride,TE,ARI,6.3,19.9,8.9,25.9,22.1,31.8,28.6,29.27,0.7
Christian McCaffrey,RB,SF,9,26.8,8.5,32.6,19.9,28.8,36.9,38.83,1.97
```

**Note:** Salary can be in thousands (6.3 = $6,300) or full dollars (6300)

---

## 🆘 Troubleshooting

### Upload button doesn't appear
- Hard refresh: **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac)
- Check browser console for errors (F12)

### CSV upload fails
- Verify CSV has all required columns
- Check file size is reasonable (<5MB)
- Try a smaller sample first (10-20 players)

### "NO PLAYERS AVAILABLE" after upload
- Check salary values are correct (should be in thousands or full dollars)
- Open browser console (F12) and look for error messages
- Try resetting data and uploading again

### Headshots don't load
- Most headshots should load from server
- ESPN API may fail due to CORS (will fallback to team logos)
- Ensure headshots folder is deployed correctly

### Data doesn't persist
- Check if in private/incognito mode (localStorage disabled)
- Ensure browser allows localStorage
- Try a different browser

---

## 🚫 What You DON'T Need Anymore

- ❌ No Python installation required
- ❌ No command line / terminal
- ❌ No local HTML generation
- ❌ No manual file uploads to server
- ❌ No package management (pip, conda, etc.)

---

## 📱 Access From Anywhere

Since everything is web-based now:

- ✅ Update from your laptop
- ✅ Update from your desktop
- ✅ Update from your phone/tablet
- ✅ Update from a friend's computer
- ✅ Works on any modern browser

---

## 🎉 Summary

**Before:**
```
1. Download CSV
2. Open terminal
3. Run Python script
4. Wait for processing
5. Upload HTML to GoDaddy
6. Test website

Time: 5-10 minutes
Requires: Python, packages, local environment
```

**Now:**
```
1. Download CSV
2. Click "Upload CSV" on website
3. Select file
4. Done!

Time: 30 seconds
Requires: Just a web browser
```

**10x faster, infinitely easier!** 🚀

---

## 📞 Need Help?

If you encounter issues:

1. Check browser console (F12) for errors
2. Try with a small sample CSV first
3. Verify CSV format matches requirements
4. Hard refresh the page (Ctrl+Shift+R)

---

**Last Updated:** November 2025
