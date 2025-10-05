import requests
import re
import os

# Your Monkeytype username
USERNAME = "grmpycrab"

# Get APE key from environment variable
APE_KEY = os.environ.get('MONKEYTYPE_APE_KEY', '')

def get_monkeytype_stats():
    """Fetch Monkeytype stats from API"""
    try:
        if not APE_KEY:
            print("Warning: No APE key found. Stats may not be accessible.")
        
        # Set up headers with authentication
        headers = {
            'Authorization': f'ApeKey {APE_KEY}',
            'User-Agent': 'Mozilla/5.0'
        }
        
        # Get personal bests
        profile_url = f"https://api.monkeytype.com/users/{USERNAME}/profile"
        profile_response = requests.get(profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            data = profile_response.json()
            
            # Extract stats (adjust based on actual API response)
            personal_bests = data.get('data', {}).get('personalBests', {})
            
            # Get stats for 60 second test (most common)
            time60 = personal_bests.get('time', {}).get('60', [])
            
            if time60:
                best_wpm = max([test.get('wpm', 0) for test in time60])
                avg_wpm = sum([test.get('wpm', 0) for test in time60]) / len(time60)
                best_acc = max([test.get('acc', 0) for test in time60])
                
                return {
                    'best_wpm': int(best_wpm),
                    'avg_wpm': int(avg_wpm),
                    'accuracy': int(best_acc)
                }
        
        print("Could not fetch stats. Using default values.")
        return None
        
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None

def update_readme(stats):
    """Update README.md with new stats"""
    if not stats:
        print("No stats to update")
        return
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the stats line
        pattern = r'\*\*Personal Best:\*\* `\d+ WPM` • \*\*Average:\*\* `\d+ WPM` • \*\*Accuracy:\*\* `\d+%`'
        
        # New stats line
        new_stats = f"**Personal Best:** `{stats['best_wpm']} WPM` • **Average:** `{stats['avg_wpm']} WPM` • **Accuracy:** `{stats['accuracy']}%`"
        
        # Replace the stats
        updated_content = re.sub(pattern, new_stats, content)
        
        # Write back to file
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated stats: {stats['best_wpm']} WPM (best), {stats['avg_wpm']} WPM (avg), {stats['accuracy']}% (acc)")
        
    except Exception as e:
        print(f"Error updating README: {e}")

if __name__ == "__main__":
    print("Fetching Monkeytype stats...")
    stats = get_monkeytype_stats()
    
    if stats:
        update_readme(stats)
    else:
        print("Could not fetch stats. README not updated.")
