# NFL DFS Visualizer - Comprehensive Optimization Plan

**Project:** NFL DFS Boom/Bust Visualizer
**Analysis Date:** 2025-11-17
**Current Version:** Production (GoDaddy Hosted)
**Goal:** Achieve 70-80% performance improvement and modernize architecture

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Critical Issues Identified](#critical-issues-identified)
4. [Phase 1: Quick Wins](#phase-1-quick-wins-1-2-days)
5. [Phase 2: Modern Build Pipeline](#phase-2-modern-build-pipeline-2-3-days)
6. [Phase 3: Advanced Optimizations](#phase-3-advanced-optimizations-3-5-days)
7. [Phase 4: Professional Polish](#phase-4-professional-polish-2-3-days)
8. [Expected Outcomes](#expected-outcomes)
9. [Implementation Timeline](#implementation-timeline)
10. [Risk Assessment](#risk-assessment)

---

## Executive Summary

### Current Performance Metrics
- **HTML File Size:** 292KB (bloated, should be ~50KB)
- **Image Assets:** 18MB (300+ headshots)
- **Initial Load Time:** 2-5 seconds
- **Deployment Time:** 5-10 minutes (manual FTP)
- **CDN Requests:** 6 separate libraries
- **Build Process:** None (browser-based JSX compilation)

### Target Performance Metrics
- **HTML File Size:** ~50-80KB (bundled + minified)
- **Image Assets:** ~12MB (WebP conversion)
- **Initial Load Time:** 0.8-1.2 seconds
- **Deployment Time:** 30 seconds (automated Git push)
- **CDN Requests:** 2 (bundled JS + CSS)
- **Build Process:** Vite + React (pre-compiled)

### Overall Impact
- **70-80%** reduction in load time
- **60-70%** reduction in bundle size
- **95%** reduction in deployment time
- **100%** elimination of manual FTP uploads

---

## Current State Analysis

### Technology Stack
```
Frontend:
├── React 18 (CDN: unpkg.com)
├── Recharts 2.12.0 (CDN: unpkg.com)
├── Babel Standalone (browser JSX compilation)
├── PapaParse 5.4.1 (CSV parsing)
├── dom-to-image 2.6.0 (chart export)
└── Google Fonts (Outfit)

Backend/Processing:
├── Python 3.x
├── Pandas 2.0+
├── Pillow 10.0+
├── nfl-data-py 0.3.0
└── ftplib (deployment)

Hosting:
├── GoDaddy Shared Hosting
├── FTP Deployment
└── No CDN
```

### File Structure
```
random-utilities/
├── public/
│   └── index.html (292KB - BLOATED)
├── src/
│   ├── nfl_dfs_visualizer.py (2,360 lines)
│   ├── deploy.py (202 lines)
│   ├── compress_headshots.py (123 lines)
│   └── update_headshots_from_csv.py (288 lines)
├── cache/
│   ├── headshot_cache/ (1.2GB - original)
│   └── headshot_cache_compressed/ (18MB)
├── data/
├── docs/
└── requirements.txt
```

### Deployment Workflow
```
Current Process:
1. User downloads CSV from DraftKings
2. Run: python src/nfl_dfs_visualizer.py --csv data/file.csv
3. Generates: public/index.html (298KB)
4. Run: ./deploy.sh website
5. FTP upload to GoDaddy (5-10 minutes)
6. Manual browser cache clear for users

Issues:
❌ Manual, error-prone process
❌ No version control for deployed files
❌ No rollback capability
❌ Slow FTP uploads
❌ No CI/CD pipeline
```

---

## Critical Issues Identified

### 🔴 High Priority (Must Fix)

#### Issue #1: Browser-Based JSX Compilation
**Severity:** CRITICAL
**Impact:** 300-800ms overhead on EVERY page load
**Location:** `public/index.html:18`

```html
<!-- Current (BAD) -->
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
  // 2000+ lines of JSX compiled in browser
</script>
```

**Why This Is Bad:**
- Babel Standalone is 500KB+ (uncompressed)
- Parsing + compiling JSX adds 300-800ms
- No source maps for debugging
- No type checking
- Cannot use modern JS features safely

**Fix:** Pre-compile with Vite/webpack

---

#### Issue #2: Hardcoded 2025 Roster Year
**Severity:** CRITICAL (Will break in January 2025)
**Impact:** Headshot matching will fail
**Location:** `src/nfl_dfs_visualizer.py:58`

```python
# Current (BROKEN)
self.roster_cache = nfl.import_seasonal_rosters([2025])
```

**Fix:**
```python
import datetime
current_year = datetime.datetime.now().year
# Adjust for NFL season (starts Sep, ends Feb)
season_year = current_year if datetime.datetime.now().month >= 9 else current_year - 1
self.roster_cache = nfl.import_seasonal_rosters([season_year])
```

---

#### Issue #3: Massive Single HTML File
**Severity:** HIGH
**Impact:** Slow parsing, no code splitting, unmaintainable
**Location:** `src/nfl_dfs_visualizer.py:286-2343`

**Problems:**
- 2000+ lines of HTML generated as Python f-string
- No syntax highlighting or linting
- All code loaded even if user only views table
- No lazy loading of components
- Difficult to debug or modify

**Example of Current Mess:**
```python
def _generate_react_html(self, all_data: dict, positions: list, default_position: str) -> str:
    data_json = json.dumps(all_data)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- 2343 lines of HTML/CSS/JS as string -->
</head>
</html>"""
```

---

#### Issue #4: Sequential FTP Uploads
**Severity:** HIGH
**Impact:** 5-10 minute deployment times
**Location:** `src/deploy.py:135-139`

```python
# Current (SLOW)
for png_file in png_files:  # 300+ files
    if self.upload_file(png_file, png_file.name):
        uploaded += 1
    # Each upload: 1-3 seconds
```

**Impact:** Uploading 300 images × 2 seconds = 10 minutes

**Fix:** Parallel uploads with ThreadPoolExecutor

---

#### Issue #5: No Image Optimization Strategy
**Severity:** HIGH
**Impact:** 18MB payload, slow loads on mobile

**Current Issues:**
- ❌ No lazy loading (`loading="lazy"` attribute)
- ❌ No responsive images (`srcset`)
- ❌ PNG format (WebP is 25-35% smaller)
- ❌ No image CDN (served from same domain)
- ❌ No caching headers
- ❌ All images loaded upfront

---

### 🟡 Medium Priority (Should Fix)

#### Issue #6: Inefficient Roster Matching
**Severity:** MEDIUM
**Impact:** O(n²) complexity, slow HTML generation
**Location:** `src/nfl_dfs_visualizer.py:137-173`

```python
# Current: Multiple pandas queries per player
match = self.roster_cache[
    (self.roster_cache['player_name'] == player_name) &
    (self.roster_cache['team'] == team)
]
# Then fuzzy matching...
# Then another fuzzy matching...
```

**Problem:** For 100 players × 3000 roster entries = 300,000 comparisons

**Fix:** Pre-build lookup dictionary:
```python
def _build_roster_index(self):
    """Build O(1) lookup dictionary"""
    self.roster_index = {}
    for _, row in self.roster_cache.iterrows():
        key = f"{row['player_name']}|{row['team']}"
        self.roster_index[key] = row['headshot_url']
```

---

#### Issue #7: Synchronous Image Downloads
**Severity:** MEDIUM
**Impact:** 2-3 minute HTML generation for full slate
**Location:** `src/nfl_dfs_visualizer.py:93-110`

```python
# Current: Downloads one at a time
def _download_and_cache_image(self, url: str, filename: str):
    response = requests.get(url, timeout=10)  # BLOCKING
    # Process...
```

**Fix:** Use asyncio for parallel downloads:
```python
async def _download_images_parallel(self, urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = [self._fetch_image(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

---

#### Issue #8: Multiple CDN Dependencies
**Severity:** MEDIUM
**Impact:** 6 separate HTTP requests, DNS overhead
**Location:** `public/index.html:8-29`

```html
<!-- Current: 6 different CDNs -->
<script src="https://unpkg.com/react@18/..."></script>
<script src="https://unpkg.com/react-dom@18/..."></script>
<script src="https://unpkg.com/react-is@18/..."></script>
<script src="https://unpkg.com/prop-types/..."></script>
<script src="https://unpkg.com/recharts@2.12.0/..."></script>
<script src="https://unpkg.com/@babel/standalone/..."></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/..."></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/..."></script>
```

**Impact:**
- 6 DNS lookups
- 6 TCP connections
- 6 SSL handshakes
- Different CDN locations
- No HTTP/2 multiplexing benefits

---

### 🟢 Low Priority (Nice to Have)

#### Issue #9: No Error Boundaries
**Impact:** One error crashes entire app
**Fix:** Add React error boundaries

#### Issue #10: Magic Numbers Throughout
**Impact:** Hard to maintain configuration
**Fix:** Extract to config file

#### Issue #11: No Analytics
**Impact:** No visibility into user behavior
**Fix:** Add Plausible or Google Analytics

#### Issue #12: No Monitoring
**Impact:** Errors happen silently
**Fix:** Add Sentry.io

---

## PHASE 1: Quick Wins (1-2 Days)

**Goal:** 40-50% improvement with minimal code changes
**Effort:** Low
**Risk:** Low
**ROI:** ⭐⭐⭐⭐⭐

### Task 1.1: Fix Hardcoded Year Bug ✅
**Priority:** CRITICAL
**Estimated Time:** 30 minutes
**Files:** `src/nfl_dfs_visualizer.py`

**Implementation:**
```python
# Line 58: Update roster loading
def _load_roster_data(self):
    """Load NFL roster data for current season"""
    try:
        print("Loading NFL roster data...")
        import nfl_data_py as nfl
        import datetime

        # Determine current NFL season year
        current_date = datetime.datetime.now()
        current_year = current_date.year

        # NFL season starts in September and ends in February
        # If we're in Jan-Aug, use previous year's season
        if current_date.month < 9:
            season_year = current_year - 1
        else:
            season_year = current_year

        print(f"Loading {season_year} season roster data...")
        self.roster_cache = nfl.import_seasonal_rosters([season_year])
        print(f"Roster data loaded: {len(self.roster_cache)} players")
    except Exception as e:
        print(f"Warning: Could not load roster data: {e}")
        self.roster_cache = pd.DataFrame()
```

**Testing:**
```bash
# Test with current data
.venv/bin/python src/nfl_dfs_visualizer.py --csv data/NFL\ DK\ Boom\ Bust.csv --output test_output.html

# Verify roster year in console output
# Should see: "Loading 2024 season roster data..."
```

**Success Criteria:**
- [ ] No hardcoded year in code
- [ ] Automatically uses correct season
- [ ] Works in off-season (Jan-Aug)
- [ ] Headshots load successfully

---

### Task 1.2: Implement Parallel FTP Uploads ⚡
**Priority:** HIGH
**Estimated Time:** 2-3 hours
**Files:** `src/deploy.py`

**Implementation:**
```python
# Add to imports
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class DeploymentManager:
    def __init__(self):
        self.ftp = None
        self.project_root = project_root
        self.upload_lock = threading.Lock()

    def upload_file_thread_safe(self, local_path, remote_filename):
        """Thread-safe file upload"""
        with self.upload_lock:
            # Create new FTP connection for this thread
            ftp = FTP()
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USER, FTP_PASS)
            ftp.cwd(REMOTE_HEADSHOTS_PATH)

            try:
                with open(local_path, 'rb') as file:
                    ftp.storbinary(f'STOR {remote_filename}', file)
                file_size = os.path.getsize(local_path)
                ftp.quit()
                return True, local_path.name, file_size
            except Exception as e:
                ftp.quit()
                return False, local_path.name, str(e)

    def deploy_headshots_parallel(self, max_workers=5):
        """Upload headshots in parallel"""
        print("\n📸 Deploying headshots (parallel mode)...")

        headshots_dir = self.project_root / 'cache' / 'headshot_cache_compressed'
        if not headshots_dir.exists():
            print(f"   ❌ Directory not found: {headshots_dir}")
            return False

        png_files = list(headshots_dir.glob('*.png'))
        if not png_files:
            print(f"   ❌ No PNG files found")
            return False

        print(f"   Found {len(png_files)} headshots to upload")
        print(f"   Using {max_workers} parallel connections")

        # Ensure directory exists
        self.ensure_directory(REMOTE_HEADSHOTS_PATH)

        uploaded = 0
        failed = 0

        # Upload in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.upload_file_thread_safe, png_file, png_file.name): png_file
                for png_file in png_files
            }

            for future in as_completed(futures):
                success, filename, result = future.result()
                if success:
                    print(f"   ✅ Uploaded {filename} ({result:,} bytes)")
                    uploaded += 1
                else:
                    print(f"   ❌ Failed {filename}: {result}")
                    failed += 1

        print(f"\n   📊 Results: {uploaded} uploaded, {failed} failed")
        return failed == 0
```

**Testing:**
```bash
# Test parallel upload
./deploy.sh headshots

# Time comparison:
# Before: ~10 minutes for 300 files
# After: ~2 minutes for 300 files (5x speedup)
```

**Success Criteria:**
- [ ] Uploads complete in <3 minutes
- [ ] No file corruption
- [ ] Proper error handling
- [ ] Progress reporting works

---

### Task 1.3: Convert Images to WebP 🖼️
**Priority:** HIGH
**Estimated Time:** 2 hours
**Files:** `src/compress_headshots.py`

**Implementation:**
```python
def compress_headshots(input_dir, output_dir, max_size=400, quality=85, use_webp=True):
    """
    Compress headshot images for web use.
    Now supports WebP format for better compression.
    """
    # ... existing code ...

    for img_file in png_files:
        try:
            # ... existing resize code ...

            # Choose output format
            if use_webp:
                # Save as WebP (25-35% smaller than JPEG)
                output_file = output_path / img_file.stem
                output_file = output_file.with_suffix('.webp')
                img.save(output_file, 'WEBP', quality=quality, method=6)

                compressed_size = output_file.stat().st_size

                # Fallback to JPEG if WebP fails or is larger
                if compressed_size > 150_000:
                    jpeg_file = output_path / img_file.stem
                    jpeg_file = jpeg_file.with_suffix('.jpg')
                    img.save(jpeg_file, 'JPEG', quality=quality, optimize=True)

                    # Use whichever is smaller
                    jpeg_size = jpeg_file.stat().st_size
                    if jpeg_size < compressed_size:
                        output_file.unlink()
                        output_file = jpeg_file
                        compressed_size = jpeg_size
                    else:
                        jpeg_file.unlink()
            else:
                # Original PNG/JPEG logic
                # ... existing code ...
```

**Update HTML to support WebP with fallback:**
```html
<picture>
  <source srcset="headshots/player_name.webp" type="image/webp">
  <source srcset="headshots/player_name.jpg" type="image/jpeg">
  <img src="headshots/player_name.jpg" alt="Player Name" loading="lazy">
</picture>
```

**Expected Savings:**
- Current: 18MB (PNG/JPEG)
- After WebP: ~12-13MB (30% reduction)

**Success Criteria:**
- [ ] WebP files generated successfully
- [ ] Fallback to JPEG for old browsers
- [ ] File size reduced by 25-35%
- [ ] No visual quality loss

---

### Task 1.4: Add Image Lazy Loading 🚀
**Priority:** MEDIUM
**Estimated Time:** 30 minutes
**Files:** `public/index.html` or React components

**Implementation:**
```javascript
// In React components, update all <img> tags
<img
  src={player.headshot_url}
  className="player-headshot"
  alt={player.player_name}
  loading="lazy"  // ← ADD THIS
  onError={(e) => { e.target.style.display = 'none'; }}
/>

// For team logos
<img
  src={getTeamLogoUrl(player.team_abbr)}
  className="team-logo"
  alt={player.team_abbr}
  loading="lazy"  // ← ADD THIS
/>
```

**Impact:**
- Only loads images as user scrolls
- Reduces initial page load by 60-70%
- Improves Time to Interactive (TTI)

**Success Criteria:**
- [ ] Images below fold don't load immediately
- [ ] Smooth loading as user scrolls
- [ ] Works on mobile devices
- [ ] No layout shift

---

### Task 1.5: Add Deployment Resume Capability 🔄
**Priority:** MEDIUM
**Estimated Time:** 1 hour
**Files:** `src/deploy.py`

**Implementation:**
```python
def get_remote_file_list(self, remote_dir):
    """Get list of files already on server"""
    try:
        self.ftp.cwd(remote_dir)
        file_list = []
        self.ftp.retrlines('NLST', file_list.append)
        return set(file_list)
    except:
        return set()

def deploy_headshots_parallel(self, max_workers=5, skip_existing=True):
    """Upload headshots in parallel with resume capability"""

    # ... existing setup code ...

    # Get list of files already on server
    if skip_existing:
        print("   Checking existing files on server...")
        remote_files = self.get_remote_file_list(REMOTE_HEADSHOTS_PATH)
        print(f"   Found {len(remote_files)} files already uploaded")

        # Filter out files that already exist
        files_to_upload = [f for f in png_files if f.name not in remote_files]
        print(f"   Will upload {len(files_to_upload)} new/updated files")
    else:
        files_to_upload = png_files

    # ... rest of upload logic ...
```

**Success Criteria:**
- [ ] Skips files already uploaded
- [ ] Can resume after network failure
- [ ] Progress tracking works
- [ ] Option to force re-upload all

---

### Phase 1 Summary

**Total Time:** 1-2 days
**Total Tasks:** 5

**Expected Results:**
- ✅ No more hardcoded year bugs
- ✅ 5x faster deployments (10min → 2min)
- ✅ 30% smaller images (18MB → 13MB)
- ✅ 40-50% faster initial page load
- ✅ Robust deployment process

**Deployment Checklist:**
- [ ] All code changes tested locally
- [ ] Backup current production files
- [ ] Deploy to production
- [ ] Verify headshots load correctly
- [ ] Test on mobile devices
- [ ] Monitor for errors

---

## PHASE 2: Modern Build Pipeline (2-3 Days)

**Goal:** Eliminate browser JSX compilation, proper bundling
**Effort:** Medium
**Risk:** Medium
**ROI:** ⭐⭐⭐⭐⭐

### Task 2.1: Initialize Vite + React Project 🏗️
**Priority:** HIGH
**Estimated Time:** 3-4 hours
**New Structure:** Complete rewrite of frontend

**Step 1: Create New Vite Project**
```bash
# Create new directory for frontend
mkdir nfl-dfs-frontend
cd nfl-dfs-frontend

# Initialize Vite with React + TypeScript
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install

# Install additional packages
npm install recharts papaparse
npm install @types/papaparse --save-dev
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Step 2: New Project Structure**
```
nfl-dfs-frontend/
├── public/
│   └── headshots/           # Symlink to ../cache/headshot_cache_compressed
├── src/
│   ├── components/
│   │   ├── Chart/
│   │   │   ├── ChartView.tsx
│   │   │   ├── PlayerHeadshot.tsx
│   │   │   └── ChartFilters.tsx
│   │   ├── DataTable/
│   │   │   ├── DataTable.tsx
│   │   │   ├── ColumnFilter.tsx
│   │   │   └── Pagination.tsx
│   │   ├── Upload/
│   │   │   ├── CSVUpload.tsx
│   │   │   └── DataManager.tsx
│   │   └── Layout/
│   │       ├── Header.tsx
│   │       ├── TabNavigation.tsx
│   │       └── Footer.tsx
│   ├── hooks/
│   │   ├── useChartData.ts
│   │   ├── useFilters.ts
│   │   └── useCSVParser.ts
│   ├── types/
│   │   └── player.ts
│   ├── utils/
│   │   ├── teamColors.ts
│   │   ├── playerUtils.ts
│   │   └── imageUtils.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

**Step 3: Configure Vite**
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true,
    })
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'recharts-vendor': ['recharts'],
          'utils': ['papaparse']
        }
      }
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
})
```

**Success Criteria:**
- [ ] Vite dev server runs successfully
- [ ] TypeScript compilation works
- [ ] Hot module replacement (HMR) works
- [ ] Build produces optimized bundle

---

### Task 2.2: Migrate React Components to TypeScript 📝
**Priority:** HIGH
**Estimated Time:** 6-8 hours
**Files:** Extract from `public/index.html` → separate `.tsx` files

**Create Type Definitions:**
```typescript
// src/types/player.ts
export interface Player {
  player_id: string;
  player_name: string;
  position: 'QB' | 'RB' | 'WR' | 'TE' | 'DST';
  team_abbr: string;
  salary: number;
  dk_projection: number;
  std_dev: number;
  ceiling: number;
  bust_pct: number;
  boom_pct: number;
  ownership_pct: number;
  optimal_pct: number;
  leverage: number;
  headshot_url: string;
}

export interface ChartData extends Player {
  x: number;
  y: number;
  rawSize: number;
  color: string;
  intensity: number;
}

export type StatKey = keyof Pick<Player,
  'boom_pct' | 'bust_pct' | 'leverage' | 'ownership_pct' |
  'optimal_pct' | 'salary' | 'dk_projection' | 'std_dev' | 'ceiling'
>;

export interface StatOption {
  value: StatKey;
  label: string;
}

export interface FilterState {
  selectedPositions: string[];
  selectedTeams: string[];
  salaryRange: [number, number];
  ownershipRange: [number, number];
}
```

**Extract Chart Component:**
```typescript
// src/components/Chart/ChartView.tsx
import React, { useState, useEffect, useMemo } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceArea,
} from 'recharts';
import { Player, ChartData, StatKey, FilterState } from '../../types/player';
import { PlayerHeadshot } from './PlayerHeadshot';
import { ChartFilters } from './ChartFilters';

interface ChartViewProps {
  players: Player[];
}

export const ChartView: React.FC<ChartViewProps> = ({ players }) => {
  const [xAxisStat, setXAxisStat] = useState<StatKey>('boom_pct');
  const [yAxisStat, setYAxisStat] = useState<StatKey>('leverage');
  const [sizeStat, setSizeStat] = useState<StatKey>('ownership_pct');

  const [filters, setFilters] = useState<FilterState>({
    selectedPositions: ['QB'],
    selectedTeams: [],
    salaryRange: [3000, 12000],
    ownershipRange: [0, 100],
  });

  // ... rest of component logic ...

  return (
    <div className="chart-view">
      <ChartFilters
        filters={filters}
        onChange={setFilters}
        xAxisStat={xAxisStat}
        yAxisStat={yAxisStat}
        sizeStat={sizeStat}
        onXAxisChange={setXAxisStat}
        onYAxisChange={setYAxisStat}
        onSizeChange={setSizeStat}
      />

      <ResponsiveContainer width="100%" height={700}>
        <ScatterChart>
          {/* Chart implementation */}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};
```

**Extract Data Table Component:**
```typescript
// src/components/DataTable/DataTable.tsx
import React, { useState, useMemo } from 'react';
import { Player } from '../../types/player';
import { ColumnFilter } from './ColumnFilter';
import { Pagination } from './Pagination';

interface DataTableProps {
  players: Player[];
}

export const DataTable: React.FC<DataTableProps> = ({ players }) => {
  // ... table logic ...
};
```

**Success Criteria:**
- [ ] All components type-checked
- [ ] No `any` types used
- [ ] Props properly typed
- [ ] IDE autocomplete works

---

### Task 2.3: Implement Code Splitting & Lazy Loading 🚀
**Priority:** MEDIUM
**Estimated Time:** 2 hours
**Files:** `src/App.tsx`

**Implementation:**
```typescript
// src/App.tsx
import React, { lazy, Suspense, useState } from 'react';
import { Header } from './components/Layout/Header';
import { TabNavigation } from './components/Layout/TabNavigation';
import { CSVUpload } from './components/Upload/CSVUpload';
import { Player } from './types/player';

// Lazy load heavy components
const ChartView = lazy(() => import('./components/Chart/ChartView'));
const DataTable = lazy(() => import('./components/DataTable/DataTable'));

// Loading fallback
const LoadingSpinner = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Loading...</p>
  </div>
);

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chart' | 'table'>('chart');
  const [players, setPlayers] = useState<Player[]>([]);

  return (
    <div className="app-container">
      <Header />

      <CSVUpload onDataLoaded={setPlayers} />

      <TabNavigation activeTab={activeTab} onChange={setActiveTab} />

      <Suspense fallback={<LoadingSpinner />}>
        {activeTab === 'chart' ? (
          <ChartView players={players} />
        ) : (
          <DataTable players={players} />
        )}
      </Suspense>
    </div>
  );
};
```

**Bundle Analysis:**
```bash
# Build and analyze bundle
npm run build

# Check bundle sizes
ls -lh dist/assets/

# Expected output:
# index-abc123.js      ~80KB (main bundle)
# react-vendor-xyz.js  ~130KB (React + React DOM)
# recharts-vendor.js   ~180KB (Recharts)
# utils-def456.js      ~20KB (PapaParse)
```

**Success Criteria:**
- [ ] Chart and Table in separate chunks
- [ ] Total JS < 450KB (vs 2MB+ current)
- [ ] Initial load only loads active tab
- [ ] Lazy loading works smoothly

---

### Task 2.4: Setup Tailwind CSS 🎨
**Priority:** MEDIUM
**Estimated Time:** 2 hours
**Benefit:** Smaller CSS, better maintainability

**Configure Tailwind:**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nfl': {
          'qb': '#dc2626',
          'rb': '#059669',
          'wr': '#3b82f6',
          'te': '#d97706',
          'dst': '#6b7280',
        }
      },
      fontFamily: {
        'outfit': ['Outfit', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

**Benefits:**
- Current CSS: ~50KB inline styles
- After Tailwind: ~10-15KB (purged)
- Better maintainability
- Consistent design system

**Success Criteria:**
- [ ] CSS size reduced by 70%
- [ ] No unused CSS in production
- [ ] Design matches current version
- [ ] Mobile responsive works

---

### Task 2.5: Update Python Script to Generate JSON 📊
**Priority:** HIGH
**Estimated Time:** 2 hours
**Files:** `src/nfl_dfs_visualizer.py`

**Goal:** Instead of generating HTML, generate JSON data

**New Script:**
```python
# src/generate_data.py
#!/usr/bin/env python3
"""
Generate JSON data for NFL DFS Visualizer frontend.
Replaces HTML generation with pure data export.
"""

import json
from pathlib import Path
from nfl_dfs_visualizer import NFLDFSVisualizer

def generate_json_data(csv_path: str, output_path: str = 'data.json'):
    """Generate JSON data file for frontend"""

    visualizer = NFLDFSVisualizer(csv_path)

    # Prepare data for all positions
    all_data = {}
    positions = ['ALL'] + sorted(visualizer.df['Position'].unique().tolist())

    for pos in positions:
        all_data[pos] = visualizer.prepare_data_for_position(pos)

    # Export as JSON
    output = {
        'generated_at': datetime.datetime.now().isoformat(),
        'source_file': csv_path,
        'positions': positions,
        'data': all_data,
        'metadata': {
            'total_players': len(visualizer.df),
            'season_year': visualizer.season_year
        }
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Generated {output_path}")
    print(f"   File size: {Path(output_path).stat().st_size / 1024:.1f} KB")

    return output_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--output', default='public/data.json')
    args = parser.parse_args()

    generate_json_data(args.csv, args.output)
```

**Frontend Data Loading:**
```typescript
// src/hooks/usePlayerData.ts
import { useEffect, useState } from 'react';
import { Player } from '../types/player';

export const usePlayerData = () => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/data.json')
      .then(res => res.json())
      .then(data => {
        setPlayers(data.data.ALL);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { players, loading, error };
};
```

**Success Criteria:**
- [ ] JSON file generated successfully
- [ ] Frontend loads data correctly
- [ ] File size < 200KB
- [ ] All player data preserved

---

### Phase 2 Summary

**Total Time:** 2-3 days
**Total Tasks:** 5

**Expected Results:**
- ✅ No browser JSX compilation (300-800ms saved)
- ✅ Bundle size reduced 60-70% (292KB → 100KB)
- ✅ Code splitting enabled
- ✅ Type safety with TypeScript
- ✅ Modern development experience
- ✅ 10x faster builds

**Before vs After:**
```
BEFORE:
- index.html: 292KB
- 6 CDN libraries: ~2MB
- Browser JSX compilation: 300-800ms
- Total load time: 2-5 seconds

AFTER:
- main.js: 80KB
- react-vendor.js: 130KB (cached)
- recharts-vendor.js: 180KB (cached)
- Total load time: 0.8-1.2 seconds
```

---

## PHASE 3: Advanced Optimizations (3-5 Days)

**Goal:** Production-grade performance and deployment
**Effort:** Medium-High
**Risk:** Medium
**ROI:** ⭐⭐⭐⭐

### Task 3.1: Migrate to Vercel Hosting 🚀
**Priority:** HIGH
**Estimated Time:** 4 hours
**Impact:** Eliminates FTP, adds CDN, enables CI/CD

**Step 1: Prepare Git Repository**
```bash
# Ensure clean git state
git status
git add .
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository (if not exists)
gh repo create nfl-dfs-visualizer --public --source=. --remote=origin
git push -u origin main
```

**Step 2: Configure Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Initialize project
cd nfl-dfs-frontend
vercel init

# Configure build settings
vercel --prod
```

**Vercel Configuration:**
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/headshots/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=2592000"
        }
      ]
    }
  ]
}
```

**Step 3: Update DNS (Keep GoDaddy Domain)**
```
1. Log into GoDaddy DNS management
2. Update A record:
   - Type: A
   - Name: @
   - Value: 76.76.21.21 (Vercel IP)

3. Add CNAME record:
   - Type: CNAME
   - Name: www
   - Value: cname.vercel-dns.com
```

**Step 4: Configure Custom Domain in Vercel**
```bash
vercel domains add joshengleman.com
vercel domains add www.joshengleman.com
```

**New Deployment Workflow:**
```bash
# Old (FTP):
./deploy.sh all          # 10 minutes
# Manual cache clear
# Manual verification

# New (Git + Vercel):
git add .
git commit -m "Update data"
git push                 # 30 seconds
# Auto-deploy
# Auto-invalidate cache
# Auto-preview URLs
```

**Success Criteria:**
- [ ] Site deployed to Vercel
- [ ] Custom domain working
- [ ] SSL certificate active
- [ ] Automatic deployments on push
- [ ] Preview deployments for PRs

---

### Task 3.2: Implement Image CDN (Cloudinary) 🖼️
**Priority:** HIGH
**Estimated Time:** 3 hours
**Impact:** Global CDN, automatic optimization

**Step 1: Setup Cloudinary Account**
```bash
# Sign up: https://cloudinary.com (Free tier: 25GB/month)
# Get credentials: Cloud name, API key, API secret
```

**Step 2: Upload Images to Cloudinary**
```python
# src/upload_to_cloudinary.py
import cloudinary
import cloudinary.uploader
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_headshots():
    """Upload all headshots to Cloudinary"""
    headshots_dir = Path('cache/headshot_cache_compressed')

    for img_file in headshots_dir.glob('*.png'):
        player_name = img_file.stem

        # Upload with transformations
        result = cloudinary.uploader.upload(
            str(img_file),
            folder='nfl-dfs/headshots',
            public_id=player_name,
            resource_type='image',
            format='webp',  # Auto-convert to WebP
            quality='auto',  # Auto-optimize quality
            fetch_format='auto',  # Serve best format
            responsive=True,
            transformation=[
                {'width': 400, 'height': 400, 'crop': 'fill'},
                {'quality': 'auto:good'},
                {'fetch_format': 'auto'}
            ]
        )

        print(f"✅ Uploaded: {player_name} -> {result['secure_url']}")

if __name__ == '__main__':
    upload_headshots()
```

**Step 3: Update Frontend to Use Cloudinary URLs**
```typescript
// src/utils/imageUtils.ts
const CLOUDINARY_BASE = 'https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload';

export const getHeadshotUrl = (playerName: string, teamAbbr: string): string => {
  const cleanName = playerName.replace(/[^a-zA-Z0-9]/g, '_');

  // Cloudinary with automatic optimization
  return `${CLOUDINARY_BASE}/f_auto,q_auto,w_400,h_400,c_fill/nfl-dfs/headshots/${cleanName}`;
};

export const getResponsiveHeadshotUrls = (playerName: string) => {
  const cleanName = playerName.replace(/[^a-zA-Z0-9]/g, '_');
  const base = `${CLOUDINARY_BASE}/nfl-dfs/headshots/${cleanName}`;

  return {
    '1x': `${base}/f_auto,q_auto,w_200,h_200,c_fill`,
    '2x': `${base}/f_auto,q_auto,w_400,h_400,c_fill`,
    '3x': `${base}/f_auto,q_auto,w_600,h_600,c_fill`,
  };
};
```

**Step 4: Implement Responsive Images**
```tsx
// Component usage
<img
  src={getHeadshotUrl(player.player_name, player.team_abbr)}
  srcSet={`
    ${getResponsiveHeadshotUrls(player.player_name)['1x']} 1x,
    ${getResponsiveHeadshotUrls(player.player_name)['2x']} 2x,
    ${getResponsiveHeadshotUrls(player.player_name)['3x']} 3x
  `}
  alt={player.player_name}
  loading="lazy"
/>
```

**Benefits:**
- Global CDN (faster worldwide)
- Automatic WebP/AVIF conversion
- Responsive images
- Image transformations on-the-fly
- No server bandwidth usage

**Success Criteria:**
- [ ] All images uploaded to Cloudinary
- [ ] URLs updated in code
- [ ] Images load from CDN
- [ ] WebP served to modern browsers
- [ ] Responsive images work

---

### Task 3.3: Implement Service Worker + PWA 📱
**Priority:** MEDIUM
**Estimated Time:** 4 hours
**Impact:** Offline support, faster repeat visits

**Step 1: Generate Service Worker**
```bash
npm install -D vite-plugin-pwa
```

**Step 2: Configure PWA**
```typescript
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'NFL DFS Boom/Bust Analyzer',
        short_name: 'NFL DFS',
        description: 'Visualize DraftKings player data with boom/bust analysis',
        theme_color: '#3b82f6',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/res\.cloudinary\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'cloudinary-images',
              expiration: {
                maxEntries: 500,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          }
        ]
      }
    })
  ]
})
```

**Step 3: Add Install Prompt**
```typescript
// src/components/Layout/InstallPrompt.tsx
import React, { useEffect, useState } from 'react';

export const InstallPrompt: React.FC = () => {
  const [installPrompt, setInstallPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setInstallPrompt(e);
      setShowPrompt(true);
    };

    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstall = async () => {
    if (!installPrompt) return;

    installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;

    if (outcome === 'accepted') {
      setShowPrompt(false);
    }
  };

  if (!showPrompt) return null;

  return (
    <div className="install-prompt">
      <p>Install NFL DFS Analyzer for quick access!</p>
      <button onClick={handleInstall}>Install</button>
      <button onClick={() => setShowPrompt(false)}>Dismiss</button>
    </div>
  );
};
```

**Success Criteria:**
- [ ] Service worker registered
- [ ] App works offline (with cached data)
- [ ] Install prompt appears
- [ ] App installable on mobile
- [ ] Repeat visits load from cache

---

### Task 3.4: Add GitHub Actions CI/CD 🤖
**Priority:** MEDIUM
**Estimated Time:** 2 hours
**Impact:** Automated testing and deployment

**Create Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build

  deploy-preview:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel Preview
        run: vercel deploy --token=${{ secrets.VERCEL_TOKEN }}

  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel Production
        run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

**Add Data Generation Workflow:**
```yaml
# .github/workflows/generate-data.yml
name: Generate Data

on:
  workflow_dispatch:
    inputs:
      csv_url:
        description: 'CSV file URL'
        required: true

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Download CSV
        run: |
          curl -o data/input.csv ${{ github.event.inputs.csv_url }}

      - name: Generate JSON data
        run: |
          python src/generate_data.py --csv data/input.csv --output nfl-dfs-frontend/public/data.json

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add nfl-dfs-frontend/public/data.json
          git commit -m "Update data: $(date)"
          git push
```

**Success Criteria:**
- [ ] Tests run on every PR
- [ ] Automatic preview deployments
- [ ] Production deploys on merge to main
- [ ] Data generation workflow works

---

### Phase 3 Summary

**Total Time:** 3-5 days
**Total Tasks:** 4

**Expected Results:**
- ✅ No more FTP deployments (30 second Git push)
- ✅ Global CDN for images (faster worldwide)
- ✅ Offline support (PWA)
- ✅ Automated CI/CD pipeline
- ✅ Preview deployments for testing

**Deployment Workflow Transformation:**
```
BEFORE:
1. Edit code locally
2. Generate HTML (2-3 min)
3. FTP upload (10 min)
4. Manually clear cache
5. Hope nothing broke
Total: ~15 minutes

AFTER:
1. Edit code locally
2. git commit && git push
3. Automatic build + test + deploy
4. Automatic cache invalidation
5. Preview URL for testing
Total: ~30 seconds
```

---

## PHASE 4: Professional Polish (2-3 Days)

**Goal:** Production monitoring, analytics, testing
**Effort:** Medium
**Risk:** Low
**ROI:** ⭐⭐⭐

### Task 4.1: Add Analytics (Plausible) 📊
**Priority:** MEDIUM
**Estimated Time:** 1 hour
**Impact:** Understand user behavior

**Setup:**
```typescript
// src/utils/analytics.ts
export const trackEvent = (eventName: string, props?: Record<string, any>) => {
  if (typeof window !== 'undefined' && (window as any).plausible) {
    (window as any).plausible(eventName, { props });
  }
};

// Track chart interactions
export const trackChartZoom = () => trackEvent('Chart Zoom');
export const trackFilterChange = (filterType: string) =>
  trackEvent('Filter Change', { type: filterType });
export const trackCSVUpload = () => trackEvent('CSV Upload');
export const trackExport = (format: string) =>
  trackEvent('Export', { format });
```

**Add to HTML:**
```html
<!-- Add to index.html -->
<script defer data-domain="joshengleman.com" src="https://plausible.io/js/script.js"></script>
```

**Track Key Events:**
- Page views
- CSV uploads
- Filter changes
- Chart zooms
- Tab switches
- Export downloads

**Success Criteria:**
- [ ] Analytics script loaded
- [ ] Events tracked correctly
- [ ] Dashboard shows data
- [ ] GDPR compliant (Plausible is)

---

### Task 4.2: Add Error Tracking (Sentry) 🐛
**Priority:** MEDIUM
**Estimated Time:** 2 hours
**Impact:** Catch and fix bugs proactively

**Setup Sentry:**
```bash
npm install @sentry/react @sentry/tracing
```

**Configure:**
```typescript
// src/main.tsx
import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [new BrowserTracing()],
  tracesSampleRate: 0.1,
  environment: import.meta.env.MODE,
  beforeSend(event, hint) {
    // Don't send errors in development
    if (import.meta.env.DEV) return null;
    return event;
  }
});
```

**Add Error Boundaries:**
```typescript
// src/components/ErrorBoundary.tsx
import React from 'react';
import * as Sentry from '@sentry/react';

const ErrorFallback: React.FC<{ error: Error }> = ({ error }) => (
  <div className="error-boundary">
    <h2>Oops! Something went wrong</h2>
    <p>We've been notified and will fix this soon.</p>
    <button onClick={() => window.location.reload()}>
      Reload Page
    </button>
  </div>
);

export const ErrorBoundary = Sentry.withErrorBoundary(
  ({ children }) => <>{children}</>,
  { fallback: ErrorFallback }
);
```

**Wrap App:**
```typescript
// src/main.tsx
root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
```

**Success Criteria:**
- [ ] Sentry captures errors
- [ ] Source maps uploaded
- [ ] Error notifications configured
- [ ] Performance monitoring enabled

---

### Task 4.3: Add Loading States & Skeletons ⏳
**Priority:** LOW
**Estimated Time:** 3 hours
**Impact:** Better perceived performance

**Create Skeleton Components:**
```typescript
// src/components/Skeletons/ChartSkeleton.tsx
export const ChartSkeleton: React.FC = () => (
  <div className="chart-skeleton animate-pulse">
    <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
    <div className="h-96 bg-gray-100 rounded"></div>
  </div>
);

// src/components/Skeletons/TableSkeleton.tsx
export const TableSkeleton: React.FC = () => (
  <div className="table-skeleton animate-pulse">
    <div className="h-12 bg-gray-200 rounded mb-2"></div>
    {[...Array(10)].map((_, i) => (
      <div key={i} className="h-16 bg-gray-100 rounded mb-1"></div>
    ))}
  </div>
);
```

**Use in Components:**
```typescript
const ChartView: React.FC = ({ players }) => {
  const [loading, setLoading] = useState(true);

  if (loading) return <ChartSkeleton />;

  return <ScatterChart>...</ScatterChart>;
};
```

**Success Criteria:**
- [ ] Skeletons match final layout
- [ ] Smooth transitions
- [ ] No layout shift
- [ ] Works on slow connections

---

### Task 4.4: Add Unit & E2E Tests 🧪
**Priority:** MEDIUM
**Estimated Time:** 6 hours
**Impact:** Prevent regressions

**Setup Testing:**
```bash
# Install testing libraries
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D @playwright/test
```

**Unit Tests:**
```typescript
// src/utils/__tests__/playerUtils.test.ts
import { describe, it, expect } from 'vitest';
import { filterPlayersByPosition, calculateQuadrant } from '../playerUtils';

describe('playerUtils', () => {
  it('filters players by position', () => {
    const players = [
      { position: 'QB', name: 'Player 1' },
      { position: 'RB', name: 'Player 2' },
    ];

    const result = filterPlayersByPosition(players, ['QB']);
    expect(result).toHaveLength(1);
    expect(result[0].position).toBe('QB');
  });

  it('calculates quadrant correctly', () => {
    const quadrant = calculateQuadrant(50, 5, 40, 0);
    expect(quadrant).toBe('green'); // High boom, positive leverage
  });
});
```

**Component Tests:**
```typescript
// src/components/__tests__/ChartFilters.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ChartFilters } from '../Chart/ChartFilters';

describe('ChartFilters', () => {
  it('renders position filters', () => {
    render(<ChartFilters {...mockProps} />);
    expect(screen.getByText('QB')).toBeInTheDocument();
    expect(screen.getByText('RB')).toBeInTheDocument();
  });

  it('calls onChange when position clicked', () => {
    const onChange = vi.fn();
    render(<ChartFilters onChange={onChange} {...mockProps} />);

    fireEvent.click(screen.getByText('RB'));
    expect(onChange).toHaveBeenCalled();
  });
});
```

**E2E Tests:**
```typescript
// e2e/chart.spec.ts
import { test, expect } from '@playwright/test';

test('loads chart view', async ({ page }) => {
  await page.goto('/');

  // Should show chart by default
  await expect(page.locator('.chart-view')).toBeVisible();

  // Should have position filters
  await expect(page.locator('.position-toggle')).toHaveCount(6);
});

test('switches to table view', async ({ page }) => {
  await page.goto('/');

  await page.click('text=Data Table');

  await expect(page.locator('.data-table')).toBeVisible();
});

test('filters by position', async ({ page }) => {
  await page.goto('/');

  // Click RB filter
  await page.click('.position-toggle.position-RB');

  // Should only show RB players
  const players = await page.locator('.player-headshot').count();
  expect(players).toBeGreaterThan(0);
});
```

**Add to package.json:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

**Success Criteria:**
- [ ] 80%+ code coverage
- [ ] All critical paths tested
- [ ] E2E tests pass
- [ ] Tests run in CI

---

### Phase 4 Summary

**Total Time:** 2-3 days
**Total Tasks:** 4

**Expected Results:**
- ✅ Analytics tracking user behavior
- ✅ Error monitoring and alerts
- ✅ Better loading UX
- ✅ Test coverage for stability

---

## Expected Outcomes

### Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Initial Load Time** | 2-5s | 0.8-1.2s | **70-80%** |
| **HTML Size** | 292KB | 50-80KB | **72%** |
| **Total JS Size** | ~2MB | ~450KB | **77%** |
| **Image Payload** | 18MB | 12MB (WebP) | **33%** |
| **CDN Requests** | 6 | 2 | **67%** |
| **Deployment Time** | 10min | 30s | **95%** |
| **Time to Interactive** | 3-6s | 1-1.5s | **75%** |
| **Lighthouse Score** | 60-70 | 95-100 | **35%** |

### Developer Experience

| Aspect | Before | After |
|--------|--------|-------|
| **Deployment** | Manual FTP | Git push |
| **Build Time** | N/A | ~30s |
| **Type Safety** | None | TypeScript |
| **Testing** | Manual | Automated |
| **Error Tracking** | None | Sentry |
| **Previews** | None | Auto PR previews |
| **Rollbacks** | Manual | One-click |

### User Experience

| Improvement | Impact |
|-------------|--------|
| **Faster loads** | Less bounce rate |
| **Offline support** | Works anywhere |
| **PWA install** | App-like experience |
| **Better mobile** | Responsive images |
| **Loading states** | Less frustration |
| **Error recovery** | Graceful failures |

---

## Implementation Timeline

### Week 1: Foundation
- **Days 1-2:** Phase 1 (Quick Wins)
- **Days 3-5:** Phase 2 (Build Pipeline)

### Week 2: Infrastructure
- **Days 1-3:** Phase 3 (Advanced Optimization)
- **Days 4-5:** Phase 4 (Polish)

### Week 3: Testing & Launch
- **Days 1-2:** End-to-end testing
- **Day 3:** Performance audit
- **Day 4:** Production deployment
- **Day 5:** Monitoring & adjustments

**Total Timeline:** 3 weeks (full-time) or 6-8 weeks (part-time)

---

## Risk Assessment

### High Risk Items

1. **Vite Migration** (Phase 2)
   - **Risk:** Breaking existing functionality
   - **Mitigation:** Incremental migration, parallel deployment
   - **Rollback:** Keep old version live during testing

2. **Vercel Migration** (Phase 3)
   - **Risk:** DNS propagation issues
   - **Mitigation:** Test with subdomain first
   - **Rollback:** Keep GoDaddy FTP as backup

3. **Image CDN Migration** (Phase 3)
   - **Risk:** Missing images, broken links
   - **Mitigation:** Verify all uploads, maintain local backup
   - **Rollback:** Fallback URLs in code

### Medium Risk Items

1. **TypeScript Conversion**
   - **Risk:** Type errors, compilation issues
   - **Mitigation:** Gradual migration, `any` types initially

2. **Code Splitting**
   - **Risk:** Increased complexity
   - **Mitigation:** Clear module boundaries

### Low Risk Items

1. **Analytics** - No user impact
2. **Testing** - Improves reliability
3. **Loading States** - Pure enhancement

---

## Success Metrics

### Technical KPIs
- [ ] Lighthouse Performance Score > 95
- [ ] First Contentful Paint < 1s
- [ ] Time to Interactive < 1.5s
- [ ] Total Bundle Size < 500KB
- [ ] Code Coverage > 80%

### Business KPIs
- [ ] Page Load Time reduced by 70%
- [ ] Deployment Time reduced by 95%
- [ ] Developer Time saved: 4-5 hours/week
- [ ] Zero downtime deployments

### User Experience KPIs
- [ ] Mobile usable (Lighthouse Mobile > 90)
- [ ] Works offline
- [ ] Installable as PWA
- [ ] Smooth interactions (no jank)

---

## Maintenance Plan

### Daily
- [ ] Check Sentry for errors
- [ ] Review analytics dashboard
- [ ] Monitor Vercel build status

### Weekly
- [ ] Update dependencies
- [ ] Review performance metrics
- [ ] Check CDN bandwidth usage

### Monthly
- [ ] Performance audit
- [ ] User feedback review
- [ ] Cost analysis (Vercel, Cloudinary)

### Quarterly
- [ ] Major dependency updates
- [ ] Lighthouse audit
- [ ] Security scan

---

## Rollback Procedures

### If Phase 2 Fails (Vite Migration)
1. Revert to Python HTML generation
2. Keep using `public/index.html`
3. Continue with FTP deployment
4. Apply only Phase 1 optimizations

### If Phase 3 Fails (Vercel)
1. Revert DNS to GoDaddy
2. Deploy built files via FTP
3. Disable service worker
4. Keep Vite build pipeline

### If Everything Fails
1. Git revert to last working commit
2. Redeploy via FTP
3. Original `public/index.html` still works
4. No data loss (all git tracked)

---

## Notes

- **Backup Before Starting:** Full git commit + GoDaddy FTP backup
- **Test Environment:** Use Vercel preview URLs for testing
- **Documentation:** Update README.md after each phase
- **Communication:** Announce maintenance window if needed
- **Budget:** Vercel Free tier sufficient, Cloudinary Free tier = 25GB/month

---

## Next Steps

1. **Review this plan** - Adjust timeline/priorities as needed
2. **Create GitHub Project** - Track tasks with issues
3. **Set up environments** - Development, staging, production
4. **Start Phase 1** - Quick wins first
5. **Iterate and improve** - Continuous optimization

---

**Last Updated:** 2025-11-17
**Status:** Ready to implement
**Estimated ROI:** 70-80% performance improvement, 95% faster deployments
