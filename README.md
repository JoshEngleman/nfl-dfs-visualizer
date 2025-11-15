# NFL DFS Boom/Bust Visualizer

A command-line tool and web application that generates professional-quality scatter plot visualizations of NFL DraftKings player data with player headshots and team logos.

![Example Visualization](example_output.png)

## 🌐 Web Application (Recommended)

The easiest way to use this tool is through the **web interface**:

👉 **Visit: [https://joshengleman.com/nfl-dfs/](https://joshengleman.com/nfl-dfs/)**

**Features:**
- 📤 Upload CSV files directly in your browser
- 🖼️ Automatic player headshot loading
- 💾 Data persists in browser localStorage
- 📱 Works on any device (desktop, mobile, tablet)
- ⚡️ No installation required

**Workflow:**
1. Visit the website
2. Click "Upload CSV"
3. Select your DraftKings CSV file
4. Done! (~30 seconds)

See [docs/SIMPLE_WORKFLOW.md](docs/SIMPLE_WORKFLOW.md) for the complete user guide.

---

## 🖥️ Command-Line Tool (Legacy)

For advanced users who prefer local image generation:

### Features

- **Player Headshots**: Automatically fetches and displays circular player images from ESPN
- **Team Logos**: Shows team logos for DST positions
- **Ownership-Based Sizing**: Player images scale with projected ownership percentage
- **Position Filtering**: Generate visualizations for specific positions (QB, RB, WR, TE, DST) or all players
- **Quadrant Analysis**: Visual quadrants showing boom/leverage relationships
- **Professional Styling**: Clean design with reference lines, grid, and color coding

## Installation

1. Clone or download this repository
2. Install **uv** (fast Python package manager):

```bash
brew install uv
```

3. Create virtual environment and install dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```

**Note**: This project uses **uv** for faster package management. All Python scripts can be run using `.venv/bin/python` or the provided wrapper scripts.

### Dependencies

- pandas >= 2.0.0
- matplotlib >= 3.7.0
- Pillow >= 10.0.0
- requests >= 2.31.0
- nflreadr >= 0.1.0
- numpy >= 1.24.0

## Usage

### Basic Usage

Generate a visualization for all players:

```bash
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv"
```

### Filter by Position

Generate visualizations for specific positions:

```bash
# Quarterbacks only
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position QB

# Running backs only
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position RB

# Wide receivers only
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position WR

# Tight ends only
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position TE

# Defenses only
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position DST
```

### Custom Output Path

Specify a custom output file:

```bash
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position QB --output my_qb_analysis.png
```

## Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--csv` | Yes | - | Path to CSV file with DFS data |
| `--position` | No | `ALL` | Position filter: ALL, QB, RB, WR, TE, or DST |
| `--output` | No | `boom_bust_{position}.png` | Output file path |

## CSV Format

The tool expects a CSV file with the following columns:

- `Name`: Player name
- `Team`: Team abbreviation
- `Salary`: Player salary (e.g., "$9,000")
- `Position`: Position (QB, RB, WR, TE, DST)
- `Projection`: Projected fantasy points
- `Std Dev`: Standard deviation
- `Ceiling`: Points ceiling
- `Bust%`: Bust percentage
- `Boom%`: Boom percentage
- `Slate`: Slate type (Main, etc.)
- `Own%`: Projected ownership percentage
- `Optimal%`: Optimal lineup percentage
- `Leverage`: Leverage score

## How It Works

### 1. Player Headshots

The tool uses the **nflreadr** package to match player names to ESPN player IDs, then fetches headshots from ESPN's CDN:

```
https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png
```

### 2. Team Logos

For DST positions, team logos are fetched from ESPN:

```
https://a.espncdn.com/i/teamlogos/nfl/500/{team_abbr}.png
```

### 3. Image Sizing

Player images are sized based on projected ownership percentage:
- **Larger images** = Higher projected ownership
- **Smaller images** = Lower projected ownership

This provides an additional visual dimension to quickly identify "chalky" plays.

### 4. Quadrant Analysis

The visualization divides players into four quadrants based on median Boom% and Leverage:

- **Top Right**: High Boom%, High Leverage (optimal targets)
- **Top Left**: Low Boom%, High Leverage (contrarian plays)
- **Bottom Right**: High Boom%, Low Leverage (chalky plays)
- **Bottom Left**: Low Boom%, Low Leverage (avoid)

## Output

The tool generates high-resolution PNG images (300 DPI) suitable for:
- Social media sharing
- Research reports
- Presentation slides
- Personal reference

Default output files are named: `boom_bust_{POSITION}.png`

## Troubleshooting

### Player Images Not Showing

If player headshots aren't appearing:

1. **Check internet connection**: Images are fetched from ESPN's servers
2. **Player name matching**: The tool attempts to match player names with ESPN's roster database
3. **Fallback to colored circles**: If a headshot can't be found, a colored circle with position-based color will be used

### Common Issues

**"nflreadr not installed"**
- Run: `pip install nflreadr`

**Images too large/small**
- Image sizing is automatic based on ownership %. Check that your CSV has valid `Own%` values

**No players found for position**
- Verify that the `Position` column in your CSV matches exactly: QB, RB, WR, TE, or DST

## Examples

### Generate All Positions

```bash
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position ALL
```

Output: `boom_bust_ALL.png`

### Generate QB Analysis

```bash
.venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position QB
```

Output: `boom_bust_QB.png`

### Batch Generate All Positions

```bash
for pos in QB RB WR TE DST; do
    .venv/bin/python src/nfl_dfs_visualizer.py --csv "data/NFL DK Boom Bust.csv" --position $pos
done
```

## Advanced Customization

To customize the visualization (colors, sizing, layout), edit the `nfl_dfs_visualizer.py` file:

- **Position colors**: Modify `pos_colors` dictionary in `_create_placeholder_image()`
- **Image sizing**: Adjust `base_size` and `scale_factor` in `_calculate_image_size()`
- **Quadrant lines**: Modify median calculations in `create_visualization()`
- **Figure size**: Change `figsize` parameter in `plt.subplots()`

## Credits

- **Data Source**: User-provided DraftKings data
- **Player Images**: ESPN API
- **NFL Data**: nflreadr package (nflverse community)

## License

This tool is provided as-is for personal use. NFL player images and team logos are trademarks of their respective organizations.

## Contributing

Feel free to submit issues or pull requests to improve the tool!

## 🔧 Developer/Maintainer Workflows

### Updating Player Headshots

When new players appear in CSV files who don't have headshots yet:

```bash
# Download new player headshots from CSV
.venv/bin/python src/update_headshots_from_csv.py data/your-file.csv

# Deploy to server
./deploy.sh headshots
```

This automatically:
- Identifies players without cached headshots
- Downloads from NFL.com (with name mapping support)
- Compresses images to ~60KB each
- Uploads to GoDaddy server via FTP

See [docs/HEADSHOT_UPDATE_WORKFLOW.md](docs/HEADSHOT_UPDATE_WORKFLOW.md) for complete details.

### Deployment Commands

```bash
# Deploy only the website (index.html)
./deploy.sh website

# Deploy only headshots
./deploy.sh headshots

# Deploy everything (website + headshots)
./deploy.sh all
```

See [docs/DEPLOYMENT_SETUP.md](docs/DEPLOYMENT_SETUP.md) for setup instructions.

### Name Mapping

Players with suffixes (Sr., Jr., III) may need mappings in `name_mappings.json`:

```json
{
  "mappings": {
    "Ray-Ray McCloud III|NYG": "Ray-Ray McCloud",
    "Kyle Pitts Sr.|ATL": "Kyle Pitts"
  }
}
```

See [docs/NAME_MATCHING_GUIDE.md](docs/NAME_MATCHING_GUIDE.md) for details.

---

## Future Enhancements

Potential improvements:
- Multiple metric comparisons (Projection vs Salary, etc.)
- Salary range filtering
- Export to multiple formats (SVG, PDF)
- Player name search/highlighting
- Custom color schemes
