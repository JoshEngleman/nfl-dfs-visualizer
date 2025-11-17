# Phase 2: Modern Build Pipeline - Preparation

**Date:** November 17, 2025
**Status:** 🔄 In Progress
**Started:** November 17, 2025, 3:15 PM
**Expected Duration:** 2-3 days
**Risk Level:** Medium (requires migration testing)

---

## Overview

Phase 2 will migrate the current browser-based JSX compilation to a modern build pipeline using **Vite + React + TypeScript**.

### Current State (index.html)
- ❌ Browser compiles JSX on every page load (300-800ms penalty)
- ❌ No code splitting - loads all code at once
- ❌ No minification or tree shaking
- ❌ No TypeScript type safety
- ❌ Single 2400+ line HTML file
- ✅ Works perfectly, deployed and tested

### Target State (Vite Build)
- ✅ Pre-compiled React components (instant load)
- ✅ Code splitting by route and feature
- ✅ Minified, tree-shaken bundles
- ✅ TypeScript type safety
- ✅ Modular component architecture
- ✅ Professional dev workflow with HMR

---

## Expected Benefits

### Performance
- **300-800ms faster** initial load (no JSX compilation)
- **60-70% smaller bundle** with code splitting
- **Faster subsequent loads** with better caching
- **Better mobile performance** with smaller payloads

### Developer Experience
- **Type safety** with TypeScript
- **Better IDE support** (autocomplete, refactoring)
- **Hot Module Replacement** (instant updates during dev)
- **Component reusability** (modular architecture)
- **Easier testing** (unit tests for components)

---

## Migration Strategy

### Approach: Parallel Development
We'll create a new `nfl-dfs-frontend/` directory alongside existing code:

```
random-utilities/
├── public/              # OLD - Current working version
│   └── index.html       # Keep as backup/fallback
├── nfl-dfs-frontend/    # NEW - Vite project
│   ├── src/
│   ├── public/
│   ├── dist/            # Build output goes here
│   └── package.json
├── src/                 # Python scripts (unchanged)
├── cache/               # Headshots (unchanged)
└── data/                # CSV files (unchanged)
```

**Benefits of this approach:**
- ✅ Keep old version working during migration
- ✅ Can test new version before switching
- ✅ Easy rollback if needed
- ✅ Python scripts don't change
- ✅ Can compare old vs new side-by-side

---

## Phase 2 Tasks Breakdown

### Task 2.1: Initialize Vite Project (3-4 hours) ✅ COMPLETED
**Status:** ✅ Done - November 17, 2025
**Commit:** `2e2617e`

**What we did:**
1. ✅ Created `nfl-dfs-frontend/` directory
2. ✅ Initialized Vite with React + TypeScript template
3. ✅ Installed dependencies (recharts, papaparse, @types/papaparse)
4. ✅ Verified project structure

**Node.js/npm versions:**
- Node.js: v22.12.0
- npm: v10.9.0

**Installed packages:**
- React 18
- TypeScript 5
- Vite 6
- recharts (charts)
- papaparse (CSV parsing)
- @types/papaparse (TypeScript types)

---

### Task 2.2: Create Type Definitions (1-2 hours) ✅ COMPLETED
**Status:** ✅ Done - November 17, 2025
**Commit:** `53bc188`
**File:** `nfl-dfs-frontend/src/types/player.ts`

**What we did:**
1. ✅ Created comprehensive TypeScript interfaces
2. ✅ Defined Player interface (14 properties)
3. ✅ Added Position types and constants
4. ✅ Created ChartData, ChartFilters types
5. ✅ Added TableColumn, TableSort, ColumnVisibility types
6. ✅ Defined StoredData (localStorage structure)
7. ✅ Created ColumnFilters, CSVParseResult types
8. ✅ Added TeamColors and NameMapping interfaces

**Benefits achieved:**
- Type-safe development foundation
- Better IDE autocomplete
- Self-documenting code
- Compile-time error checking

---

