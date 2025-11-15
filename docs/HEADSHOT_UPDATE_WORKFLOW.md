# Headshot Update Workflow

## 🎯 When to Use This Workflow

Use this workflow when:
- New players appear in your CSV files who don't have headshots yet
- A player's headshot is missing or showing as a team logo
- You want to bulk-download headshots for all players in a CSV

## ⚡️ Quick Workflow

**Time: 2-3 minutes total**

### Step 1: Download New Headshots (1-2 minutes)

```bash
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv
```

**What this does:**
- Reads your CSV file
- Identifies players who don't have cached headshots
- Downloads headshots from NFL.com (applies name mappings automatically)
- Compresses images to ~60KB each for web optimization
- Saves to `cache/headshot_cache_compressed/`

**Example output:**
```
🔍 Found 13 players needing headshots...

📥 Downloading headshots from NFL.com...
   ✅ Downloaded: Brock Purdy
   ✅ Downloaded: Ray-Ray McCloud (mapped from Ray-Ray McCloud III)
   ✅ Downloaded: Ashton Jeanty
   ...

📊 Download Summary:
   ✅ Downloaded: 13
   ❌ Failed: 0
```

### Step 2: Deploy to Server (1 minute)

```bash
./deploy.sh headshots
```

**What this does:**
- Connects to your GoDaddy server via FTP
- Uploads all headshots to `/public_html/nfl-dfs/headshots/`
- Shows progress for each file

**Example output:**
```
============================================================
NFL DFS Visualization - Deployment Tool
============================================================
🔌 Connecting to ftp.joshengleman.com...
✅ Connected as josh

📸 Deploying headshots...
   Found 279 headshots to upload
   ✅ Uploaded Brock_Purdy.png (62,276 bytes)
   ✅ Uploaded RayRay_McCloud.png (64,260 bytes)
   ...

   📊 Results: 279 uploaded, 0 failed
👋 Disconnected from FTP server
```

### Step 3: Verify on Website

1. Visit https://joshengleman.com/nfl-dfs/
2. Upload your CSV
3. Check that player headshots now appear

**Done!** ✅

---

## 🔧 Detailed Instructions

### Prerequisites

Make sure you have:
- ✅ uv installed (`brew install uv`)
- ✅ Virtual environment set up (`.venv/`)
- ✅ Dependencies installed (`uv pip install -r requirements.txt`)
- ✅ FTP credentials in `.env` file

### Download Headshots Script

**Command:**
```bash
.venv/bin/python src/update_headshots_from_csv.py <csv-file-path>
```

**Options:**
```bash
# Download headshots from specific CSV
.venv/bin/python src/update_headshots_from_csv.py data/week11.csv

# Use default data file
.venv/bin/python src/update_headshots_from_csv.py "data/NFL DK Boom Bust.csv"
```

**What it does:**

1. **Loads CSV**: Reads player data from your CSV file
2. **Checks Cache**: Identifies players without cached headshots
3. **Applies Name Mappings**: Uses `name_mappings.json` for players with suffixes
4. **Downloads from NFL.com**: Scrapes player pages for headshot URLs
5. **Compresses Images**: Optimizes images to ~60KB for web
6. **Saves Locally**: Stores in `cache/headshot_cache_compressed/`

**Name Mapping Example:**

If your CSV has:
```
Ray-Ray McCloud III,WR,NYG
```

The script automatically maps to:
```
Ray-Ray McCloud
```

And downloads from: `https://www.nfl.com/players/ray-ray-mccloud/`

### Deploy Headshots Script

**Command:**
```bash
./deploy.sh headshots
```

**Alternative (direct Python):**
```bash
.venv/bin/python src/deploy.py headshots
```

**What it does:**

1. **Loads FTP credentials** from `.env` file
2. **Connects to GoDaddy** server
3. **Creates directory** if needed: `/public_html/nfl-dfs/headshots/`
4. **Uploads all PNG files** from `cache/headshot_cache_compressed/`
5. **Shows progress** for each file
6. **Disconnects** gracefully

