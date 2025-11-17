#!/usr/bin/env python3
"""Quick fix for the allData issue"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where ORIGINAL_DATA ends (look for the closing });)
# and add the allData initialization logic right after it

fix_code = '''

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
        }
'''

# Find the line that starts with "        const storedData = localStorage.getItem"
# and remove everything from there until we find the next significant code

# First, let's find if storedData line exists
if 'const storedData = localStorage.getItem' in content:
    # Already has the fix code, but allData is missing
    # Find the storedData section and add let allData before it
    content = content.replace(
        '        // Check if we have uploaded data in localStorage',
        '        // Check if we have uploaded data in localStorage\n        let allData;'
    )
else:
    # Need to add the whole fix after ORIGINAL_DATA
    # This is trickier - need to find where the huge ORIGINAL_DATA JSON ends
    # Look for a pattern that indicates the end
    pass

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed allData declaration")
