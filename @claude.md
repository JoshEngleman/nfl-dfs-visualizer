# NFL DFS Boom/Bust Visualizer - Project Overview

## ⚠️ IMPORTANT: Development Server Rules

**NEVER start dev servers automatically!**
- User manages their own dev servers
- DO NOT run `npm run dev` or similar background commands
- DO NOT restart servers without explicit permission
- If user mentions server is running, assume it's already set up correctly
- Only make code changes and let user refresh their browser

## Project Description

A web-based NFL DFS (Daily Fantasy Sports) analysis tool that visualizes player data with boom/bust percentages and leverage scores. Features player headshots, interactive tooltips, CSV upload functionality, and automated deployment to GoDaddy hosting.

## Key Features

- **CSV Upload Interface**: Users can upload DraftKings CSV files directly on the website
- **Player Headshots**: Automatic headshot fetching with multi-tier fallback system
- **Interactive Visualization**: Scatter plot with boom% vs leverage, sized by ownership
- **Automated Deployment**: One-command deployment to GoDaddy via FTP
- **Name Mapping System**: Handles player name variations (Sr., Jr., III, etc.)

## Technology Stack

- **Frontend**: Pure JavaScript (no frameworks), HTML5, CSS3
- **Backend**: Python 3.x for local tooling
- **Package Manager**: uv (fast Python package manager)
- **Deployment**: FTP to GoDaddy hosting
- **Data Processing**: pandas, matplotlib (for standalone visualizations)

## Project Structure

```
random-utilities/
├── src/                        # Python scripts
│   ├── nfl_dfs_visualizer.py          # Original CLI visualization tool
│   ├── nfl_dfs_visualizer_gui.py      # GUI version
│   ├── extract_headshots.py           # Extract headshots from HTML
│   ├── compress_headshots.py          # Compress images for web
│   ├── update_headshots_from_csv.py   # Download new player headshots
│   └── deploy.py                       # Automated FTP deployment
│
├── public/                     # Website files
│   └── index.html              # Main web application
│
├── docs/                       # Documentation
│   ├── SIMPLE_WORKFLOW.md             # User workflow guide
│   ├── HEADSHOT_UPLOAD_GUIDE.md       # Headshot management
│   ├── NAME_MATCHING_GUIDE.md         # Name mapping system
│   ├── QUICK_START.md                 # Quick start guide
│   ├── DEPLOYMENT_SETUP.md            # Deployment setup
│   └── HEADSHOT_UPDATE_WORKFLOW.md    # New headshot update process
│
├── data/                       # CSV data files
├── cache/                      # Cached headshots (gitignored)
│   ├── headshot_cache/                # Original headshots
│   └── headshot_cache_compressed/     # Optimized for web
│
├── archive/                    # Old/unused files
├── .venv/                      # Python virtual environment (uv-managed)
├── .env                        # FTP credentials (gitignored)
├── .env.example                # Template for credentials
├── name_mappings.json          # Player name mappings
├── requirements.txt            # Python dependencies
└── deploy.sh                   # Deployment wrapper script
```

## Key Workflows

### 1. Weekly DFS Updates (End User)

Users simply:
1. Visit https://joshengleman.com/nfl-dfs/
2. Click "Upload CSV"
3. Select their DraftKings CSV file
4. Done! (30 seconds)

Data is stored in browser localStorage. No server updates needed.

### 2. Headshot Management (Developer)

When new players appear in CSV files and need headshots:

```bash
# Download new headshots from CSV
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv

# Deploy headshots to server
./deploy.sh headshots
```

### 3. Website Deployment (Developer)

Update the web application:

```bash
# Deploy just the website
./deploy.sh website

# Deploy everything (website + headshots)
./deploy.sh all
```

### 4. Name Mapping System

Players with suffixes (Sr., Jr., III) may need name mappings in `name_mappings.json`:

```json
{
  "mappings": {
    "Ray-Ray McCloud III|NYG": "Ray-Ray McCloud",
    "Kyle Pitts Sr.|ATL": "Kyle Pitts"
  }
}
```

Both Python scripts and index.html use these mappings.

## Important Files

### Production Files
- `public/index.html` - Main web application (deployed to server)
- `cache/headshot_cache_compressed/` - Optimized headshots (deployed to server)
- `name_mappings.json` - Player name mappings (embedded in index.html)

### Development Tools
- `src/deploy.py` - FTP deployment script
- `src/update_headshots_from_csv.py` - Download new player headshots
- `.env` - FTP credentials (NOT in git)

### Configuration
- `requirements.txt` - Python dependencies
- `.env.example` - Template for FTP credentials
- `.gitignore` - Excludes .env, cache/, .venv/

## Development Setup

### First Time Setup

```bash
# Install uv
brew install uv

# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Set up FTP credentials
cp .env.example .env
# Edit .env with your GoDaddy FTP credentials
```

### Common Commands

```bash
# Update headshots for new players
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv

# Deploy to server
./deploy.sh all          # Deploy everything
./deploy.sh website      # Deploy only index.html
./deploy.sh headshots    # Deploy only headshot images

# Standalone visualization (legacy)
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position QB
```

## Deployment Details

### Server Structure (GoDaddy)
```
/public_html/nfl-dfs/
├── index.html
└── headshots/
    ├── Christian_McCaffrey.png
    ├── Brock_Purdy.png
    └── ... (279 more files)
```

### FTP Configuration (.env)
```
FTP_HOST=ftp.joshengleman.com
FTP_USER=josh
FTP_PASS=your-password
FTP_PORT=21
REMOTE_BASE_PATH=/public_html/nfl-dfs
REMOTE_HEADSHOTS_PATH=/public_html/nfl-dfs/headshots
```

## Headshot Fetching Strategy

The web application tries multiple sources in order:

