#!/usr/bin/env python3
"""
Download headshots for new players from CSV who don't already have images.
Scrapes NFL.com player pages to fetch headshots automatically.
"""

import csv
import sys
import os
import re
import json
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

def load_name_mappings(mappings_file='name_mappings.json'):
    """
    Load name mappings from JSON file.
    Returns dict mapping "Player Name|TEAM" -> "Mapped Name"
    """
    try:
        if os.path.exists(mappings_file):
            with open(mappings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('mappings', {})
    except Exception as e:
        print(f"Warning: Could not load name mappings: {e}")
    return {}

def apply_name_mapping(player_name, team_abbr, name_mappings):
    """
    Apply name mapping if one exists for this player.
    Returns mapped name if found, otherwise original name.
    """
    if not name_mappings:
        return player_name

    mapping_key = f"{player_name}|{team_abbr}"
    if mapping_key in name_mappings:
        mapped_name = name_mappings[mapping_key]
        print(f"    → Applying name mapping: '{player_name}' → '{mapped_name}'")
        return mapped_name

    return player_name

def clean_player_name(name):
    """
    Clean player name for filename (same logic as extract_headshots.py and index.html).
    Removes special characters and replaces spaces with underscores.
    """
    clean = name.replace("'", "").replace(".", "")
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', clean)
    clean = clean.replace(' ', '_')
    return clean

def fetch_headshot_from_nfl(player_name, team_abbr=None):
    """
    Fetch player headshot from NFL.com by scraping player page.
    Returns image URL if found, None otherwise.
    """
    try:
        # Convert player name to NFL.com URL format
        # "Brock Purdy" -> "brock-purdy"
        url_name = player_name.lower().replace(' ', '-').replace("'", '').replace('.', '')

        # Fetch NFL.com player page
        player_url = f"https://www.nfl.com/players/{url_name}/"
        response = requests.get(player_url, timeout=10)
        response.raise_for_status()

        # Search for headshot URL in page content
        # Pattern: https://static.www.nfl.com/image/upload/t_headshot_desktop/league/{id}
        import re
        pattern = r'https://static\.www\.nfl\.com/image/upload/t_headshot_desktop/league/([a-z0-9]+)'
        match = re.search(pattern, response.text)

        if match:
            headshot_id = match.group(1)
            # Construct URL with f_auto,q_auto (same format as existing headshots)
            headshot_url = f"https://static.www.nfl.com/image/upload/f_auto,q_auto/league/{headshot_id}"
            return headshot_url

        return None

    except Exception as e:
        return None

def compress_and_save(img_url, output_path, max_size=400, quality=85):
    """
    Download image from URL, compress it, and save as PNG.
    Same compression logic as compress_headshots.py.
    """
    try:
        # Download image
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()

        # Open image
        img = Image.open(BytesIO(response.content))

        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # Resize if needed (maintain aspect ratio)
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Save as optimized PNG
        img.save(output_path, 'PNG', optimize=True)

        # If still too large, convert to JPEG (but keep .png extension)
        compressed_size = output_path.stat().st_size
        if compressed_size > 200_000:  # If larger than 200KB
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

        return True

    except Exception as e:
        print(f"    Error saving image: {e}")
        return False

def detect_column_name(headers, possible_names):
    """
    Detect column name from list of possible variations.
    Returns the actual column name found, or None.
    """
    headers_lower = [h.lower().strip() for h in headers]
    for possible in possible_names:
        if possible.lower() in headers_lower:
            idx = headers_lower.index(possible.lower())
            return headers[idx]
    return None

def update_headshots_from_csv(csv_file, output_dir='headshot_cache_compressed'):
    """
    Download headshots for players in CSV who don't already have images.
    """
    print("=" * 60)
    print("Automated Headshot Downloader for CSV Players")
    print("=" * 60)
    print()

    # Load name mappings
    name_mappings = load_name_mappings()
    if name_mappings:
        print(f"Loaded {len(name_mappings)} name mappings")
        for key, value in name_mappings.items():
            print(f"  {key} → {value}")
        print()
    else:
        print("No name mappings found (name_mappings.json not found or empty)")
        print()

    # Check if CSV exists
    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file not found: {csv_file}")
        return

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read CSV
    print(f"Reading CSV: {csv_file}")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        # Detect column names (same logic as index.html)
        name_col = detect_column_name(headers, ['Name', 'player_name', 'Player', 'PLAYER'])
        team_col = detect_column_name(headers, ['Team', 'team_abbr', 'Tm', 'TM'])

        if not name_col:
            print("ERROR: Could not find player name column in CSV")
            print(f"Available columns: {', '.join(headers)}")
            return

        print(f"Detected columns: Name='{name_col}', Team='{team_col or 'N/A'}'")
        print()

        # Process players
        players = list(reader)
        total = len(players)
        downloaded = 0
        skipped = 0
        failed = 0
        failed_players = []

        print(f"Found {total} players in CSV")
        print(f"Output directory: {output_path.absolute()}")
        print()
        print("Processing players...")
        print()

        for i, row in enumerate(players, 1):
            player_name = row.get(name_col, '').strip()
            team_abbr = row.get(team_col, '').strip() if team_col else None

            if not player_name:
                continue

            # Apply name mapping if one exists
            mapped_name = apply_name_mapping(player_name, team_abbr, name_mappings)

            # Clean name for filename (use mapped name)
            clean_name = clean_player_name(mapped_name)
            filename = f"{clean_name}.png"
            filepath = output_path / filename

            # Check if already exists
            if filepath.exists():
                skipped += 1
                continue

            # Download from NFL.com (use mapped name for URL)
            print(f"[{i}/{total}] {player_name} ({team_abbr or 'N/A'})...")
            headshot_url = fetch_headshot_from_nfl(mapped_name, team_abbr)

            if headshot_url:
                print(f"    Found: {headshot_url}")
                if compress_and_save(headshot_url, filepath):
                    print(f"    ✅ Saved: {filename}")
                    downloaded += 1
                else:
                    print(f"    ❌ Failed to save")
                    failed += 1
                    failed_players.append(player_name)
            else:
                print(f"    ❌ No headshot found on NFL.com")
                failed += 1
                failed_players.append(player_name)

            # Be nice to NFL.com servers
            time.sleep(0.5)

        # Summary
        print()
        print("=" * 60)
        print("✅ Processing Complete!")
        print("=" * 60)
        print(f"Downloaded:  {downloaded} new headshots")
        print(f"Skipped:     {skipped} (already exist)")
        print(f"Failed:      {failed} (not found or error)")
        print()

        if failed_players:
            print("Failed players:")
            for player in failed_players:
                print(f"  - {player}")
            print()

        print(f"Headshots saved to: {output_path.absolute()}")
        print()
        print("Next steps:")
        print("1. Upload new headshots to GoDaddy at /nfl-dfs/headshots/")
        print("2. Headshots will load automatically on your website")
        print()

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 update_headshots_from_csv.py <csv_file>")
        print()
        print("Example:")
        print("  python3 update_headshots_from_csv.py weekly_dfs_data.csv")
        print()
        sys.exit(1)

    csv_file = sys.argv[1]

    # Check required packages
    try:
        import requests
        from PIL import Image
    except ImportError as e:
        print(f"ERROR: Missing required package: {e}")
        print("Install with: pip install requests pillow")
        sys.exit(1)

    # Run
    update_headshots_from_csv(csv_file)
