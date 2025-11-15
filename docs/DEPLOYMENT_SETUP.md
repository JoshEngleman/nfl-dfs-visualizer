# Automated Deployment Setup

This guide shows you how to set up automated deployment to your GoDaddy server using the `deploy.py` script.

> **Note**: This project uses **uv** for fast Python package management. No need to manually activate virtual environments - just use `./deploy.sh` or `.venv/bin/python`!

## Prerequisites

- Python 3.x installed
- **uv** package manager: `brew install uv` (already installed)
- python-dotenv package (already in requirements.txt and installed)

## Step 1: Get Your GoDaddy FTP Credentials

### Option A: Using GoDaddy cPanel

1. Log into GoDaddy
2. Go to **My Products** → **Web Hosting** → **Manage**
3. Click **cPanel Admin**
4. Find **FTP Accounts** under the Files section
5. Note your FTP details:
   - **FTP Server**: Usually `ftp.yourdomain.com`
   - **Username**: Your FTP username (usually `username@yourdomain.com`)
   - **Password**: Your FTP password

### Option B: Using GoDaddy Dashboard

1. Log into GoDaddy account
2. Go to **My Products** → **Web Hosting**
3. Click **Manage** next to your hosting plan
4. Look for **FTP** or **File Manager**
5. Click **FTP Details** or **Credentials**

### Common FTP Server Formats:
- `ftp.yourdomain.com`
- `yourdomain.com`
- An IP address like `123.45.67.89`

## Step 2: Create Your .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```bash
   # Open with your favorite editor
   nano .env
   # or
   code .env
   ```

3. Fill in your GoDaddy FTP details:
   ```
   FTP_HOST=ftp.joshengleman.com
   FTP_USER=your-ftp-username@joshengleman.com
   FTP_PASS=your-secure-password
   FTP_PORT=21

   REMOTE_BASE_PATH=/public_html/nfl-dfs
   REMOTE_HEADSHOTS_PATH=/public_html/nfl-dfs/headshots
   ```

4. Save and close the file

**⚠️ IMPORTANT**: The `.env` file is automatically excluded from git (via `.gitignore`). Never commit your credentials to version control!

## Step 3: Test the Connection

Run a test deployment of just the website:

```bash
./deploy.sh website
```

Or use the .venv Python directly:

```bash
.venv/bin/python src/deploy.py website
```

You should see:
```
🔌 Connecting to ftp.joshengleman.com...
✅ Connected as your-username
🌐 Deploying website...
   ✅ Uploaded index.html (297,984 bytes)
👋 Disconnected from FTP server
```

## Step 4: Full Deployment

Once the test works, deploy everything:

```bash
./deploy.sh all
```

This will:
1. Upload `public/index.html` to `/public_html/nfl-dfs/`
2. Upload all headshots from `cache/headshot_cache_compressed/` to `/nfl-dfs/headshots/`

## Usage Commands

**Using the wrapper script** (recommended - easiest):
```bash
# Deploy everything (website + headshots)
./deploy.sh all

# Deploy only the website (index.html)
./deploy.sh website

# Deploy only headshots
./deploy.sh headshots

# Interactive mode (asks what to deploy)
./deploy.sh
```

**Alternative - direct Python call**:
```bash
.venv/bin/python src/deploy.py all
.venv/bin/python src/deploy.py website
.venv/bin/python src/deploy.py headshots
```

## Typical Workflow

### After making changes to index.html:
```bash
./deploy.sh website
```

### After downloading new headshots:
```bash
# Download new headshots
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv

# Deploy new headshots only
./deploy.sh headshots
```

### First-time setup or major update:
```bash
./deploy.sh all
```

## Troubleshooting

### Connection Failed
- **Check credentials**: Make sure FTP_HOST, FTP_USER, and FTP_PASS are correct in `.env`
- **Try port 22 (SFTP)**: Some GoDaddy accounts use SFTP instead of FTP
  - Change `FTP_PORT=22` in your `.env` file
  - Note: This script uses FTP only. SFTP would require a different library.
- **Firewall**: Ensure your firewall allows FTP connections (port 21 or 22)
- **Passive mode**: GoDaddy usually requires passive mode (enabled by default in the script)

### "Directory not found" errors
- Check that `REMOTE_BASE_PATH` and `REMOTE_HEADSHOTS_PATH` match your server structure
- The script will try to create directories if they don't exist

### Permission denied
- Verify your FTP user has write permissions to `/public_html/nfl-dfs/`
- Contact GoDaddy support if you can't write to the directory

### Files not updating
- Clear your browser cache after deployment
- Add a cache-busting query string: `index.html?v=2`
- Check that the file was actually uploaded (use FileZilla or cPanel to verify)

## Security Best Practices

1. ✅ **Never commit .env to git** (already in .gitignore)
2. ✅ **Use strong FTP passwords** (change in GoDaddy if weak)
3. ✅ **Limit FTP user permissions** to only `/public_html/nfl-dfs/`
4. ✅ **Use SFTP if available** (port 22) instead of FTP (port 21)
5. ✅ **Rotate credentials periodically** (every 3-6 months)

## Alternative: Manual Deployment

If automated deployment isn't working or you prefer manual control:

1. **Using FileZilla** (see `HEADSHOT_UPLOAD_GUIDE.md`)
2. **Using cPanel File Manager**
3. **Using git hooks** (if GoDaddy supports it)

---

**Last Updated**: November 2025
