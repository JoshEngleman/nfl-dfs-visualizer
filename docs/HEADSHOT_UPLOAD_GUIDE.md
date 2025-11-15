# Headshot Upload Guide - GoDaddy

## 🚀 Recommended: Automated Deployment (NEW!)

**The easiest and fastest way to deploy headshots:**

```bash
./deploy.sh headshots
```

This automatically uploads all headshots via FTP in 1-2 minutes. See [HEADSHOT_UPDATE_WORKFLOW.md](HEADSHOT_UPDATE_WORKFLOW.md) for the complete automated workflow.

---

## 📸 Manual Upload Methods (Alternative)

If you prefer manual upload or the automated deployment isn't working, use one of these methods:

**You have compressed headshots ready to upload:**
```
/Users/joshengleman/Documents/python_projects/random-utilities/cache/headshot_cache_compressed/
```

**Compression Results:**
- ✅ Original size: 1,251 MB
- ✅ Compressed size: 17.5 MB
- ✅ Savings: 98.6% reduction!
- ✅ Average per image: 66.6 KB (perfect for web)

---

## 🚀 Quick Upload (Recommended: FTP)

### Method 1: Using FTP/SFTP Client (FileZilla)

**Best for:** Bulk upload of many files (fastest)

#### Step 1: Connect to GoDaddy via FTP

1. Open **FileZilla** (or your FTP client)
2. Enter connection details:
   - **Host:** `sftp://yoursite.com` or your GoDaddy FTP hostname
   - **Username:** Your FTP username
   - **Password:** Your FTP password
   - **Port:** 22 (SFTP) or 21 (FTP)
3. Click **Quickconnect**

#### Step 2: Navigate to nfl-dfs Directory

1. In **Remote site** panel (right side):
   - Navigate to: `/public_html/nfl-dfs/`

#### Step 3: Create headshots Folder

1. Right-click in Remote site panel
2. Select **Create directory**
3. Name it: `headshots`
4. Press Enter
5. Double-click the `headshots` folder to open it

#### Step 4: Upload All Headshot Files

1. In **Local site** panel (left side):
   - Navigate to: `/Users/joshengleman/Documents/python_projects/random-utilities/headshot_cache_compressed/`
2. **Select all files:**
   - Press `Cmd+A` (Mac) or `Ctrl+A` (Windows)
3. **Drag and drop** all files to the Remote site panel
   - OR right-click → Upload
4. FileZilla shows upload progress
5. Wait for "Transfer finished" message

#### Step 5: Set Permissions

1. In Remote site panel, select all uploaded files
2. Right-click → **File permissions**
3. Set numeric value: `644`
4. Check "Apply to all files"
5. Click **OK**

**Time: 5-10 minutes** ⚡️

---

## 🌐 Alternative: Using cPanel File Manager

### Method 2: cPanel Upload

**Best for:** If you don't have FTP client installed

#### Step 1: Log into cPanel

1. Go to GoDaddy → My Products → Web Hosting → Manage
2. Click **cPanel Admin**

#### Step 2: Open File Manager

1. In cPanel, click **File Manager** under Files section

#### Step 3: Navigate and Create Folder

1. Navigate to: `public_html/nfl-dfs/`
2. Click **+ Folder** button
3. Name it: `headshots`
4. Click **Create New Folder**

#### Step 4: Upload Files

1. Click on the `headshots` folder to open it
2. Click **Upload** button
3. Click **Select File**
4. Navigate to: `/Users/joshengleman/Documents/python_projects/random-utilities/headshot_cache_compressed/`
5. Select all files (`Cmd+A` or `Ctrl+A`)
6. Click **Open**
7. Wait for all files to upload (progress bar)

**Note:** You may need to upload in batches if you have upload limits

#### Step 5: Set Permissions

1. Select all uploaded files (checkbox at top)
2. Click **Permissions** button
3. Set permissions to `644` (rw-r--r--)
4. Click **Change Permissions**

**Time: 15-30 minutes** ⏱️

---

## ✅ Verify Upload

After uploading, test if headshots are accessible:

1. Open browser
2. Visit: `https://joshengleman.com/nfl-dfs/headshots/Christian_McCaffrey.png`
3. You should see Christian McCaffrey's headshot

If you see a 404 error:
- Check file was uploaded correctly
- Check filename matches exactly (case-sensitive)
- Check permissions are set to 644

---

## 📁 Expected Server Structure

After upload, your server should look like:

```
public_html/
└── nfl-dfs/
    ├── index.html
    └── headshots/
        ├── Christian_McCaffrey.png
        ├── Trey_McBride.png
        ├── DeVon_Achane.png
        ├── Brock_Bowers.png
        └── ... (259 more files)
```

---

## 🔄 Future Updates

When you need to add headshots for NEW players:

**Recommended: Automated Workflow** ⚡️
```bash
# Download new player headshots from CSV
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv

# Deploy to server
./deploy.sh headshots
```

See [HEADSHOT_UPDATE_WORKFLOW.md](HEADSHOT_UPDATE_WORKFLOW.md) for complete details.

**Alternative: Let the website fetch them**
- CSV upload will try ESPN API
- May fall back to team logos
- Works but slower and less reliable

---

## 💾 Storage Info

- **Total files:** 263 optimized PNG images
- **Total size:** 17.5 MB (compressed from 1.2 GB!)
- **Average per image:** 66.6 KB
- **Server impact:** Minimal
- **Bandwidth:** Cached by browsers after first load
- **Load time:** Nearly instant on modern connections

---

## 🆘 Troubleshooting

### Can't connect via FTP
- Check FTP credentials in GoDaddy
- Try SFTP (port 22) instead of FTP (port 21)
- Check firewall isn't blocking connection

### Upload fails / timeout
- Upload in smaller batches (50 files at a time)
- Try during off-peak hours
- Check internet connection speed

### "403 Forbidden" when accessing headshots
- Check folder permissions: 755
- Check file permissions: 644
- Clear browser cache and try again

### Some headshots don't load on website
- Check filename matches player name exactly
- Player names with special characters may differ
- Check browser console for 404 errors

---

## ✨ All Done!

Once headshots are uploaded:

1. ✅ Visit `https://joshengleman.com/nfl-dfs/`
2. ✅ Click "Upload CSV"
3. ✅ Upload your CSV
4. ✅ Headshots load instantly from server!

**No more Python needed for weekly updates!** 🎉
