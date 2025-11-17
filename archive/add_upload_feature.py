#!/usr/bin/env python3
"""
Script to add CSV upload feature to the NFL DFS visualization
"""

import re

def add_upload_feature(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Add upload controls HTML after <body>
    upload_html = '''<body>
    <!-- Upload Controls -->
    <div class="upload-controls">
        <input type="file" id="csvFileInput" accept=".csv">
        <button class="upload-btn" onclick="document.getElementById('csvFileInput').click()">Upload CSV</button>
        <button class="reset-btn" onclick="resetToOriginalData()" id="resetBtn" style="display: none;">Reset Data</button>
    </div>
    <div class="upload-status" id="uploadStatus"></div>
'''
    content = content.replace('<body>', upload_html)

    # Step 2: Modify the allData initialization to check localStorage first
    # Find the line with const allData
    alldata_pattern = r'(const allData = )(\{"ALL".*?\}\);)'

    # We need to find this and wrap it
    alldata_replacement = r'''// Store original data
        const ORIGINAL_DATA = \2

        // Check if we have uploaded data in localStorage
        let allData;
        const storedData = localStorage.getItem('nflDfsUploadedData');
        if (storedData) {
            try {
                allData = JSON.parse(storedData);
                console.log('Loaded data from localStorage');
                // Show reset button
                setTimeout(() => {
                    const resetBtn = document.getElementById('resetBtn');
                    if (resetBtn) resetBtn.style.display = 'block';
                }, 100);
            } catch (e) {
                console.error('Error parsing stored data:', e);
                allData = ORIGINAL_DATA;
            }
        } else {
            allData = ORIGINAL_DATA;
        }'''

    content = re.sub(alldata_pattern, alldata_replacement, content, flags=re.DOTALL)

    # Step 3: Add upload handling functions before the closing </script> tag
    # Find the React render line
    upload_functions = '''
        // ========== CSV UPLOAD FUNCTIONALITY ==========

        // Show status message
        function showStatus(message, type = 'info') {
            const status = document.getElementById('uploadStatus');
            status.textContent = message;
            status.className = 'upload-status show ' + type;
            setTimeout(() => {
                status.classList.remove('show');
            }, 3000);
        }

        // Reset to original data
        window.resetToOriginalData = function() {
            if (confirm('Reset to original data? This will remove your uploaded data.')) {
                localStorage.removeItem('nflDfsUploadedData');
                localStorage.removeItem('nflDfsHeadshotCache');
                showStatus('Resetting to original data...', 'info');
                setTimeout(() => {
                    location.reload();
                }, 500);
            }
        };

        // Map CSV columns to internal format
        function mapCSVRow(row) {
            return {
                player_name: row['Name'] || row['name'] || row['player_name'] || '',
                player_id: (row['Name'] || row['player_name'] || 'Unknown').replace(/\\s+/g, '_') + '_' + Math.random().toString(36).substr(2, 9),
                position: row['Position'] || row['position'] || row['Pos'] || '',
                team_abbr: row['Team'] || row['team'] || row['team_abbr'] || '',
                salary: parseFloat(row['Salary'] || row['salary'] || 0),
                dk_projection: parseFloat(row['Projection'] || row['projection'] || row['dk_projection'] || 0),
                std_dev: parseFloat(row['Std Dev'] || row['std_dev'] || row['StdDev'] || 0),
                ceiling: parseFloat(row['Ceiling'] || row['ceiling'] || 0),
                bust_pct: parseFloat(row['Bust%'] || row['bust_pct'] || row['Bust'] || 0),
                boom_pct: parseFloat(row['Boom%'] || row['boom_pct'] || row['Boom'] || 0),
                ownership_pct: parseFloat(row['Own%'] || row['ownership_pct'] || row['Ownership'] || 0),
                optimal_pct: parseFloat(row['Optimal%'] || row['optimal_pct'] || row['Optimal'] || 0),
                leverage: parseFloat(row['Leverage'] || row['leverage'] || 0),
                headshot_url: '' // Will be fetched separately
            };
        }

        // Fetch headshot for a player
        async function fetchHeadshot(player) {
            // First, check if player already exists in ORIGINAL_DATA (embedded headshots)
            const originalPlayer = ORIGINAL_DATA.ALL.find(p =>
                p.player_name.toLowerCase() === player.player_name.toLowerCase()
            );
            if (originalPlayer && originalPlayer.headshot_url) {
                return originalPlayer.headshot_url;
            }

            // Second, try to fetch from server headshots folder
            const cleanName = player.player_name.replace(/[^a-zA-Z0-9\\s]/g, '').replace(/\\s+/g, '_');
            const serverHeadshotUrl = `/nfl-dfs/headshots/${cleanName}.png`;

            try {
                const response = await fetch(serverHeadshotUrl, { method: 'HEAD' });
                if (response.ok) {
                    return serverHeadshotUrl;
                }
            } catch (e) {
                // Server headshot not found, continue
            }

            // Third, try ESPN API (may have CORS issues)
            try {
                const espnUrl = `https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/${player.player_name.replace(/\\s+/g, '-').toLowerCase()}`;
                const response = await fetch(espnUrl);
                if (response.ok) {
                    const data = await response.json();
                    if (data.athlete && data.athlete.headshot && data.athlete.headshot.href) {
                        return data.athlete.headshot.href;
                    }
                }
            } catch (e) {
                // ESPN API failed
            }

            // Fourth, fallback to team logo or placeholder
            if (player.team_abbr) {
                return `https://a.espncdn.com/i/teamlogos/nfl/500/${player.team_abbr}.png`;
            }

            // Final fallback
            return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiNlNWU3ZWIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBmaWxsPSIjOWNhM2FmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Pz88L3RleHQ+PC9zdmc+';
        }

        // Handle CSV file upload
        document.getElementById('csvFileInput').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;

            showStatus('Parsing CSV file...', 'info');

            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: async function(results) {
                    if (!results.data || results.data.length === 0) {
                        showStatus('Error: CSV file is empty', 'error');
                        return;
                    }

                    showStatus(`Processing ${results.data.length} players...`, 'info');

                    // Map CSV data to internal format
                    const mappedData = results.data.map(mapCSVRow);

                    // Fetch headshots for all players
                    let completed = 0;
                    const totalPlayers = mappedData.length;

                    for (const player of mappedData) {
                        player.headshot_url = await fetchHeadshot(player);
                        completed++;
                        if (completed % 10 === 0 || completed === totalPlayers) {
                            showStatus(`Fetching images: ${completed}/${totalPlayers}`, 'info');
                        }
                    }

                    // Store in localStorage
                    const newData = { ALL: mappedData };
                    try {
                        localStorage.setItem('nflDfsUploadedData', JSON.stringify(newData));
                        showStatus('Upload successful! Reloading...', 'success');

                        // Reload the page to use new data
                        setTimeout(() => {
                            location.reload();
                        }, 1000);
                    } catch (e) {
                        if (e.name === 'QuotaExceededError') {
                            showStatus('Error: Data too large for browser storage', 'error');
                        } else {
                            showStatus('Error saving data: ' + e.message, 'error');
                        }
                    }
                },
                error: function(error) {
                    showStatus('Error parsing CSV: ' + error.message, 'error');
                }
            });

            // Reset file input
            e.target.value = '';
        });

        // ========== END CSV UPLOAD FUNCTIONALITY ==========

'''

    # Insert before the ReactDOM.createRoot line
    content = content.replace(
        '        // Render\n        const root = ReactDOM.createRoot(document.getElementById(\'root\'));',
        upload_functions + '        // Render\n        const root = ReactDOM.createRoot(document.getElementById(\'root\'));'
    )

    # Write the modified content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully added upload feature to {output_file}")
    print("Features added:")
    print("  ✓ PapaParse library (already added)")
    print("  ✓ Upload button UI")
    print("  ✓ CSV parsing logic")
    print("  ✓ localStorage persistence")
    print("  ✓ Headshot fetching (embedded → server → ESPN API → fallback)")
    print("  ✓ Reset to original data button")

if __name__ == '__main__':
    add_upload_feature('index.html.backup', 'index.html')