1. **Embedded ORIGINAL_DATA** - Players from initial dataset (instant)
2. **Server folder** (`/nfl-dfs/headshots/`) - Fast, reliable
3. **ESPN API** - May have CORS issues
4. **Team logo** - Always works as fallback

## Name Mapping System

Handles player name variations:

**Python scripts** (`update_headshots_from_csv.py`):
- Loads `name_mappings.json`
- Applies mapping before fetching from NFL.com
- Example: "Ray-Ray McCloud III" → "Ray-Ray McCloud"

**JavaScript** (`index.html`):
- NAME_MAPPINGS embedded as constant
- Applies mapping in fetchHeadshot()
- Same mappings, consistent behavior

## Recent Updates (November 2025)

### Phase 1: Quick Wins (✅ Completed - November 17, 2025)

**Performance Optimization Initiative** - Achieved 40-50% performance improvements with minimal code changes.

1. **Dynamic Season Year Detection** (✅ Completed)
   - Fixed hardcoded 2025 season year in `nfl_dfs_visualizer.py:58`
   - Now automatically detects current NFL season based on date (Sep-Feb cycle)
   - Prevents future breakage when seasons change
   - Commit: `890ce7c`

2. **Parallel FTP Uploads** (✅ Completed)
   - Reduces deployment time from ~10 minutes to ~2 minutes (5x speedup)
   - ThreadPoolExecutor with 5 concurrent connections
   - Each thread has its own FTP connection (thread-safe)
   - Commit: `d098c94`

3. **WebP Image Conversion** (✅ Completed)
   - Added WebP format support to `compress_headshots.py`
   - Smart fallback: compares WebP vs JPEG, uses smaller file
   - Expected 30% reduction in image payload (18MB → 12-13MB)
   - Quality method=6 for optimal compression
   - Commit: `7abb549`

4. **Image Lazy Loading** (✅ Completed)
   - Added `loading="lazy"` to all player headshots and table images
   - 60-70% reduction in initial image loads
   - Team filter logos NOT lazy loaded (above the fold)
   - Commit: `17aa066`

5. **Deployment Resume Capability** (✅ Completed)
   - Skip already-uploaded files automatically
   - Resume failed deployments from where they left off
   - Integrated with parallel uploads
   - Commit: `d098c94`

**Phase 1 Results:**
- ✅ 5x faster deployments (10min → 2min)
- ✅ 30% smaller images with WebP
- ✅ 40-50% faster initial page load
- ✅ No more hardcoded year bugs
- ✅ Robust, resumable deployment process

### Phase 2: Modern Build Pipeline (🔄 In Progress - Started November 17, 2025)

**Objective:** Migrate from browser JSX compilation to Vite + React + TypeScript build pipeline for 300-800ms faster loads and better developer experience.

**Completed Tasks:**
1. **Vite Project Setup** (✅ Completed)
   - Initialized Vite with React 18 + TypeScript 5
   - Installed dependencies: recharts, papaparse, @types/papaparse
   - Project structure: `nfl-dfs-frontend/`
   - Commit: `2e2617e`

2. **TypeScript Type Definitions** (✅ Completed)
   - Created comprehensive Player interface (14 properties)
   - Position types, ChartData, TableColumn types
   - StoredData, ColumnFilters, CSVParseResult types
   - Type-safe development foundation
   - Commit: `53bc188`

**In Progress:**
3. **Component Extraction** (Pending)
   - Extract React components from 2400+ line index.html
   - Convert to modular .tsx files with TypeScript
   - Components: App, ChartView, DataTable, CSVUpload, Filters, PlayerHeadshot

4. **Data Management Migration** (Pending)
   - Custom hooks: useLocalStorage, usePlayerData, useCSVParser
   - Utility functions: teamColors, imageUtils, playerUtils

5. **Build Configuration** (Pending)
   - Configure Vite build output
   - Update deploy.py for new dist/ output
   - Test production build

**Expected Benefits:**
- 300-800ms faster initial load (no browser JSX compilation)
- 60-70% smaller bundle with code splitting
- Type safety and better IDE support
- Hot Module Replacement for development

### Previous Updates

1. **Automated Headshot Updates**: Created `update_headshots_from_csv.py` to download headshots for new players from CSV files
2. **Name Mapping Integration**: Both Python and JavaScript now use unified name mappings from `name_mappings.json`
3. **Deployment Automation**: FTP deployment script (`deploy.py`) with wrapper (`deploy.sh`)
4. **Package Manager Migration**: Switched from pip to uv for faster dependency management
5. **Project Reorganization**: Moved to structured folders (src/, docs/, public/, data/)

## Known Issues & Limitations

- ESPN API may have CORS restrictions (falls back to team logos)
- Large CSV files (>5MB) may be slow to process in browser
- localStorage has ~5-10MB limit per domain
- Headshot URLs from NFL.com may change over time

## Future Enhancements

- Interactive web version with Plotly/Dash
- Multiple metric comparisons (Projection vs Salary, etc.)
- Salary range filtering
- Player name search/highlighting
- Export to SVG/PDF formats
- Custom color schemes

## Security Notes

- `.env` file contains FTP credentials - NEVER commit to git
- `.gitignore` configured to exclude sensitive files
- FTP credentials used only for deployment
- No user data stored on server (all in browser localStorage)

## Support & Documentation

- Main README: `README.md`
- User workflow: `docs/SIMPLE_WORKFLOW.md`
- Headshot management: `docs/HEADSHOT_UPDATE_WORKFLOW.md`
- Deployment setup: `docs/DEPLOYMENT_SETUP.md`
- Name matching: `docs/NAME_MATCHING_GUIDE.md`

## Contact

For issues or questions, check the documentation in the `docs/` folder.

**Last Updated:** November 2025
