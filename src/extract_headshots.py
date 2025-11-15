#!/usr/bin/env python3
"""
Download headshots from index.html embedded URLs and save as PNG files.
This is a one-time script to populate the headshot_cache folder.
"""

import json
import re
import os
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

def download_headshots_from_html(html_file, output_dir):
    """Download all headshots from URLs in HTML and save as PNG files."""

    print(f"Reading {html_file}...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ORIGINAL_DATA JSON
    # Look for: const ORIGINAL_DATA = {"ALL": [...]}
    pattern = r'const ORIGINAL_DATA = (\{.*?\});'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("ERROR: Could not find ORIGINAL_DATA in HTML file")
        return

    print("Found ORIGINAL_DATA, parsing JSON...")
    data_json = match.group(1)

    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON: {e}")
        return

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_path.absolute()}")

    # Download headshots
    all_players = data.get('ALL', [])
    print(f"Found {len(all_players)} players in data")
    print("Downloading headshots...\n")

    downloaded = 0
    skipped = 0
    failed = 0

    for player in all_players:
        player_name = player.get('player_name', 'Unknown')
        headshot_url = player.get('headshot_url', '')

        # Clean player name for filename
        clean_name = player_name.replace("'", "").replace(".", "")
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', clean_name)
        clean_name = clean_name.replace(' ', '_')

        filename = f"{clean_name}.png"
        filepath = output_path / filename

        # Check if it's a valid URL
        if headshot_url and (headshot_url.startswith('http://') or headshot_url.startswith('https://')):
            try:
                # Download image
                response = requests.get(headshot_url, timeout=10)
                response.raise_for_status()

                # Open image and save as PNG
                img = Image.open(BytesIO(response.content))
                img.save(filepath, 'PNG')

                downloaded += 1
                if downloaded % 10 == 0:
                    print(f"  Downloaded {downloaded}/{len(all_players)} headshots...")

            except requests.exceptions.RequestException as e:
                print(f"  ❌ Failed to download {player_name}: {e}")
                failed += 1
            except Exception as e:
                print(f"  ❌ Error processing {player_name}: {e}")
                failed += 1
        else:
            # Not a valid URL, skip
            skipped += 1

    print(f"\n✅ Download complete!")
    print(f"   Downloaded: {downloaded} headshots")
    print(f"   Failed: {failed} downloads")
    print(f"   Skipped: {skipped} players (no URL)")
    print(f"   Location: {output_path.absolute()}")
    print(f"\nNext step: Upload these files to GoDaddy at /nfl-dfs/headshots/")

if __name__ == '__main__':
    # Configuration
    html_file = 'index.html'
    output_dir = 'headshot_cache'

    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"ERROR: {html_file} not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        exit(1)

    # Check required packages
    try:
        import requests
        from PIL import Image
    except ImportError as e:
        print(f"ERROR: Missing required package: {e}")
        print("Install with: pip install requests pillow")
        exit(1)

    # Run download
    download_headshots_from_html(html_file, output_dir)