**Deployment Options:**
```bash
# Deploy only headshots
./deploy.sh headshots

# Deploy only website (index.html)
./deploy.sh website

# Deploy everything (website + headshots)
./deploy.sh all
```

---

## 🗺️ Name Mapping System

### When Players Need Mapping

Players with suffixes often have different names on NFL.com:
- ❌ "Kyle Pitts Sr." (CSV name)
- ✅ "Kyle Pitts" (NFL.com name)

### How to Add Mappings

Edit `name_mappings.json`:

```json
{
  "mappings": {
    "Player Name|TEAM": "Mapped Name"
  }
}
```

**Example:**
```json
{
  "mappings": {
    "Kyle Pitts Sr.|ATL": "Kyle Pitts",
    "Aaron Jones Sr.|MIN": "Aaron Jones",
    "James Cook III|BUF": "James Cook",
    "Ray-Ray McCloud III|NYG": "Ray-Ray McCloud"
  }
}
```

**Important:**
- Key format: `"Player Name|TEAM"`
- Use exact team abbreviation from CSV
- Mapped name should match NFL.com URL

### Name Mapping is Used By:

1. **Python scripts** (`update_headshots_from_csv.py`)
   - Applies mapping before fetching from NFL.com

2. **Website** (`index.html`)
   - NAME_MAPPINGS constant embedded in HTML
   - Used when fetching headshots from server

Both systems use the same mappings for consistency.

---

## 📊 Understanding the Output

### Download Script Output

**Players needing headshots:**
```
🔍 Analyzing CSV file...
   Total players: 100
   Already cached: 87
   Need download: 13
```

**Download progress:**
```
📥 Downloading headshots from NFL.com...
   ✅ Downloaded: Brock Purdy (62,276 bytes)
   → Applying name mapping: 'Ray-Ray McCloud III' → 'Ray-Ray McCloud'
   ✅ Downloaded: Ray-Ray McCloud (64,260 bytes)
   ❌ Failed: Unknown Player (not found on NFL.com)
```

**Summary:**
```
📊 Download Summary:
   ✅ Downloaded: 12
   ❌ Failed: 1
   📁 Saved to: cache/headshot_cache_compressed/
```

### Deploy Script Output

**Connection:**
```
🔌 Connecting to ftp.joshengleman.com...
✅ Connected as josh
   Server: 220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------
```

**Upload progress:**
```
📸 Deploying headshots...
   Found 279 headshots to upload
   ✅ Uploaded Brock_Purdy.png (62,276 bytes)
   ✅ Uploaded Christian_McCaffrey.png (64,711 bytes)
   ...
```

**Summary:**
```
   📊 Results: 279 uploaded, 0 failed
👋 Disconnected from FTP server
```

---

## 🆘 Troubleshooting

### Download Issues

**Problem: "Player not found on NFL.com"**

Solution:
1. Check player name spelling in CSV
2. Add name mapping in `name_mappings.json`
3. Try alternative name format
4. Player may be rookie or practice squad (not on NFL.com yet)

**Problem: "Connection timeout"**

Solution:
1. Check internet connection
2. NFL.com may be temporarily down
3. Try again in a few minutes
4. Some players may be rate-limited

**Problem: "No players need headshots"**

This is normal! It means:
- All players already have cached headshots
- Script is working correctly
- No download needed

### Deploy Issues

**Problem: "Connection failed"**

Solution:
1. Check `.env` file has correct credentials
2. Verify FTP_HOST, FTP_USER, FTP_PASS are set
3. Try connecting with FileZilla to test credentials
4. Check firewall isn't blocking FTP

**Problem: "Upload failed for some files"**

Solution:
1. Check file permissions in cache folder
2. Try deploying again (resume from where it failed)
3. Check GoDaddy server has enough disk space
4. Verify remote directory exists and is writable

**Problem: "Headshots upload but don't show on website"**

