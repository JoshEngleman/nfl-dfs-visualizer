# Deployment Instructions

## Files to Upload to GoDaddy

### 1. Upload Website
**File**: `index.html`  
**Destination**: `/public_html/nfl-dfs/index.html`  
**Method**: cPanel File Manager or FTP

### 2. Upload Headshots
**Folder**: `../cache/headshot_cache_compressed/*`  
**Destination**: `/public_html/nfl-dfs/headshots/`  
**Method**: FTP (FileZilla recommended for bulk upload)

## Quick Deploy Checklist

- [ ] Upload `index.html` to `/public_html/nfl-dfs/`
- [ ] Upload compressed headshots to `/public_html/nfl-dfs/headshots/`
- [ ] Test website: https://joshengleman.com/nfl-dfs/
- [ ] Upload new CSV via website interface

## Weekly Updates

No deployment needed! Just:
1. Visit https://joshengleman.com/nfl-dfs/
2. Click "Upload CSV"
3. Select your weekly CSV file
4. Done!

## Adding New Player Headshots

If you need headshots for new players:

```bash
# From project root
python3 src/update_headshots_from_csv.py data/your-new-file.csv
```

Then upload new files from `cache/headshot_cache_compressed/` to server.
