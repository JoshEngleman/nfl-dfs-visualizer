# GoDaddy Deployment Guide: NFL DFS Boom/Bust Visualization

This guide will walk you through deploying your NFL DFS Boom/Bust visualization to your GoDaddy hosted website at joshengleman.com.

## Overview

You'll be creating a new section at `joshengleman.com/nfl-dfs/` where the visualization will live as a standalone page.

## Prerequisites

- Active GoDaddy hosting for joshengleman.com
- `index.html` file (the renamed visualization)
- FTP client (FileZilla recommended) OR access to cPanel File Manager

---

## Method 1: Upload via cPanel File Manager (Easiest)

### Step 1: Log into cPanel

1. Go to your GoDaddy account: https://www.godaddy.com/
2. Navigate to **My Products** → **Web Hosting**
3. Click **Manage** next to your hosting plan
4. Click **cPanel Admin** button

### Step 2: Navigate to File Manager

1. In cPanel, scroll down to **Files** section
2. Click **File Manager**
3. You'll see your file directory structure

### Step 3: Create the nfl-dfs Directory

1. Navigate to `public_html/` folder (this is your website root)
2. Click **+ Folder** button at the top
3. Name it: `nfl-dfs`
4. Click **Create New Folder**

### Step 4: Upload the Visualization

1. Click on the `nfl-dfs` folder to open it
2. Click **Upload** button at the top
3. Click **Select File** and choose your `index.html` file
4. Wait for upload to complete (should be quick, ~269KB)
5. The upload window will show "Upload Complete"

### Step 5: Set File Permissions (if needed)

1. Right-click on `index.html` in File Manager
2. Select **Permissions**
3. Ensure permissions are set to `644` (usually default)
   - Owner: Read + Write
   - Group: Read
   - World: Read
4. Click **Change Permissions**

### Step 6: Test Your Site

1. Open a web browser
2. Go to: `https://joshengleman.com/nfl-dfs/`
3. The visualization should load and be fully interactive

---

## Method 2: Upload via FTP/SFTP (Recommended for Regular Updates)

### Step 1: Get Your FTP Credentials

1. Log into your GoDaddy account
2. Go to **My Products** → **Web Hosting** → **Manage**
3. Find **FTP** section or click **Settings** → **FTP/SFTP**
4. Note down:
   - **Hostname/Server:** Usually `ftp.yourdomain.com` or IP address
   - **Username:** Your FTP username
   - **Password:** Your FTP password (reset if needed)
   - **Port:** 21 (FTP) or 22 (SFTP - more secure)

### Step 2: Download and Install FileZilla (if needed)

1. Go to: https://filezilla-project.org/
2. Download FileZilla Client (free)
3. Install on your computer

### Step 3: Connect to Your GoDaddy Server

1. Open FileZilla
2. Enter connection details in the top bar:
   - **Host:** `sftp://yourhostname.com` (for SFTP) or `ftp://yourhostname.com` (for FTP)
   - **Username:** Your FTP username
   - **Password:** Your FTP password
   - **Port:** 22 (SFTP) or 21 (FTP)
3. Click **Quickconnect**
4. Accept certificate if prompted (for SFTP)

### Step 4: Navigate to Website Root

1. In the **Remote site** panel (right side), navigate to `public_html/`
2. This is your website's root directory

### Step 5: Create nfl-dfs Directory

1. Right-click in the Remote site panel
2. Select **Create directory**
3. Name it: `nfl-dfs`
4. Press Enter

### Step 6: Upload index.html

1. On your **Local site** panel (left side), navigate to your project folder:
   `/Users/joshengleman/Documents/python_projects/random-utilities/`
2. On the **Remote site** panel (right side), double-click the `nfl-dfs` folder to open it
3. Drag and drop `index.html` from left panel to right panel
4. FileZilla will show transfer progress at the bottom
5. Wait for "File transfer successful" message

### Step 7: Verify File Permissions

1. Right-click on `index.html` in the Remote site panel
2. Select **File permissions**
3. Set numeric value to: `644`
   - Or check: Read (Owner, Group, Public), Write (Owner only)
