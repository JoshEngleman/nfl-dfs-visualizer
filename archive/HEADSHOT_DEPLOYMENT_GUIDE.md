# Headshot Cache Deployment Guide

This guide explains how to deploy the headshot_cache folder to your GoDaddy hosting to enable faster loading of player images when uploading new CSV files.

## Why Upload the Headshot Cache?

When you upload a new CSV file with updated player data:
1. The app first checks if player headshots are already embedded in the original HTML
2. If not found, it tries to fetch from your server's headshot folder (faster, no external API calls)
3. If still not found, it tries ESPN's API (slower, may have CORS issues)
4. Finally, falls back to team logos or placeholders

By uploading the headshot_cache folder, you ensure steps 2 works efficiently.

## Directory Structure

After deployment, your server structure should look like:

```
public_html/
└── nfl-dfs/
    ├── index.html              (the visualization with upload feature)
    └── headshots/              (new folder)
        ├── Trey_McBride.png
        ├── Christian_McCaffrey.png
        ├── DeVon_Achane.png
        ├── Brock_Bowers.png
        └── ... (all other player headshots)
```

## Method 1: Upload via cPanel File Manager

### Step 1: Log into cPanel
1. Go to GoDaddy → My Products → Web Hosting → Manage → cPanel Admin

### Step 2: Open File Manager
1. In cPanel, click **File Manager** under the Files section

### Step 3: Navigate to nfl-dfs Directory
1. Navigate to `public_html/nfl-dfs/`

### Step 4: Create headshots Directory
1. Click **+ Folder** button
2. Name it: `headshots`
3. Click **Create New Folder**

### Step 5: Upload Headshot Files
1. Click on the `headshots` folder to open it
2. Click **Upload** button
3. Click **Select File** and select ALL files from your local `headshot_cache/` folder
   - On Mac: Press `Cmd+A` to select all files in the folder
   - On Windows: Press `Ctrl+A` to select all files
4. Click **Open** to start upload
5. Wait for all files to upload (progress bar will show completion)

**Note:** You can also upload files in batches if you have many files.

### Step 6: Verify Permissions
1. Select all uploaded files (click checkbox at top of list)
2. Click **Permissions** button
3. Set permissions to `644` (rw-r--r--)
4. Click **Change Permissions**

## Method 2: Upload via FTP/SFTP (Faster for Many Files)

### Step 1: Connect to Your Server
1. Open FileZilla (or your FTP client)
2. Connect using your GoDaddy FTP credentials
   - Host: `sftp://yourhostname.com` (or FTP hostname)
   - Username: Your FTP username
   - Password: Your FTP password
   - Port: 22 (SFTP) or 21 (FTP)
3. Click **Quickconnect**

### Step 2: Navigate to nfl-dfs Directory
1. In the **Remote site** panel (right side), navigate to:
   `public_html/nfl-dfs/`

### Step 3: Create headshots Directory
1. Right-click in the Remote site panel
2. Select **Create directory**
3. Name it: `headshots`
4. Press Enter
5. Double-click the `headshots` folder to open it

### Step 4: Upload All Headshot Files
1. In the **Local site** panel (left side), navigate to:
   `/Users/joshengleman/Documents/python_projects/random-utilities/headshot_cache/`
2. Select all files in the headshot_cache folder:
   - Press `Cmd+A` (Mac) or `Ctrl+A` (Windows)
3. Drag and drop all selected files to the Remote site panel
4. FileZilla will show upload progress
5. Wait for "Transfer finished" message

**Tip:** FileZilla can upload multiple files simultaneously, making this much faster than cPanel for large numbers of files.

### Step 5: Verify File Permissions
1. In the Remote site panel, select all uploaded files
2. Right-click and select **File permissions**
3. Set numeric value to: `644`
4. Check "Apply to all files"
5. Click **OK**

## Verification

### Test if Headshots Are Accessible