### Task 2.3: Extract React Components (6-8 hours)
**What we'll do:**
1. Split monolithic index.html into modular components:
   - `App.tsx` - Main app container
   - `ChartView.tsx` - Scatter chart with filters
   - `DataTable.tsx` - Sortable data table
   - `CSVUpload.tsx` - File upload handler
   - `PlayerHeadshot.tsx` - Image loading component
   - `Filters.tsx` - Position/team filtering

**Migration steps:**
- Copy existing React code from index.html
- Convert to TypeScript (.tsx files)
- Add proper types to props and state
- Extract styles to separate CSS modules
- Test each component individually

---

### Task 2.4: Migrate Data Management (2-3 hours)
**What we'll do:**
1. Extract localStorage logic to custom hooks:
   - `useLocalStorage.ts` - Generic localStorage hook
   - `usePlayerData.ts` - Player data management
   - `useCSVParser.ts` - CSV parsing logic

2. Move utility functions:
   - `teamColors.ts` - Team color mappings
   - `imageUtils.ts` - Headshot loading logic
   - `playerUtils.ts` - Player name formatting

**Why:**
- Reusable logic across components
- Easier to test
- Cleaner component code

---

### Task 2.5: Configure Build & Deployment (2-3 hours)
**What we'll do:**
1. Configure Vite build output to `dist/`
2. Set up code splitting (vendor chunks)
3. Configure asset optimization
4. Update `deploy.py` to handle new `dist/` output
5. Test local build: `npm run build`

**New deployment workflow:**
```bash
# Build frontend
cd nfl-dfs-frontend
npm run build

# Deploy (from project root)
./deploy.sh website  # Now uploads from nfl-dfs-frontend/dist/
```

---

### Task 2.6: Testing & Validation (2-3 hours)
**What we'll do:**
1. **Local testing:**
   - Run dev server: `npm run dev`
   - Test all features (upload, chart, table, filters)
   - Check console for errors
   - Verify images load correctly

2. **Build testing:**
   - Build production bundle: `npm run build`
   - Preview build: `npm run preview`
   - Test minified version
   - Check bundle sizes

3. **Lighthouse testing:**
   - Run Lighthouse before migration
   - Run Lighthouse after migration
   - Compare scores

4. **Production testing:**
   - Deploy to staging (if available)
   - OR deploy to production with ability to rollback
   - Test on real devices (mobile, desktop)

---

## Prerequisites

