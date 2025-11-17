#!/usr/bin/env python3
"""
Stokastic NFL Boom/Bust Visualization - React/Recharts version
Generates standalone HTML using React + Recharts (same as NBA implementation)
"""

import pandas as pd
import numpy as np
import argparse
from typing import Optional
import requests
from PIL import Image
from io import BytesIO
import base64
import os
from pathlib import Path
import json


class NFLDFSVisualizer:
    """Generates React/Recharts visualization (matches NBA implementation)"""

    def __init__(self, csv_path: str, name_mappings: Optional[dict] = None):
        self.csv_path = csv_path
        self.df = None
        self.roster_cache = None
        self.name_mappings = name_mappings or {}
        self.unmatched_names = []

        # Create cache directory for headshots
        self.cache_dir = Path('headshot_cache')
        self.cache_dir.mkdir(exist_ok=True)

        self._load_data()
        self._load_roster_data()

    def _load_data(self):
        """Load CSV data"""
        print(f"Loading data from {self.csv_path}...")
        self.df = pd.read_csv(self.csv_path)
        self.df.columns = self.df.columns.str.strip()

        if 'Salary' in self.df.columns:
            self.df['Salary'] = self.df['Salary'].str.replace('$', '').str.replace(',', '').astype(float)

        numeric_cols = ['Projection', 'Std Dev', 'Ceiling', 'Bust%', 'Boom%', 'Own%', 'Optimal%', 'Leverage']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        print(f"Loaded {len(self.df)} players")

    def _load_roster_data(self):
        """Load NFL roster data for current season"""
        try:
            print("Loading NFL roster data...")
            import nfl_data_py as nfl
            import datetime

            # Determine current NFL season year
            # NFL season starts in September and ends in February
            # If we're in Jan-Aug, use previous year's season
            current_date = datetime.datetime.now()
            current_year = current_date.year

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

    def _get_base64_from_cache(self, filename: str, max_size: int = 300) -> Optional[str]:
        """Load cached image, compress/resize, and convert to base64 data URL"""
        local_path = self.cache_dir / filename

        if not local_path.exists():
            return None

        try:
            img = Image.open(local_path)

            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85, optimize=True)
            img_data = buffered.getvalue()

            img_base64 = base64.b64encode(img_data).decode()
            return f"data:image/jpeg;base64,{img_base64}"
        except Exception as e:
            print(f"Failed to load cached image {filename}: {e}")
            return None

    def _download_and_cache_image(self, url: str, filename: str) -> Optional[str]:
        """Download image, save to cache, and return base64 data URL"""
        local_path = self.cache_dir / filename

        if local_path.exists():
            return self._get_base64_from_cache(filename)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                print(f"Cached: {filename}")
                return self._get_base64_from_cache(filename)
        except Exception as e:
            print(f"Failed to cache {filename}: {e}")

        return None

    def _get_team_logo_url(self, team_abbr: str) -> str:
        """Get NFL team logo URL (external)"""
        url = f"https://a.espncdn.com/i/teamlogos/nfl/500/{team_abbr.upper()}.png"
        return url

    def _get_headshot_url(self, player_name: str, team: str, position: str = None) -> Optional[str]:
        """Get NFL headshot URL or team logo URL"""

        if position == 'DST':
            return self._get_team_logo_url(team)

        if self.roster_cache is None or self.roster_cache.empty:
            return None

        # Check custom name mappings first
        mapping_key = f"{player_name}|{team}"
        if mapping_key in self.name_mappings:
            mapped_name = self.name_mappings[mapping_key]
            print(f"Using custom mapping: {player_name} -> {mapped_name}")
            match = self.roster_cache[self.roster_cache['player_name'] == mapped_name]
            if not match.empty and 'headshot_url' in match.columns:
                url = match.iloc[0]['headshot_url']
                if pd.notna(url):
                    return url

        # Exact match
        match = self.roster_cache[
            (self.roster_cache['player_name'] == player_name) &
            (self.roster_cache['team'] == team)
        ]

        if not match.empty and 'headshot_url' in match.columns:
            url = match.iloc[0]['headshot_url']
            if pd.notna(url):
                return url

        # Fuzzy match by last name
        name_parts = player_name.split()
        if len(name_parts) >= 2:
            last_name = name_parts[-1]

            match = self.roster_cache[
                (self.roster_cache['player_name'].str.contains(last_name, case=False, na=False)) &
                (self.roster_cache['team'] == team)
            ]

            if not match.empty and 'headshot_url' in match.columns:
                url = match.iloc[0]['headshot_url']
                if pd.notna(url):
                    print(f"Fuzzy matched: {player_name} -> {match.iloc[0]['player_name']}")
                    return url

        # Fuzzy match without team filter
        match = self.roster_cache[
            self.roster_cache['player_name'].str.contains(player_name, case=False, na=False)
        ]

        if not match.empty and 'headshot_url' in match.columns:
            url = match.iloc[0]['headshot_url']
            if pd.notna(url):
                print(f"Fuzzy matched (no team): {player_name} -> {match.iloc[0]['player_name']}")
                return url

        # Track unmatched names
        unmatched_info = {'name': player_name, 'team': team, 'position': position}
        if unmatched_info not in self.unmatched_names:
            self.unmatched_names.append(unmatched_info)

        print(f"No headshot found for: {player_name} ({team})")
        return None

    def find_potential_matches(self, player_name: str, team: str = None, limit: int = 10) -> list:
        """Find potential roster matches for a player name"""
        if self.roster_cache is None or self.roster_cache.empty:
            return []

        potential_matches = []

        # Extract last name for fuzzy matching
        name_parts = player_name.split()
        last_name = name_parts[-1] if name_parts else player_name

        # Search by last name
        if team:
            matches = self.roster_cache[
                (self.roster_cache['player_name'].str.contains(last_name, case=False, na=False)) &
                (self.roster_cache['team'] == team)
            ].head(limit)
        else:
            matches = self.roster_cache[
                self.roster_cache['player_name'].str.contains(last_name, case=False, na=False)
            ].head(limit)

        for _, row in matches.iterrows():
            potential_matches.append({
                'player_name': row['player_name'],
                'team': row.get('team', 'Unknown'),
                'position': row.get('position', 'Unknown')
            })

        return potential_matches

    def prepare_data_for_position(self, position_filter: str = 'ALL'):
        """Prepare data for a single position"""

        if position_filter != 'ALL':
            df_filtered = self.df[self.df['Position'] == position_filter].copy()
        else:
            df_filtered = self.df.copy()

        print(f"  {len(df_filtered)} {position_filter} players")

        # Prepare player data with headshots
        players_data = []
        for idx, row in df_filtered.iterrows():
            headshot_url = self._get_headshot_url(row['Name'], row['Team'], row['Position'])

            # Use team logo as fallback if no player headshot found
            if not headshot_url:
                headshot_url = self._get_team_logo_url(row['Team'])

            players_data.append({
                'player_name': row['Name'],
                'player_id': f"{row['Name'].replace(' ', '_')}_{idx}",
                'position': row['Position'],
                'team_abbr': row['Team'],
                'salary': float(row['Salary']),
                'dk_projection': float(row['Projection']) if pd.notna(row['Projection']) else 0,
                'std_dev': float(row['Std Dev']) if pd.notna(row['Std Dev']) else 0,
                'ceiling': float(row['Ceiling']) if pd.notna(row['Ceiling']) else 0,
                'bust_pct': float(row['Bust%']) if pd.notna(row['Bust%']) else 0,
                'boom_pct': float(row['Boom%']) if pd.notna(row['Boom%']) else 0,
                'ownership_pct': float(row['Own%']) if pd.notna(row['Own%']) else 0,
                'optimal_pct': float(row['Optimal%']) if pd.notna(row['Optimal%']) else 0,
                'leverage': float(row['Leverage']) if pd.notna(row['Leverage']) else 0,
                'headshot_url': headshot_url
            })

        return players_data

    def create_visualization(self, position_filter: str = 'ALL', output_path: str = 'boom_bust.html'):
        """Create multi-position visualization with dropdown selector using React/Recharts"""

        positions = ['ALL'] + sorted(self.df['Position'].unique().tolist())
        print(f"Generating visualizations for positions: {', '.join(positions)}")

        # Prepare data for all positions
        all_data = {}
        for pos in positions:
            print(f"  Processing {pos}...")
            all_data[pos] = self.prepare_data_for_position(pos)

        # Default position
        default_position = 'QB' if 'QB' in positions else positions[0]

        print(f"\nSaving visualization to {output_path}...")

        # Generate HTML with React/Recharts
        html_content = self._generate_react_html(all_data, positions, default_position)

        with open(output_path, 'w') as f:
            f.write(html_content)

        print(f"✓ Visualization saved to: {output_path}")
        file_size_mb = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"File size: {file_size_mb:.1f} MB")
        print(f"Open {output_path} in your browser to view")
        print(f"Default position: {default_position}")

    def _generate_react_html(self, all_data: dict, positions: list, default_position: str) -> str:
        """Generate standalone HTML with React/Recharts"""

        data_json = json.dumps(all_data)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stokastic NFL Boom/Bust Analysis</title>

    <!-- React and ReactDOM from CDN -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-is@18/umd/react-is.production.min.js"></script>
    <script src="https://unpkg.com/prop-types/prop-types.min.js"></script>

    <!-- Recharts from CDN -->
    <script src="https://unpkg.com/recharts@2.12.0/umd/Recharts.js"></script>

    <!-- Babel standalone for JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- dom-to-image for better SVG export with external images -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.min.js"></script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f9fafb;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }}

        .selector-container {{
            text-align: center;
            padding: 20px;
            background: #f9fafb;
            border-bottom: 2px solid #e5e7eb;
            margin: -20px -20px 20px -20px;
            border-radius: 8px 8px 0 0;
        }}

        select {{
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 700;
            border: 2px solid #d1d5db;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        label {{
            margin-right: 10px;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .chart-title {{
            text-align: center;
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .info-text {{
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 15px;
            letter-spacing: 0.3px;
        }}

        /* Filter Containers */
        .filters-container {{
            display: flex;
            gap: 16px;
            flex-direction: column;
            margin-bottom: 20px;
        }}

        .filter-group {{
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .filter-group-header {{
            font-family: 'Oswald', 'Impact', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #374151;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .filter-group-content {{
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
        }}

        .filter-item {{
            flex: 1;
            min-width: 180px;
        }}

        .filter-item label {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 7px;
            font-size: 12px;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .filter-item select,
        .filter-item input[type="text"] {{
            width: 100%;
            padding: 9px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            background: #ffffff;
            color: #1f2937;
            font-weight: 500;
            transition: all 0.15s;
        }}

        .filter-item select:hover,
        .filter-item input[type="text"]:hover {{
            border-color: #9ca3af;
            background: #f9fafb;
        }}

        .filter-item select:focus,
        .filter-item input[type="text"]:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }}

        /* Range Slider Styles */
        .range-slider {{
            margin-top: 5px;
        }}

        .range-values {{
            font-size: 13px;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }}

        .slider-container {{
            position: relative;
            height: 30px;
        }}

        .slider-container input[type="range"] {{
            position: absolute;
            width: 100%;
            pointer-events: none;
            -webkit-appearance: none;
            appearance: none;
            background: transparent;
            height: 5px;
        }}

        .slider-container input[type="range"]::-webkit-slider-thumb {{
            pointer-events: auto;
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #3b82f6;
            cursor: pointer;
            border: 2px solid #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: transform 0.15s, box-shadow 0.15s;
        }}

        .slider-container input[type="range"]::-webkit-slider-thumb:hover {{
            transform: scale(1.1);
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        }}

        .slider-container input[type="range"]::-moz-range-thumb {{
            pointer-events: auto;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #3b82f6;
            cursor: pointer;
            border: 2px solid #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: transform 0.15s, box-shadow 0.15s;
        }}

        .slider-container input[type="range"]::-moz-range-thumb:hover {{
            transform: scale(1.1);
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        }}

        .slider-container input[type="range"]::-webkit-slider-runnable-track {{
            width: 100%;
            height: 5px;
            background: #e5e7eb;
            border-radius: 3px;
        }}

        .slider-container input[type="range"]::-moz-range-track {{
            width: 100%;
            height: 5px;
            background: #e5e7eb;
            border-radius: 3px;
        }}

        /* Buttons */
        .button-group {{
            display: flex;
            gap: 10px;
            justify-content: center;
        }}

        button {{
            padding: 10px 20px;
            font-family: 'Oswald', 'Impact', sans-serif;
            font-size: 14px;
            font-weight: 700;
            border-radius: 6px;
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.15s;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .btn-primary {{
            background: #3b82f6;
            color: #ffffff;
            border-color: #3b82f6;
        }}

        .btn-primary:hover {{
            background: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
        }}

        .btn-secondary {{
            background: #ffffff;
            color: #6b7280;
            border-color: #d1d5db;
        }}

        .btn-secondary:hover {{
            background: #f9fafb;
            border-color: #9ca3af;
            color: #374151;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }}

        button:active {{
            transform: translateY(0);
        }}

        .btn-outline {{
            background: white;
            color: #3b82f6;
            border: 2px solid #3b82f6;
        }}

        .btn-outline:hover {{
            background: #eff6ff;
        }}

        /* Position Badge Toggles */
        .position-badges-container {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            padding: 4px 0;
        }}

        .position-toggle {{
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: opacity 0.2s ease, transform 0.1s ease;
            user-select: none;
            min-width: 50px;
            text-align: center;
            border: 2px solid transparent;
        }}

        .position-toggle.active {{
            opacity: 1;
        }}

        .position-toggle.inactive {{
            opacity: 0.3;
        }}

        .position-toggle:hover {{
            transform: translateY(-2px);
        }}

        .position-toggle.position-QB {{
            background: #dc2626;
            color: white;
        }}

        .position-toggle.position-RB {{
            background: #059669;
            color: white;
        }}

        .position-toggle.position-WR {{
            background: #3b82f6;
            color: white;
        }}

        .position-toggle.position-TE {{
            background: #d97706;
            color: white;
        }}

        .position-toggle.position-DST {{
            background: #6b7280;
            color: white;
        }}

        .position-toggle.position-ALL {{
            background: #8b5cf6;
            color: white;
        }}

        /* Team Logo Toggles */
        .team-logos-container {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 8px 0;
        }}

        .team-logos-row {{
            display: flex;
            justify-content: space-between;
            flex-wrap: nowrap;
            align-items: center;
        }}

        .team-logo-toggle {{
            width: 60px;
            height: 60px;
            flex: 0 0 60px;
            object-fit: contain;
            cursor: pointer;
            transition: opacity 0.2s ease, transform 0.1s ease;
            border-radius: 4px;
            padding: 4px;
        }}

        .team-logo-toggle.active {{
            opacity: 1;
        }}

        .team-logo-toggle.inactive {{
            opacity: 0.3;
        }}

        .team-logo-toggle:hover {{
            transform: scale(1.15);
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                padding: 15px;
            }}

            .filters-container {{
                flex-direction: column;
            }}

            .filter-item {{
                min-width: 100%;
            }}

            .chart-title {{
                font-size: 18px;
            }}

            .info-text {{
                font-size: 10px;
            }}

            .button-group {{
                flex-direction: column;
            }}

            button {{
                width: 100%;
            }}

            .recharts-wrapper {{
                font-size: 10px;
            }}

            .team-logos-row {{
                flex-wrap: wrap;
                justify-content: center;
            }}

            .team-logo-toggle {{
                width: 45px;
                height: 45px;
            }}
        }}

        /* Ensure chart container has proper sizing */
        .recharts-responsive-container {{
            min-height: 500px;
            background:
                radial-gradient(circle at center, rgba(250, 250, 248, 1) 0%, rgba(245, 245, 243, 1) 100%),
                linear-gradient(90deg, rgba(229, 231, 235, 0.2) 1px, transparent 1px),
                linear-gradient(rgba(229, 231, 235, 0.2) 1px, transparent 1px);
            background-size: 100% 100%, 40px 40px, 40px 40px;
            background-position: center, 0 0, 0 0;
            border-radius: 8px;
        }}

        @media (max-width: 768px) {{
            .recharts-responsive-container {{
                min-height: 400px;
            }}
        }}

        /* Tab Styles */
        .tab-navigation {{
            display: flex;
            gap: 4px;
            border-bottom: 2px solid #e5e7eb;
            margin: 20px -20px 0 -20px;
            padding: 0 20px;
        }}

        .tab-button {{
            padding: 12px 24px;
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            color: #6b7280;
            transition: all 0.2s;
            margin-bottom: -2px;
        }}

        .tab-button:hover {{
            color: #3b82f6;
            background: #f9fafb;
        }}

        .tab-button.active {{
            color: #3b82f6;
            border-bottom-color: #3b82f6;
            background: #ffffff;
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.3s;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* Data Table Styles */
        .data-table-container {{
            padding: 20px 0;
        }}

        .table-controls {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px;
            background: #f9fafb;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }}

        .table-search {{
            flex: 1;
            min-width: 250px;
        }}

        .table-search input {{
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            font-family: 'Outfit', sans-serif;
        }}

        .table-search input:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }}

        .column-visibility {{
            position: relative;
        }}

        .column-visibility-btn {{
            padding: 10px 16px;
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: #374151;
        }}

        .column-visibility-dropdown {{
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 5px;
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 10px;
            min-width: 200px;
            z-index: 1000;
            max-height: 300px;
            overflow-y: auto;
        }}

        .column-visibility-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px;
            cursor: pointer;
        }}

        .column-visibility-item:hover {{
            background: #f9fafb;
        }}

        .column-visibility-item input[type="checkbox"] {{
            cursor: pointer;
        }}

        .data-table-wrapper {{
            overflow-x: auto;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: white;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .data-table th {{
            background: #f9fafb;
            padding: 10.8px 14.4px;
            text-align: left;
            font-weight: 700;
            color: #374151;
            border-bottom: 2px solid #e5e7eb;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        .data-table th.sortable {{
            cursor: pointer;
            user-select: none;
        }}

        .data-table th.sortable:hover {{
            background: #e5e7eb;
        }}

        .data-table th .sort-indicator {{
            display: inline-block;
            margin-left: 5px;
            font-size: 10px;
            color: #9ca3af;
        }}

        .data-table th.sort-asc .sort-indicator::after {{
            content: '▲';
            color: #3b82f6;
        }}

        .data-table th.sort-desc .sort-indicator::after {{
            content: '▼';
            color: #3b82f6;
        }}

        .data-table th.has-filter {{
            background: #eff6ff;
        }}

        .th-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            position: relative;
        }}

        .th-content > span {{
            flex: 1;
            cursor: pointer;
        }}

        .filter-trigger {{
            background: none;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            padding: 4px 8px;
            cursor: pointer;
            font-size: 12px;
            color: #6b7280;
            transition: all 0.15s;
            margin: 0;
            box-shadow: none;
        }}

        .filter-trigger:hover {{
            background: #f3f4f6;
            color: #3b82f6;
            border-color: #3b82f6;
            transform: none;
        }}

        .has-filter .filter-trigger {{
            color: #3b82f6;
            border-color: #3b82f6;
            background: #eff6ff;
        }}

        .column-filter-dropdown {{
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 5px;
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 12px;
            min-width: 200px;
            z-index: 1000;
            text-transform: none;
            font-weight: normal;
        }}

        .filter-checkbox-list {{
            max-height: 250px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .filter-checkbox-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 8px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 13px;
            color: #374151;
            font-weight: normal;
        }}

        .filter-checkbox-item:hover {{
            background: #f9fafb;
        }}

        .filter-checkbox-item input[type="checkbox"] {{
            cursor: pointer;
        }}

        .filter-range {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .filter-range-item {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}

        .filter-range-item label {{
            font-size: 11px;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
        }}

        .filter-range-item input {{
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 13px;
            font-family: 'Outfit', sans-serif;
            width: 100%;
        }}

        .filter-range-item input:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }}

        .data-table td {{
            padding: 10.8px 14.4px;
            border-bottom: 1px solid #f3f4f6;
            color: #1f2937;
            font-weight: 500;
        }}

        .data-table tr:hover {{
            background: #f9fafb;
        }}

        .data-table .player-cell {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .data-table .player-name {{
            text-transform: uppercase;
        }}

        .data-table .player-headshot {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #e5e7eb;
        }}

        .data-table .team-cell {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .data-table .team-logo {{
            width: 32px;
            height: 32px;
            object-fit: contain;
        }}

        .position-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
            text-align: center;
            min-width: 40px;
        }}

        .position-QB {{
            background: #dc2626;
            color: white;
        }}

        .position-RB {{
            background: #059669;
            color: white;
        }}

        .position-WR {{
            background: #3b82f6;
            color: white;
        }}

        .position-TE {{
            background: #d97706;
            color: white;
        }}

        .position-DST {{
            background: #6b7280;
            color: white;
        }}

        .pagination {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding: 15px;
            background: #f9fafb;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }}

        .pagination-info {{
            font-size: 13px;
            color: #6b7280;
            font-weight: 600;
        }}

        .pagination-buttons {{
            display: flex;
            gap: 8px;
        }}

        .pagination-button {{
            padding: 8px 16px;
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: #374151;
            transition: all 0.15s;
        }}

        .pagination-button:hover:not(:disabled) {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}

        .pagination-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        @media (max-width: 768px) {{
            .table-controls {{
                flex-direction: column;
                align-items: stretch;
            }}

            .table-search {{
                min-width: 100%;
            }}

            .pagination {{
                flex-direction: column;
                gap: 15px;
            }}

            .data-table {{
                font-size: 11px;
            }}

            .data-table th,
            .data-table td {{
                padding: 7.2px 10.8px;
            }}
        }}
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState, useEffect }} = React;
        const {{ ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, ReferenceArea }} = Recharts;

        // All data embedded
        const allData = {data_json};
        const positions = {json.dumps(positions)};
        const defaultPosition = '{default_position}';

        // Available stats for axes and sizing
        const statOptions = [
            {{ value: 'boom_pct', label: 'Boom %' }},
            {{ value: 'bust_pct', label: 'Bust %' }},
            {{ value: 'leverage', label: 'Leverage' }},
            {{ value: 'ownership_pct', label: 'Ownership %' }},
            {{ value: 'optimal_pct', label: 'Optimal %' }},
            {{ value: 'salary', label: 'Salary' }},
            {{ value: 'dk_projection', label: 'Projection' }},
            {{ value: 'std_dev', label: 'Std Dev' }},
            {{ value: 'ceiling', label: 'Ceiling' }},
        ];

        // Helper functions (shared by both components)
        const getTeamLogoUrl = (teamAbbr) => {{
            return `https://a.espncdn.com/i/teamlogos/nfl/500/${{teamAbbr.toLowerCase()}}.png`;
        }};

        const getTeamColor = (teamAbbr) => {{
            const teamColors = {{
                'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773', 'BUF': '#00338D',
                'CAR': '#0085CA', 'CHI': '#C83803', 'CIN': '#FB4F14', 'CLE': '#311D00',
                'DAL': '#041E42', 'DEN': '#FB4F14', 'DET': '#0076B6', 'GB': '#203731',
                'HOU': '#03202F', 'IND': '#002C5F', 'JAX': '#006778', 'KC': '#E31837',
                'LAC': '#0080C6', 'LAR': '#003594', 'LV': '#000000', 'MIA': '#008E97',
                'MIN': '#4F2683', 'NE': '#002244', 'NO': '#D3BC8D', 'NYG': '#0B2265',
                'NYJ': '#125740', 'PHI': '#004C54', 'PIT': '#FFB612', 'SF': '#AA0000',
                'SEA': '#002244', 'TB': '#D50A0A', 'TEN': '#0C2340', 'WAS': '#5A1414'
            }};
            return teamColors[teamAbbr] || '#e5e7eb';
        }};

        // DataTable Component
        function DataTable() {{
            // Get all players (use 'ALL' position to avoid duplicates)
            const allPlayers = allData['ALL'] || [];

            // Table state
            const [searchTerm, setSearchTerm] = useState('');
            const [sortConfig, setSortConfig] = useState({{ key: null, direction: 'asc' }});
            const [currentPage, setCurrentPage] = useState(1);
            const [showColumnMenu, setShowColumnMenu] = useState(false);
            const [activeFilterColumn, setActiveFilterColumn] = useState(null);
            const [visibleColumns, setVisibleColumns] = useState({{
                player_name: true,
                position: true,
                team_abbr: true,
                salary: true,
                dk_projection: true,
                std_dev: true,
                ceiling: true,
                boom_pct: true,
                bust_pct: true,
                ownership_pct: true,
                optimal_pct: true,
                leverage: true
            }});

            // Column filters
            const [columnFilters, setColumnFilters] = useState({{
                position: [],
                team_abbr: [],
                salary: {{ min: '', max: '' }},
                dk_projection: {{ min: '', max: '' }},
                std_dev: {{ min: '', max: '' }},
                ceiling: {{ min: '', max: '' }},
                boom_pct: {{ min: '', max: '' }},
                bust_pct: {{ min: '', max: '' }},
                ownership_pct: {{ min: '', max: '' }},
                optimal_pct: {{ min: '', max: '' }},
                leverage: {{ min: '', max: '' }}
            }});

            const itemsPerPage = 25;

            // Column definitions
            const columns = [
                {{ key: 'player_name', label: 'Player', locked: true, type: 'text' }},
                {{ key: 'team_abbr', label: 'Team', type: 'checkbox' }},
                {{ key: 'position', label: 'Pos', type: 'checkbox' }},
                {{ key: 'salary', label: 'Salary', format: (val) => `$${{val.toLocaleString()}}`, type: 'range' }},
                {{ key: 'dk_projection', label: 'Proj', format: (val) => val.toFixed(1), type: 'range' }},
                {{ key: 'std_dev', label: 'Std Dev', format: (val) => val.toFixed(1), type: 'range' }},
                {{ key: 'ceiling', label: 'Ceiling', format: (val) => val.toFixed(1), type: 'range' }},
                {{ key: 'boom_pct', label: 'Boom%', format: (val) => `${{val.toFixed(1)}}%`, type: 'range' }},
                {{ key: 'bust_pct', label: 'Bust%', format: (val) => `${{val.toFixed(1)}}%`, type: 'range' }},
                {{ key: 'ownership_pct', label: 'Own%', format: (val) => `${{val.toFixed(1)}}%`, type: 'range' }},
                {{ key: 'optimal_pct', label: 'Opt%', format: (val) => `${{val.toFixed(1)}}%`, type: 'range' }},
                {{ key: 'leverage', label: 'Lev', format: (val) => val.toFixed(1), type: 'range' }}
            ];

            // Get unique teams and positions
            const allTeams = [...new Set(allPlayers.map(p => p.team_abbr))].sort();
            const allPositions = [...new Set(allPlayers.map(p => p.position))].sort();

            // Apply column filters
            const filteredData = allPlayers.filter(player => {{
                // Search term filter
                if (searchTerm) {{
                    const matchesSearch = player.player_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                        player.team_abbr.toLowerCase().includes(searchTerm.toLowerCase());
                    if (!matchesSearch) return false;
                }}

                // Position filter
                if (columnFilters.position.length > 0) {{
                    if (!columnFilters.position.includes(player.position)) return false;
                }}

                // Team filter
                if (columnFilters.team_abbr.length > 0) {{
                    if (!columnFilters.team_abbr.includes(player.team_abbr)) return false;
                }}

                // Range filters
                const rangeColumns = ['salary', 'dk_projection', 'std_dev', 'ceiling', 'boom_pct', 'bust_pct', 'ownership_pct', 'optimal_pct', 'leverage'];
                for (const col of rangeColumns) {{
                    const filter = columnFilters[col];
                    if (filter.min !== '' && player[col] < parseFloat(filter.min)) return false;
                    if (filter.max !== '' && player[col] > parseFloat(filter.max)) return false;
                }}

                return true;
            }});

            // Sort data
            const sortedData = React.useMemo(() => {{
                if (!sortConfig.key) return filteredData;

                return [...filteredData].sort((a, b) => {{
                    const aVal = a[sortConfig.key];
                    const bVal = b[sortConfig.key];

                    if (aVal === bVal) return 0;

                    const comparison = aVal < bVal ? -1 : 1;
                    return sortConfig.direction === 'asc' ? comparison : -comparison;
                }});
            }}, [filteredData, sortConfig]);

            // Pagination
            const totalPages = Math.ceil(sortedData.length / itemsPerPage);
            const startIndex = (currentPage - 1) * itemsPerPage;
            const paginatedData = sortedData.slice(startIndex, startIndex + itemsPerPage);

            // Handle sort
            const handleSort = (key) => {{
                setSortConfig(prev => ({{
                    key,
                    direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
                }}));
            }};

            // Toggle filter dropdown
            const toggleFilter = (key, e) => {{
                e.stopPropagation();
                setActiveFilterColumn(activeFilterColumn === key ? null : key);
            }};

            // Clear all filters
            const clearAllFilters = () => {{
                setSearchTerm('');
                setSortConfig({{ key: null, direction: 'asc' }});
                setCurrentPage(1);
                setColumnFilters({{
                    position: [],
                    team_abbr: [],
                    salary: {{ min: '', max: '' }},
                    dk_projection: {{ min: '', max: '' }},
                    std_dev: {{ min: '', max: '' }},
                    ceiling: {{ min: '', max: '' }},
                    boom_pct: {{ min: '', max: '' }},
                    bust_pct: {{ min: '', max: '' }},
                    ownership_pct: {{ min: '', max: '' }},
                    optimal_pct: {{ min: '', max: '' }},
                    leverage: {{ min: '', max: '' }}
                }});
                setActiveFilterColumn(null);
            }};

            // Check if column has active filter
            const hasActiveFilter = (key) => {{
                if (key === 'position') return columnFilters.position.length > 0;
                if (key === 'team_abbr') return columnFilters.team_abbr.length > 0;
                if (columnFilters[key]) {{
                    return columnFilters[key].min !== '' || columnFilters[key].max !== '';
                }}
                return false;
            }};

            // Reset to page 1 when search/filters change
            useEffect(() => {{
                setCurrentPage(1);
            }}, [searchTerm, columnFilters]);

            return (
                <div className="data-table-container">
                    <div className="table-controls">
                        <div className="table-search">
                            <input
                                type="text"
                                placeholder="Search by player name or team..."
                                value={{searchTerm}}
                                onChange={{(e) => setSearchTerm(e.target.value)}}
                            />
                        </div>

                        <div className="column-visibility">
                            <button
                                className="column-visibility-btn"
                                onClick={{() => setShowColumnMenu(!showColumnMenu)}}
                            >
                                Columns ▾
                            </button>
                            {{showColumnMenu && (
                                <div className="column-visibility-dropdown">
                                    {{columns.map(col => (
                                        <div
                                            key={{col.key}}
                                            className="column-visibility-item"
                                            onClick={{() => {{
                                                if (!col.locked) {{
                                                    setVisibleColumns(prev => ({{
                                                        ...prev,
                                                        [col.key]: !prev[col.key]
                                                    }}));
                                                }}
                                            }}}}
                                        >
                                            <input
                                                type="checkbox"
                                                checked={{visibleColumns[col.key]}}
                                                disabled={{col.locked}}
                                                onChange={{() => {{}}}}
                                            />
                                            <label>{{col.label}}</label>
                                        </div>
                                    ))}}
                                </div>
                            )}}
                        </div>

                        <button
                            className="btn-secondary"
                            onClick={{clearAllFilters}}
                        >
                            Clear Filters
                        </button>
                    </div>

                    <div className="data-table-wrapper">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    {{columns.filter(col => visibleColumns[col.key]).map(col => (
                                        <th
                                            key={{col.key}}
                                            className={{`sortable ${{sortConfig.key === col.key ? `sort-${{sortConfig.direction}}` : ''}} ${{hasActiveFilter(col.key) ? 'has-filter' : ''}}`}}
                                        >
                                            <div className="th-content">
                                                <span onClick={{() => handleSort(col.key)}}>
                                                    {{col.label}}
                                                    <span className="sort-indicator"></span>
                                                </span>
                                                {{col.type !== 'text' && (
                                                    <button
                                                        className="filter-trigger"
                                                        onClick={{(e) => toggleFilter(col.key, e)}}
                                                        title="Filter"
                                                    >
                                                        {{hasActiveFilter(col.key) ? '●' : '☰'}}
                                                    </button>
                                                )}}
                                            </div>

                                            {{/* Filter Dropdown */}}
                                            {{activeFilterColumn === col.key && (
                                                <div className="column-filter-dropdown" onClick={{(e) => e.stopPropagation()}}>
                                                    {{col.type === 'checkbox' && (
                                                        <div className="filter-checkbox-list">
                                                            {{(col.key === 'position' ? allPositions : allTeams).map(item => (
                                                                <label key={{item}} className="filter-checkbox-item">
                                                                    <input
                                                                        type="checkbox"
                                                                        checked={{columnFilters[col.key].includes(item)}}
                                                                        onChange={{(e) => {{
                                                                            setColumnFilters(prev => ({{
                                                                                ...prev,
                                                                                [col.key]: e.target.checked
                                                                                    ? [...prev[col.key], item]
                                                                                    : prev[col.key].filter(x => x !== item)
                                                                            }}));
                                                                        }}}}
                                                                    />
                                                                    {{item}}
                                                                </label>
                                                            ))}}
                                                        </div>
                                                    )}}

                                                    {{col.type === 'range' && (
                                                        <div className="filter-range">
                                                            <div className="filter-range-item">
                                                                <label>Min</label>
                                                                <input
                                                                    type="number"
                                                                    placeholder="Min"
                                                                    value={{columnFilters[col.key].min}}
                                                                    onChange={{(e) => {{
                                                                        setColumnFilters(prev => ({{
                                                                            ...prev,
                                                                            [col.key]: {{ ...prev[col.key], min: e.target.value }}
                                                                        }}));
                                                                    }}}}
                                                                    step={{col.key === 'salary' ? '100' : '0.1'}}
                                                                />
                                                            </div>
                                                            <div className="filter-range-item">
                                                                <label>Max</label>
                                                                <input
                                                                    type="number"
                                                                    placeholder="Max"
                                                                    value={{columnFilters[col.key].max}}
                                                                    onChange={{(e) => {{
                                                                        setColumnFilters(prev => ({{
                                                                            ...prev,
                                                                            [col.key]: {{ ...prev[col.key], max: e.target.value }}
                                                                        }}));
                                                                    }}}}
                                                                    step={{col.key === 'salary' ? '100' : '0.1'}}
                                                                />
                                                            </div>
                                                        </div>
                                                    )}}
                                                </div>
                                            )}}
                                        </th>
                                    ))}}
                                </tr>
                            </thead>
                            <tbody>
                                {{paginatedData.map((player, idx) => (
                                    <tr key={{`${{player.player_id}}_${{idx}}`}}>
                                        {{columns.filter(col => visibleColumns[col.key]).map(col => (
                                            <td key={{col.key}}>
                                                {{col.key === 'player_name' ? (
                                                    <div className="player-cell">
                                                        <img
                                                            src={{player.headshot_url}}
                                                            className="player-headshot"
                                                            alt={{player.player_name}}
                                                            style={{{{ borderColor: getTeamColor(player.team_abbr) }}}}
                                                            onError={{(e) => {{ e.target.style.display = 'none'; }}}}
                                                        />
                                                        <span className="player-name">{{player.player_name}}</span>
                                                    </div>
                                                ) : col.key === 'team_abbr' ? (
                                                    <div className="team-cell">
                                                        <img
                                                            src={{getTeamLogoUrl(player.team_abbr)}}
                                                            className="team-logo"
                                                            alt={{player.team_abbr}}
                                                            title={{player.team_abbr}}
                                                        />
                                                    </div>
                                                ) : col.key === 'position' ? (
                                                    <span className={{`position-badge position-${{player.position}}`}}>
                                                        {{player.position}}
                                                    </span>
                                                ) : col.format ? col.format(player[col.key]) : player[col.key]}}
                                            </td>
                                        ))}}
                                    </tr>
                                ))}}
                            </tbody>
                        </table>
                    </div>

                    <div className="pagination">
                        <div className="pagination-info">
                            Showing {{startIndex + 1}}-{{Math.min(startIndex + itemsPerPage, sortedData.length)}} of {{sortedData.length}} players
                        </div>
                        <div className="pagination-buttons">
                            <button
                                className="pagination-button"
                                onClick={{() => setCurrentPage(prev => Math.max(1, prev - 1))}}
                                disabled={{currentPage === 1}}
                            >
                                Previous
                            </button>
                            <span className="pagination-info">Page {{currentPage}} of {{totalPages}}</span>
                            <button
                                className="pagination-button"
                                onClick={{() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}}
                                disabled={{currentPage === totalPages}}
                            >
                                Next
                            </button>
                        </div>
                    </div>
                </div>
            );
        }}

        function NFLDFSChart() {{
            // Tab state
            const [activeTab, setActiveTab] = useState('chart');
            // Position filter (multi-select)
            const [selectedPositions, setSelectedPositions] = useState([defaultPosition]);
            const [players, setPlayers] = useState(allData[defaultPosition] || []);

            // Axis and size selectors
            const [xAxisStat, setXAxisStat] = useState('boom_pct');
            const [yAxisStat, setYAxisStat] = useState('leverage');
            const [sizeStat, setSizeStat] = useState('ownership_pct');

            // Additional filters
            const [selectedTeams, setSelectedTeams] = useState([]);
            const [salaryRange, setSalaryRange] = useState([3000, 12000]);
            const [ownershipRange, setOwnershipRange] = useState([0, 100]);

            // Zoom state
            const [refAreaLeft, setRefAreaLeft] = useState('');
            const [refAreaRight, setRefAreaRight] = useState('');
            const [refAreaTop, setRefAreaTop] = useState('');
            const [refAreaBottom, setRefAreaBottom] = useState('');
            const [left, setLeft] = useState(null);
            const [right, setRight] = useState(null);
            const [top, setTop] = useState(null);
            const [bottom, setBottom] = useState(null);

            useEffect(() => {{
                // Combine data from all selected positions
                if (selectedPositions.length === 0) {{
                    setPlayers([]);
                    return;
                }}

                // If 'ALL' is selected, use only the ALL dataset
                if (selectedPositions.includes('ALL')) {{
                    setPlayers(allData['ALL'] || []);
                    return;
                }}

                // Otherwise, combine data from selected positions and remove duplicates
                const combined = selectedPositions.flatMap(pos => allData[pos] || []);
                const uniquePlayers = combined.filter((player, index, self) =>
                    index === self.findIndex(p => p.player_id === player.player_id)
                );
                setPlayers(uniquePlayers);
            }}, [selectedPositions]);

            // Extract unique teams from ALL players (not filtered by position)
            const allTeamsData = allData['ALL'] || [];
            const allTeams = [...new Set(allTeamsData.map(p => p.team_abbr))].sort();

            // Apply filters
            const filteredPlayers = players.filter(p => {{
                // Team filter
                if (selectedTeams.length > 0 && !selectedTeams.includes(p.team_abbr)) {{
                    return false;
                }}
                // Salary filter
                if (p.salary < salaryRange[0] || p.salary > salaryRange[1]) {{
                    return false;
                }}
                // Ownership filter
                if (p.ownership_pct < ownershipRange[0] || p.ownership_pct > ownershipRange[1]) {{
                    return false;
                }}
                return true;
            }});

            // Zoom functions
            const zoom = () => {{
                if (refAreaLeft === refAreaRight || refAreaRight === '') {{
                    setRefAreaLeft('');
                    setRefAreaRight('');
                    return;
                }}

                let leftVal = refAreaLeft;
                let rightVal = refAreaRight;
                let topVal = refAreaTop;
                let bottomVal = refAreaBottom;

                if (leftVal > rightVal) [leftVal, rightVal] = [rightVal, leftVal];
                if (bottomVal > topVal) [bottomVal, topVal] = [topVal, bottomVal];

                // Round values to avoid floating point issues
                setLeft(Math.round(leftVal * 100) / 100);
                setRight(Math.round(rightVal * 100) / 100);
                setBottom(Math.round(bottomVal * 100) / 100);
                setTop(Math.round(topVal * 100) / 100);
                setRefAreaLeft('');
                setRefAreaRight('');
                setRefAreaTop('');
                setRefAreaBottom('');
            }};

            const zoomOut = () => {{
                setLeft(null);
                setRight(null);
                setTop(null);
                setBottom(null);
                setRefAreaLeft('');
                setRefAreaRight('');
                setRefAreaTop('');
                setRefAreaBottom('');
            }};

            const clearFilters = () => {{
                setSelectedPositions([defaultPosition]);
                setSelectedTeams([]);
                setSalaryRange([3000, 12000]);
                setOwnershipRange([0, 100]);
            }};

            const togglePosition = (position) => {{
                setSelectedPositions(prev => {{
                    if (prev.includes(position)) {{
                        // Don't allow deselecting all positions
                        if (prev.length === 1) return prev;
                        return prev.filter(p => p !== position);
                    }} else {{
                        return [...prev, position];
                    }}
                }});
            }};

            const toggleTeam = (team) => {{
                setSelectedTeams(prev => {{
                    if (prev.includes(team)) {{
                        return prev.filter(t => t !== team);
                    }} else {{
                        return [...prev, team];
                    }}
                }});
            }};

            if (filteredPlayers.length === 0) {{
                return (
                    <div className="container">
                        <div className="chart-title">No players available</div>
                    </div>
                );
            }}

            // Calculate ranges and quartiles based on selected stats
            const xValues = filteredPlayers.map(p => p[xAxisStat]).sort((a, b) => a - b);
            const yValues = filteredPlayers.map(p => p[yAxisStat]).sort((a, b) => a - b);
            const sizeValues = filteredPlayers.map(p => p[sizeStat]);

            const xMedian = xValues[Math.floor(xValues.length * 0.5)];
            const x75th = xValues[Math.floor(xValues.length * 0.75)];
            const y75th = yValues[Math.floor(yValues.length * 0.75)];

            // Get dynamic axis labels
            const xAxisLabel = statOptions.find(s => s.value === xAxisStat)?.label.toUpperCase() || 'X-AXIS';
            const yAxisLabel = statOptions.find(s => s.value === yAxisStat)?.label.toUpperCase() || 'Y-AXIS';
            const sizeLabel = statOptions.find(s => s.value === sizeStat)?.label || 'Size';

            const minSize = Math.min(...sizeValues);
            const maxSize = Math.max(...sizeValues);

            // Calculate clean axis domains with padding
            const xMin = Math.min(...xValues);
            const xMax = Math.max(...xValues);
            const yMin = Math.min(...yValues);
            const yMax = Math.max(...yValues);

            // Default domains with padding (use when not zoomed)
            const defaultLeft = Math.floor(xMin - Math.abs(xMin * 0.05));
            const defaultRight = Math.ceil(xMax + Math.abs(xMax * 0.05));
            const defaultBottom = Math.floor(yMin - Math.abs(yMin * 0.05));
            const defaultTop = Math.ceil(yMax + Math.abs(yMax * 0.05));

            // Prepare chart data with colors based on quadrant
            const chartData = filteredPlayers.map(p => {{
                const sizeNormalized = (p[sizeStat] - minSize) / (maxSize - minSize);

                // Determine Y-axis midpoint (0 for leverage, median for others)
                const yMidpoint = yAxisStat === 'leverage' ? 0 : xMedian;

                // Color by quadrant
                let color;
                if (p[xAxisStat] >= xMedian && p[yAxisStat] >= yMidpoint) {{
                    // Top-right: High X, High Y - Green
                    color = '#059669'; // darker green
                }} else if (p[xAxisStat] < xMedian && p[yAxisStat] >= yMidpoint) {{
                    // Top-left: Low X, High Y - Yellow/Amber
                    color = '#d97706'; // darker amber
                }} else if (p[xAxisStat] >= xMedian && p[yAxisStat] < yMidpoint) {{
                    // Bottom-right: High X, Low Y - Grey
                    color = '#6b7280'; // darker grey
                }} else {{
                    // Bottom-left: Low X, Low Y - Red
                    color = '#dc2626'; // darker red
                }}

                return {{
                    ...p,
                    x: p[xAxisStat],
                    y: p[yAxisStat],
                    rawSize: p[sizeStat],
                    color: color,
                    intensity: 0.85
                }};
            }});

            // Custom shape for player headshots
            const PlayerHeadshot = (props) => {{
                const {{ cx, cy, payload, index }} = props;

                const sizeNormalized = (payload.rawSize - minSize) / (maxSize - minSize);
                const size = 24 + (sizeNormalized * 24);
                const radius = size / 2;

                const borderOpacity = payload.intensity;
                const glowOpacity = payload.intensity * 0.3;

                // Extract last name
                const nameParts = payload.player_name.split(' ');
                let lastName = payload.player_name;
                if (nameParts.length > 1) {{
                    const lastPart = nameParts[nameParts.length - 1];
                    const suffixes = ['Jr.', 'Sr.', 'II', 'III', 'IV', 'V'];
                    if (suffixes.includes(lastPart) && nameParts.length > 2) {{
                        lastName = nameParts[nameParts.length - 2];
                    }} else {{
                        lastName = lastPart;
                    }}
                }}

                // Only show labels for top performers (above 75th percentile in either axis)
                const showLabel = payload.x >= x75th || payload.y >= y75th;

                // Smart label positioning to avoid overlaps
                const nearbyPlayers = chartData.filter((other, idx) => {{
                    if (idx === index) return false;
                    const distance = Math.sqrt(
                        Math.pow(other.x - payload.x, 2) +
                        Math.pow(other.y - payload.y, 2)
                    );
                    return distance < 3; // Within 3 units
                }});

                // Default position: below
                let labelX = cx;
                let labelY = cy + radius + 12;
                let labelAnchor = 'middle';

                // If crowded, use hash-based positioning
                if (nearbyPlayers.length > 0) {{
                    const hash = payload.player_id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 4;
                    if (hash === 0) {{
                        // Below-right
                        labelX = cx + radius + 5;
                        labelY = cy + radius + 8;
                        labelAnchor = 'start';
                    }} else if (hash === 1) {{
                        // Below-left
                        labelX = cx - radius - 5;
                        labelY = cy + radius + 8;
                        labelAnchor = 'end';
                    }} else if (hash === 2) {{
                        // Above
                        labelY = cy - radius - 4;
                    }} else {{
                        // Below with extra offset
                        labelY = cy + radius + 18;
                    }}
                }}

                // Team logo watermark
                const teamLogoUrl = `https://a.espncdn.com/i/teamlogos/nfl/500/${{payload.team_abbr.toUpperCase()}}.png`;
                const watermarkSize = size * 1.3;

                return (
                    <g>
                        <circle
                            cx={{cx}}
                            cy={{cy}}
                            r={{radius + 2}}
                            fill={{payload.color}}
                            opacity={{glowOpacity}}
                        />
                        <defs>
                            <clipPath id={{`clip-${{payload.player_id}}`}}>
                                <circle cx={{cx}} cy={{cy}} r={{radius}} />
                            </clipPath>
                            <clipPath id={{`clip-watermark-${{payload.player_id}}`}}>
                                <circle cx={{cx}} cy={{cy}} r={{radius}} />
                            </clipPath>
                        </defs>
                        <circle
                            cx={{cx}}
                            cy={{cy}}
                            r={{radius}}
                            fill="white"
                        />
                        <image
                            x={{cx - watermarkSize / 2}}
                            y={{cy - watermarkSize / 2}}
                            width={{watermarkSize}}
                            height={{watermarkSize}}
                            href={{teamLogoUrl}}
                            clipPath={{`url(#clip-watermark-${{payload.player_id}})`}}
                            opacity={{0.18}}
                            preserveAspectRatio="xMidYMid meet"
                        />
                        <image
                            x={{cx - radius}}
                            y={{cy - radius}}
                            width={{size}}
                            height={{size}}
                            href={{payload.headshot_url}}
                            clipPath={{`url(#clip-${{payload.player_id}})`}}
                            preserveAspectRatio="xMidYMid slice"
                            opacity={{0.9}}
                        />
                        <circle
                            cx={{cx}}
                            cy={{cy}}
                            r={{radius}}
                            fill="none"
                            stroke={{payload.color}}
                            strokeWidth={{2.5}}
                            opacity={{borderOpacity}}
                        />
                        {{showLabel && (
                            <>
                                <text
                                    x={{labelX}}
                                    y={{labelY}}
                                    textAnchor={{labelAnchor}}
                                    fill="white"
                                    fontSize="10"
                                    fontWeight="700"
                                    opacity={{0.8}}
                                    stroke="white"
                                    strokeWidth="4"
                                    style={{{{ pointerEvents: 'none', fontFamily: 'Roboto Condensed, Arial Narrow, sans-serif', letterSpacing: '0.5px' }}}}
                                >
                                    {{lastName.toUpperCase()}}
                                </text>
                                <text
                                    x={{labelX}}
                                    y={{labelY}}
                                    textAnchor={{labelAnchor}}
                                    fill="#0f172a"
                                    fontSize="10"
                                    fontWeight="700"
                                    opacity={{1}}
                                    style={{{{ pointerEvents: 'none', fontFamily: 'Roboto Condensed, Arial Narrow, sans-serif', letterSpacing: '0.5px' }}}}
                                >
                                    {{lastName.toUpperCase()}}
                                </text>
                            </>
                        )}}
                    </g>
                );
            }};

            return (
                <div className="container">
                    <div className="chart-title">
                        Stokastic NFL Boom/Bust Analysis
                    </div>

                    {{/* Tab Navigation - At the Top */}}
                    <div className="tab-navigation">
                        <button
                            className={{`tab-button ${{activeTab === 'chart' ? 'active' : ''}}`}}
                            onClick={{() => setActiveTab('chart')}}
                        >
                            Chart View
                        </button>
                        <button
                            className={{`tab-button ${{activeTab === 'table' ? 'active' : ''}}`}}
                            onClick={{() => setActiveTab('table')}}
                        >
                            Data Table
                        </button>
                    </div>

                    {{/* Chart Tab Content */}}
                    <div className={{`tab-content ${{activeTab === 'chart' ? 'active' : ''}}`}}>
                        <div className="filters-container">
                            {{/* Group 1: Position Filters */}}
                            <div className="filter-group">
                                <div className="filter-group-header">
                                    Positions
                                </div>
                                <div className="filter-group-content">
                                    <div className="position-badges-container">
                                        {{positions.map(pos => (
                                            <div
                                                key={{pos}}
                                                className={{`position-toggle position-${{pos}} ${{selectedPositions.includes(pos) ? 'active' : 'inactive'}}`}}
                                                onClick={{() => togglePosition(pos)}}
                                            >
                                                {{pos}}
                                            </div>
                                        ))}}
                                    </div>
                                </div>
                            </div>

                        {{/* Group 2: Team Filters */}}
                        <div className="filter-group">
                            <div className="filter-group-header">
                                Teams
                            </div>
                            <div className="filter-group-content">
                                <div className="team-logos-container">
                                    {{/* First Row - Half of teams */}}
                                    <div className="team-logos-row">
                                        {{allTeams.slice(0, Math.ceil(allTeams.length / 2)).map(team => (
                                            <img
                                                key={{team}}
                                                src={{getTeamLogoUrl(team)}}
                                                alt={{team}}
                                                title={{team}}
                                                className={{`team-logo-toggle ${{selectedTeams.includes(team) ? 'active' : 'inactive'}}`}}
                                                onClick={{() => toggleTeam(team)}}
                                            />
                                        ))}}
                                    </div>
                                    {{/* Second Row - Other half of teams */}}
                                    <div className="team-logos-row">
                                        {{allTeams.slice(Math.ceil(allTeams.length / 2)).map(team => (
                                            <img
                                                key={{team}}
                                                src={{getTeamLogoUrl(team)}}
                                                alt={{team}}
                                                title={{team}}
                                                className={{`team-logo-toggle ${{selectedTeams.includes(team) ? 'active' : 'inactive'}}`}}
                                                onClick={{() => toggleTeam(team)}}
                                            />
                                        ))}}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {{/* Group 3: Player Filters */}}
                        <div className="filter-group">
                            <div className="filter-group-header">
                                Player Filters
                            </div>
                            <div className="filter-group-content">

                                <div className="filter-item">
                                    <label>Salary Range</label>
                                    <div className="range-values">
                                        <span>${{(salaryRange[0]/1000).toFixed(1)}}K</span>
                                        <span>${{(salaryRange[1]/1000).toFixed(1)}}K</span>
                                    </div>
                                    <div className="slider-container">
                                        <input
                                            type="range"
                                            min="3000"
                                            max="12000"
                                            step="100"
                                            value={{salaryRange[0]}}
                                            onChange={{(e) => {{
                                                const val = parseInt(e.target.value);
                                                if (val < salaryRange[1]) {{
                                                    setSalaryRange([val, salaryRange[1]]);
                                                }}
                                            }}}}
                                        />
                                        <input
                                            type="range"
                                            min="3000"
                                            max="12000"
                                            step="100"
                                            value={{salaryRange[1]}}
                                            onChange={{(e) => {{
                                                const val = parseInt(e.target.value);
                                                if (val > salaryRange[0]) {{
                                                    setSalaryRange([salaryRange[0], val]);
                                                }}
                                            }}}}
                                        />
                                    </div>
                                </div>

                                <div className="filter-item">
                                    <label>Ownership Range</label>
                                    <div className="range-values">
                                        <span>{{ownershipRange[0]}}%</span>
                                        <span>{{ownershipRange[1]}}%</span>
                                    </div>
                                    <div className="slider-container">
                                        <input
                                            type="range"
                                            min="0"
                                            max="100"
                                            step="1"
                                            value={{ownershipRange[0]}}
                                            onChange={{(e) => {{
                                                const val = parseInt(e.target.value);
                                                if (val < ownershipRange[1]) {{
                                                    setOwnershipRange([val, ownershipRange[1]]);
                                                }}
                                            }}}}
                                        />
                                        <input
                                            type="range"
                                            min="0"
                                            max="100"
                                            step="1"
                                            value={{ownershipRange[1]}}
                                            onChange={{(e) => {{
                                                const val = parseInt(e.target.value);
                                                if (val > ownershipRange[0]) {{
                                                    setOwnershipRange([ownershipRange[0], val]);
                                                }}
                                            }}}}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                        {{/* Group 4: Chart Configuration & Actions */}}
                        <div className="filter-group">
                            <div className="filter-group-header">
                                Chart Configuration
                            </div>
                            <div className="filter-group-content">
                                <div className="filter-item">
                                    <label>X-Axis</label>
                                    <select value={{xAxisStat}} onChange={{(e) => setXAxisStat(e.target.value)}}>
                                        {{statOptions.map(stat => (
                                            <option key={{stat.value}} value={{stat.value}}>{{stat.label}}</option>
                                        ))}}
                                    </select>
                                </div>

                                <div className="filter-item">
                                    <label>Y-Axis</label>
                                    <select value={{yAxisStat}} onChange={{(e) => setYAxisStat(e.target.value)}}>
                                        {{statOptions.map(stat => (
                                            <option key={{stat.value}} value={{stat.value}}>{{stat.label}}</option>
                                        ))}}
                                    </select>
                                </div>

                                <div className="filter-item">
                                    <label>Bubble Size</label>
                                    <select value={{sizeStat}} onChange={{(e) => setSizeStat(e.target.value)}}>
                                        {{statOptions.map(stat => (
                                            <option key={{stat.value}} value={{stat.value}}>{{stat.label}}</option>
                                        ))}}
                                    </select>
                                </div>

                                <div className="button-group">
                                    <button className="btn-primary" onClick={{zoomOut}}>
                                        Reset Zoom
                                    </button>
                                    <button className="btn-secondary" onClick={{clearFilters}}>
                                        Clear Filters
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="info-text">
                            {{filteredPlayers.length}} players ({{players.length}} total) • Median {{xAxisLabel}}: {{xMedian.toFixed(1)}} | {{yAxisLabel}} at 0
                            <br />
                            Size = {{sizeLabel}} | Color = Quadrant (🟢 Best, 🟡 Contrarian, ⚪ Popular, 🔴 Avoid) | Drag to zoom, Reset Zoom to clear
                        </div>

                        <div id="chart-export-area">
                        <ResponsiveContainer width="100%" height={{700}}>
                        <ScatterChart
                            margin={{{{ top: 40, right: 120, bottom: 60, left: 60 }}}}
                            onMouseDown={{(e) => {{
                                if (e) {{
                                    setRefAreaLeft(e.xValue);
                                    setRefAreaTop(e.yValue);
                                }}
                            }}}}
                            onMouseMove={{(e) => {{
                                if (refAreaLeft && e) {{
                                    setRefAreaRight(e.xValue);
                                    setRefAreaBottom(e.yValue);
                                }}
                            }}}}
                            onMouseUp={{zoom}}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" strokeWidth={{1.5}} />
                            <XAxis
                                type="number"
                                dataKey="x"
                                name={{xAxisLabel}}
                                label={{{{ value: xAxisLabel, position: 'bottom', style: {{ fill: '#0f172a', fontWeight: '800', fontSize: 15, fontFamily: 'Oswald, Impact, sans-serif', letterSpacing: '1px' }} }}}}
                                tick={{{{ fill: '#1f2937', fontWeight: 700, fontFamily: 'Roboto Condensed, sans-serif' }}}}
                                stroke="#4b5563"
                                strokeWidth={{2}}
                                allowDataOverflow={{true}}
                                domain={{[left !== null ? left : defaultLeft, right !== null ? right : defaultRight]}}
                            />
                            <YAxis
                                type="number"
                                dataKey="y"
                                name={{yAxisLabel}}
                                label={{{{ value: yAxisLabel, angle: -90, position: 'left', style: {{ fill: '#0f172a', fontWeight: '800', fontSize: 15, fontFamily: 'Oswald, Impact, sans-serif', letterSpacing: '1px' }} }}}}
                                tick={{{{ fill: '#1f2937', fontWeight: 700, fontFamily: 'Roboto Condensed, sans-serif' }}}}
                                stroke="#4b5563"
                                strokeWidth={{2}}
                                allowDataOverflow={{true}}
                                domain={{[bottom !== null ? bottom : defaultBottom, top !== null ? top : defaultTop]}}
                            />
                            <Tooltip cursor={{{{ strokeDasharray: '3 3' }}}} />

                            {{/* Quadrant backgrounds */}}
                            <ReferenceArea
                                x1={{defaultLeft}}
                                x2={{xMedian}}
                                y1={{defaultBottom}}
                                y2={{0}}
                                fill="#ef4444"
                                fillOpacity={{0.03}}
                                ifOverflow="visible"
                            />
                            <ReferenceArea
                                x1={{xMedian}}
                                x2={{defaultRight}}
                                y1={{defaultBottom}}
                                y2={{0}}
                                fill="#9ca3af"
                                fillOpacity={{0.04}}
                                ifOverflow="visible"
                            />
                            <ReferenceArea
                                x1={{defaultLeft}}
                                x2={{xMedian}}
                                y1={{0}}
                                y2={{defaultTop}}
                                fill="#fbbf24"
                                fillOpacity={{0.04}}
                                ifOverflow="visible"
                            />
                            <ReferenceArea
                                x1={{xMedian}}
                                x2={{defaultRight}}
                                y1={{0}}
                                y2={{defaultTop}}
                                fill="#10b981"
                                fillOpacity={{0.05}}
                                ifOverflow="visible"
                            />

                            <ReferenceLine x={{xMedian}} stroke="#9ca3af" strokeDasharray="5 5" strokeWidth={{1.5}} opacity={{0.5}} />
                            <ReferenceLine y={{0}} stroke="#9ca3af" strokeDasharray="5 5" strokeWidth={{1.5}} opacity={{0.5}} />

                            <Scatter data={{chartData}} shape={{PlayerHeadshot}} />

                            {{refAreaLeft && refAreaRight && (
                                <ReferenceArea
                                    x1={{refAreaLeft}}
                                    x2={{refAreaRight}}
                                    y1={{refAreaTop}}
                                    y2={{refAreaBottom}}
                                    strokeOpacity={{0.3}}
                                    fill="#3b82f6"
                                    fillOpacity={{0.3}}
                                />
                            )}}
                        </ScatterChart>
                    </ResponsiveContainer>
                        </div>
                    </div>

                    {{/* Data Table Tab Content */}}
                    <div className={{`tab-content ${{activeTab === 'table' ? 'active' : ''}}`}}>
                        <DataTable />
                    </div>
                </div>
            );
        }}

        // Render
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<NFLDFSChart />);
    </script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description='Create NFL DFS visualizations using React/Recharts')
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--position', default='ALL', help='Position filter (QB, RB, WR, TE, DST, or ALL)')
    parser.add_argument('--output', default='boom_bust.html', help='Output filename')

    args = parser.parse_args()

    visualizer = NFLDFSVisualizer(args.csv)
    visualizer.create_visualization(args.position, args.output)


if __name__ == '__main__':
    main()