4. Click **OK**

### Step 8: Test Your Site

1. Open a web browser
2. Go to: `https://joshengleman.com/nfl-dfs/`
3. The visualization should load and be fully interactive

---

## Troubleshooting

### Issue: "403 Forbidden" Error

**Solution:** Check file permissions. Should be `644` for index.html and `755` for the nfl-dfs directory.

```
File: 644 (rw-r--r--)
Directory: 755 (rwxr-xr-x)
```

### Issue: "404 Not Found" Error

**Solutions:**
- Verify the file is named exactly `index.html` (lowercase)
- Verify the file is in `public_html/nfl-dfs/` directory
- Check the URL is correct: `https://joshengleman.com/nfl-dfs/`

### Issue: Visualization Loads but Images Don't Show

**Solution:** This shouldn't happen since images are base64-encoded, but if it does:
- Check browser console for errors (F12 → Console tab)
- Verify the HTML file uploaded completely (check file size is ~269KB)
- Try clearing browser cache and reloading

### Issue: Interactive Features Don't Work

**Solution:**
- Check browser console for JavaScript errors
- Verify you're accessing via `https://` not `file://`
- Ensure your browser has JavaScript enabled
- Check if CDN libraries are loading (requires internet connection)

---

## Future Updates Workflow

When you want to update the visualization with new data:

### Step 1: Generate New Visualization Locally

```bash
cd /Users/joshengleman/Documents/python_projects/random-utilities
python nfl_dfs_visualizer.py --csv "NEW_DATA_FILE.csv" --output index.html
```

### Step 2: Upload to GoDaddy

**Via cPanel:**
1. Go to File Manager → `public_html/nfl-dfs/`
2. Select existing `index.html` and delete it
3. Upload new `index.html`

**Via FTP:**
1. Connect to your server via FileZilla
2. Navigate to `public_html/nfl-dfs/`
3. Drag new `index.html` from local to remote (overwrite when prompted)

### Step 3: Verify Update

1. Visit `https://joshengleman.com/nfl-dfs/`
2. Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
3. Verify new data is showing

---

## Optional Enhancements

### Add Navigation Link from Main Site

Edit your main site's navigation menu to include:
```html
<a href="/nfl-dfs/">NFL DFS Analysis</a>
```

### Create a Custom Landing Page

If you want a description page before the visualization:
1. Rename `index.html` to `visualization.html`
2. Create a new `index.html` with description and a link to `visualization.html`
3. Upload both files

### Enable HTTPS (if not already)

1. In cPanel, go to **Security** → **SSL/TLS Status**
2. Enable AutoSSL for your domain (free)
3. This ensures secure access via `https://`

---

## Directory Structure on Server

After deployment, your structure should look like:

```
public_html/
├── index.html              (your main site homepage)
├── nfl-dfs/               (new directory)
│   └── index.html         (the visualization)
├── (other existing files)
```

Accessible at: `https://joshengleman.com/nfl-dfs/`

---

## File Specifications

- **File:** index.html
- **Size:** ~269 KB
- **Type:** Static HTML/JavaScript
- **Requirements:** Modern browser, internet connection (for CDN libraries)
- **Server Requirements:** None (static file hosting only)

---

## Support

If you encounter issues:

1. Check GoDaddy's hosting documentation
2. Contact GoDaddy support for hosting-specific issues
3. Check browser console (F12) for JavaScript errors
4. Verify file permissions and directory structure

---

## Security Notes

- The visualization is read-only (no form submissions or data collection)
- All data is embedded in the HTML file
- Uses reputable CDNs (unpkg.com, cdnjs.cloudflare.com)
- No sensitive data exposure
- No backend or database connections

---

## Performance

- File size: ~269KB (very small)
- Loads quickly on broadband connections
- All processing happens client-side (in browser)
- No server load impact
- Works well on mobile devices

---

**That's it! Your NFL DFS Boom/Bust visualization is now live on your personal website.**