### Required Tools
- [x] Node.js installed (check: `node --version`)
- [x] npm installed (check: `npm --version`)
- [ ] TypeScript knowledge (we'll learn as we go)
- [x] Git for version control

### Current Project Status
- [x] Phase 1 complete and deployed
- [x] Working backup in `public/index.html`
- [x] Clean git state
- [x] All features documented

---

## Risk Mitigation

### Risks & Mitigations

**Risk 1: Migration introduces bugs**
- ✅ Mitigation: Keep old version as fallback
- ✅ Mitigation: Thorough testing before deployment
- ✅ Mitigation: Can rollback to old index.html instantly

**Risk 2: Build process complexity**
- ✅ Mitigation: Use proven tools (Vite, React, TypeScript)
- ✅ Mitigation: Follow best practices
- ✅ Mitigation: Document build process

**Risk 3: Breaking changes to workflow**
- ✅ Mitigation: Python scripts don't change
- ✅ Mitigation: Headshot workflow stays the same
- ✅ Mitigation: Deployment script handles new output

**Risk 4: Time investment**
- ✅ Mitigation: Can pause and use old version anytime
- ✅ Mitigation: Modular approach (can do piece by piece)
- ✅ Mitigation: Clear task breakdown

---

## Success Criteria

Phase 2 will be considered successful when:

- [ ] All features from old version work in new version
- [ ] Lighthouse Performance Score improves
- [ ] Initial load time is 300-800ms faster
- [ ] Bundle size is 60-70% smaller
- [ ] No console errors
- [ ] All images load correctly
- [ ] CSV upload works
- [ ] Chart and table views work
- [ ] Filters work correctly
- [ ] Mobile responsive
- [ ] TypeScript compiles without errors
- [ ] Build process is documented
- [ ] Deployment workflow is updated

---

## Rollback Plan

If Phase 2 fails or has issues:

### Quick Rollback (5 minutes)
```bash
# Option 1: Revert to old index.html
git checkout main -- public/index.html
./deploy.sh website

# Option 2: Use git revert
git revert HEAD -m 1
./deploy.sh website
```

### Keep Both Versions
- Old version: `https://joshengleman.com/nfl-dfs/index-old.html`
- New version: `https://joshengleman.com/nfl-dfs/`
- Can switch between them easily

---

## Timeline Estimate

### Optimistic (2 days)
- Day 1: Tasks 2.1-2.3 (Vite setup + component extraction)
- Day 2: Tasks 2.4-2.6 (Data management + deployment + testing)

### Realistic (3 days)
- Day 1: Tasks 2.1-2.2 (Vite setup + types)
- Day 2: Tasks 2.3-2.4 (Components + data management)
- Day 3: Tasks 2.5-2.6 (Build config + testing + deployment)

### Conservative (4 days)
- Day 1: Task 2.1 (Vite setup + verification)
- Day 2: Tasks 2.2-2.3 (Types + components)
- Day 3: Task 2.4 (Data management)
- Day 4: Tasks 2.5-2.6 (Build + testing + deployment)

**Recommended approach:** Start with realistic estimate (3 days)

---

## File Structure Preview

### Before (Current)
```
random-utilities/
└── public/
    └── index.html (2400+ lines)
```

### After (Phase 2)
```
random-utilities/
├── public/
│   └── index-old.html (backup)
├── nfl-dfs-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chart/
│   │   │   │   ├── ChartView.tsx
│   │   │   │   ├── ChartFilters.tsx
│   │   │   │   └── PlayerTooltip.tsx
│   │   │   ├── DataTable/
│   │   │   │   ├── DataTable.tsx
│   │   │   │   ├── ColumnFilter.tsx
│   │   │   │   └── TableRow.tsx
│   │   │   ├── Upload/
│   │   │   │   └── CSVUpload.tsx
│   │   │   └── Layout/
│   │   │       ├── Header.tsx
│   │   │       └── TabNavigation.tsx
│   │   ├── hooks/
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── usePlayerData.ts
│   │   │   └── useCSVParser.ts
│   │   ├── types/
│   │   │   └── player.ts
│   │   ├── utils/
│   │   │   ├── teamColors.ts
│   │   │   ├── imageUtils.ts
│   │   │   └── playerUtils.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   └── headshots/ (symlink to ../../cache/headshot_cache_compressed)
│   ├── dist/ (build output)
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── src/ (Python scripts - unchanged)
```

---

## Next Steps

When ready to begin Phase 2:

1. ✅ Create `phase-2-modern-build` branch
2. ✅ Check Node.js/npm versions
3. ✅ Start with Task 2.1 (Initialize Vite)
4. ✅ Follow task breakdown systematically
5. ✅ Commit frequently
6. ✅ Test thoroughly before merging

---

## Questions to Answer Before Starting

1. **Do we have Node.js installed?**
   - Check: `node --version` (need v16+)
   - Check: `npm --version` (need v7+)

2. **Do we want to use Tailwind CSS?**
   - Pro: Modern utility-first CSS
   - Con: Adds complexity
   - Decision: Optional, can add later

3. **Should we keep old version accessible?**
   - Recommendation: Yes, as `index-old.html`
   - Allows users to switch if issues arise

4. **Testing strategy?**
   - Option A: Deploy directly (can rollback)
   - Option B: Deploy to subdirectory first (`/nfl-dfs/beta/`)
   - Recommendation: Option A (we can rollback easily)

---

**Status:** Ready to begin Phase 2 when you are!

**First Command:**
```bash
# Check if we have Node.js and npm
node --version
npm --version
```

If installed, we can proceed to create the branch and initialize Vite!