Solution:
1. Hard refresh website (Ctrl+Shift+R or Cmd+Shift+R)
2. Check browser console for 404 errors
3. Verify headshot URL: `https://joshengleman.com/nfl-dfs/headshots/Player_Name.png`
4. Check file permissions on server (should be 644)

---

## 📁 File Locations

### Local Files
```
cache/
├── headshot_cache/                 # Original downloads (large)
└── headshot_cache_compressed/      # Optimized for web (~60KB each)
    ├── Brock_Purdy.png
    ├── Christian_McCaffrey.png
    └── ... (279 files)
```

### Server Files (GoDaddy)
```
/public_html/nfl-dfs/
└── headshots/
    ├── Brock_Purdy.png
    ├── Christian_McCaffrey.png
    └── ... (279 files)
```

### Configuration
```
name_mappings.json       # Player name mappings
.env                     # FTP credentials (NOT in git)
.env.example            # Template for .env
```

---

## 🔄 Regular Workflow

### Beginning of NFL Season

Download all headshots for the season:

```bash
.venv/bin/python src/update_headshots_from_csv.py data/week1.csv
./deploy.sh headshots
```

### Weekly Updates

Most weeks, you won't need to do anything! But if you see missing headshots:

```bash
# Download new player headshots
.venv/bin/python src/update_headshots_from_csv.py data/week11.csv

# Deploy only if new players were downloaded
./deploy.sh headshots
```

### Mid-Season Check

Occasionally verify all headshots are working:

1. Upload latest CSV to website
2. Look for any team logos (should be headshots)
3. If you find missing players, run update script
4. Deploy to server

---

## 💡 Pro Tips

### Batch Processing

If you have multiple CSV files:

```bash
# Download from all CSVs
for csv in data/*.csv; do
    .venv/bin/python src/update_headshots_from_csv.py "$csv"
done

# Deploy once after all downloads
./deploy.sh headshots
```

### Verify Before Deploy

Check what will be deployed:

```bash
# Count headshots
ls cache/headshot_cache_compressed/*.png | wc -l

# Check file sizes
du -sh cache/headshot_cache_compressed/
```

### Deploy Only New Files

Currently the script uploads all files. To upload only new ones, use FileZilla:
1. Connect via FTP
2. Upload `cache/headshot_cache_compressed/` folder
3. Choose "Overwrite if source newer" option

---

## 📊 Performance Metrics

**Download Speed:**
- ~1-2 seconds per player
- 10 players: ~15-30 seconds
- 50 players: ~1-2 minutes

**Upload Speed:**
- ~1-2 MB/minute over FTP
- 279 files (18 MB): ~2-3 minutes
- Depends on internet connection

**Total Time:**
- Download 10 new players + deploy: ~2-3 minutes
- Download 50 new players + deploy: ~3-5 minutes

---

## ✅ Success Checklist

After running the workflow:

- [ ] Download script completed successfully
- [ ] No failed downloads (or failures are acceptable)
- [ ] Deploy script connected to FTP
- [ ] All files uploaded (279/279 or similar)
- [ ] No FTP errors
- [ ] Website shows headshots for new players
- [ ] Hard refresh clears any caching issues

---

## 📞 Getting Help

If you encounter persistent issues:

1. **Check logs**: Both scripts show detailed output
2. **Test FTP connection**: Use FileZilla to verify credentials
3. **Test NFL.com access**: Visit player pages manually
4. **Check file permissions**: Ensure cache folder is writable
5. **Review name mappings**: Verify mappings are correct

---

## 🔐 Security Notes

- **Never commit `.env`** - Contains FTP credentials
- **FTP password** is stored in plain text in `.env` - keep secure
- **Name mappings** are safe to commit - no sensitive data
- **Cache folders** are gitignored - can be large files

---

## 📚 Related Documentation

- **Deployment Setup**: `docs/DEPLOYMENT_SETUP.md` - FTP credential setup
- **Name Matching**: `docs/NAME_MATCHING_GUIDE.md` - Player name variations
- **Simple Workflow**: `docs/SIMPLE_WORKFLOW.md` - End user workflow

---

**Last Updated:** November 2025