1. Open a web browser
2. Navigate to: `https://joshengleman.com/nfl-dfs/headshots/Trey_McBride.png`
3. You should see the player's headshot image
4. If you see a "404 Not Found" error, check:
   - File was uploaded correctly
   - File permissions are set to `644`
   - File name matches exactly (case-sensitive)

## File Naming Convention

The headshot files should be named using the format:
- Player name with spaces replaced by underscores
- Special characters removed
- `.png` extension

Examples:
- `Trey McBride` → `Trey_McBride.png`
- `Christian McCaffrey` → `Christian_McCaffrey.png`
- `De'Von Achane` → `DeVon_Achane.png`

## Updating Headshots

When you want to add new player headshots:

### Option 1: Generate Locally and Upload
1. Run the Python visualization script with new data:
   ```bash
   python nfl_dfs_visualizer.py --csv "new_data.csv" --output temp.html
   ```
2. This will add new headshots to the `headshot_cache/` folder
3. Upload only the new headshot files to the server's `headshots/` folder via FTP or cPanel

### Option 2: Let the App Fetch Automatically
1. Upload your CSV through the web interface
2. The app will attempt to fetch headshots from ESPN API
3. These will be stored in the browser's localStorage (not on server)
4. For better performance, periodically sync these to the server manually

## Storage Considerations

### File Sizes
- Each headshot is typically 10-50 KB
- 100 players = ~1-5 MB total
- Most hosting plans can handle this easily

### Bandwidth
- Headshots are loaded when users view the visualization
- Cached by browsers after first load
- Minimal impact on hosting bandwidth

## Troubleshooting

### Issue: "403 Forbidden" When Accessing Headshots
**Solution:** Check file and folder permissions
```
Folder (headshots): 755 (rwxr-xr-x)
Files (*.png): 644 (rw-r--r--)
```

### Issue: Some Headshots Don't Load
**Solution:**
1. Check if the file exists in the `headshots/` folder
2. Verify the filename matches exactly (case-sensitive)
3. Check file permissions are `644`
4. Try accessing the file directly via URL in browser

### Issue: Upload Fails with "Disk Quota Exceeded"
**Solution:**
1. Check your hosting plan's storage limit
2. Delete unnecessary files from your hosting
3. Consider compressing images before upload
4. Upload only essential player headshots

### Issue: FTP Upload Is Very Slow
**Solution:**
1. Use SFTP instead of FTP (usually faster)
2. Try uploading during off-peak hours
3. Upload in smaller batches
4. Check your internet connection speed

## Maintenance

### Periodic Cleanup
- Remove headshots for players no longer in the league
- Delete duplicate or corrupted images
- Keep folder organized by season/year if needed

### Adding New Players
1. Generate headshot using the Python script
2. Upload to server's `headshots/` folder
3. Or let users upload CSV and app will fetch automatically

---

## Quick Reference Commands

### Via Command Line (if you have SSH access)
```bash
# Navigate to nfl-dfs directory
cd /home/username/public_html/nfl-dfs/

# Create headshots directory
mkdir headshots
chmod 755 headshots

# Upload files (from local machine)
scp /local/path/headshot_cache/*.png username@yourhost.com:/path/to/public_html/nfl-dfs/headshots/

# Set permissions
chmod 644 headshots/*.png
```

---

## Summary

**Required Steps:**
1. ✅ Create `headshots/` folder in `/public_html/nfl-dfs/`
2. ✅ Upload all `.png` files from local `headshot_cache/` folder
3. ✅ Set folder permissions to `755`
4. ✅ Set file permissions to `644`
5. ✅ Verify accessibility via browser

**Time Estimate:**
- cPanel: 15-30 minutes (depending on number of files)
- FTP: 5-10 minutes (faster for bulk uploads)

**Storage Needed:**
- Approximately 1-5 MB for 100 players

That's it! Your headshot cache is now deployed and ready to use.
