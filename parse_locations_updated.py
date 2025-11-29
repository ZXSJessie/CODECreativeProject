import pandas as pd
import re

# Read Excel file
df = pd.read_excel('assets/location_data.xlsx')

def extract_sketchfab_id(html_str):
    """Extract Sketchfab model ID from embed HTML"""
    if pd.isna(html_str):
        return ""
    match = re.search(r'models/([a-f0-9]+)/', str(html_str))
    return match.group(1) if match else ""

def extract_ratings(rating_str):
    """Extract star ratings from the 'Other' column (Column F)"""
    if pd.isna(rating_str):
        return {
            "comfort": 3,
            "quietness": 3,
            "accessibility": 3,
            "vibe_check": 3,
            "danger": 1
        }
    
    # Count stars for each category
    lines = str(rating_str).split('\n')
    ratings = {}
    
    for line in lines:
        star_count = line.count('★')
        if star_count > 0:
            # Map to our rating categories based on keywords
            if '💤' in line or 'Nap Level' in line:
                ratings['comfort'] = star_count
            elif '🔍' in line or 'Discovery' in line or 'Difficulty' in line:
                ratings['accessibility'] = 6 - star_count  # Invert: harder to find = more accessible rating
            elif '☁️' in line or 'Comfort' in line:
                ratings['quietness'] = star_count
            elif '🕐' in line or 'Time' in line:
                ratings['vibe_check'] = star_count
    
    # Set defaults for any missing
    result = {
        "comfort": ratings.get('comfort', 3),
        "quietness": ratings.get('quietness', 3),
        "accessibility": ratings.get('accessibility', 3),
        "vibe_check": ratings.get('vibe_check', 3),
        "danger": 1  # Default low danger
    }
    
    return result

def personality_to_rarity(personality):
    """Map personality type to rarity"""
    if pd.isna(personality):
        return "UNCOMMON"
    
    p = str(personality).upper()
    if 'C (COMFORT)' in p or 'SOFA DAYDREAMER' in p:
        return "LEGENDARY"
    elif 'S (STIMULATION)' in p or 'LECTURE PHANTOM' in p:
        return "EPIC"
    elif 'R (RITUAL)' in p or 'EFFICIENT NAPPER' in p:
        return "RARE"
    else:
        return "UNCOMMON"

def create_location_id(name):
    """Create a location ID from name"""
    # Remove special characters and convert to lowercase
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
    words = clean.lower().split()[:3]  # Take first 3 words
    return '-'.join(words)

print("Parsing locations from Excel...")
print(f"Found {len(df)} locations\n")

for idx, row in df.iterrows():
    location = row['location']
    name = row['name']
    subtitle = row['Subtitle']
    description = row[' Copy']  # Note the leading space
    personality = row['Primary Dimension - Sleep Personality']
    ratings_str = row['Other']
    model_html = row['link']
    
    location_id = create_location_id(name)
    model_id = extract_sketchfab_id(model_html)
    rarity = personality_to_rarity(personality)
    sample_ratings = extract_ratings(ratings_str)
    
    # Determine icon based on personality/location
    if 'sofa' in str(name).lower() or 'SOFA DAYDREAMER' in str(personality).upper():
        icon = 'sofa'
    elif 'outdoor' in str(location).lower() or 'EASYGOING' in str(personality).upper():
        icon = 'compass'
    elif 'stair' in str(name).lower() or 'LECTURE PHANTOM' in str(personality).upper():
        icon = 'zap'
    elif 'milk tea' in str(name).lower() or 'tea' in str(name).lower():
        icon = 'clock'
    else:
        icon = 'bed-double'
    
    print(f"Location {idx + 1}:")
    print(f"  ID: {location_id}")
    print(f"  Location: {location}")
    print(f"  Name: {name}")
    print(f"  Subtitle: {subtitle}")
    print(f"  Description: {description[:100]}...")
    print(f"  Rarity: {rarity}")
    print(f"  Icon: {icon}")
    print(f"  Model ID: {model_id}")
    print(f"  Sample Ratings: {sample_ratings}")
    print()

print("\n=== Python Dictionary Format ===\n")
for idx, row in df.iterrows():
    location = row['location']
    name = row['name']
    description = row[' Copy']
    personality = row['Primary Dimension - Sleep Personality']
    model_html = row['link']
    
    location_id = create_location_id(name)
    model_id = extract_sketchfab_id(model_html)
    rarity = personality_to_rarity(personality)
    sample_ratings = extract_ratings(row['Other'])
    
    # Determine icon
    if 'sofa' in str(name).lower() or 'SOFA DAYDREAMER' in str(personality).upper():
        icon = 'sofa'
    elif 'outdoor' in str(location).lower() or 'EASYGOING' in str(personality).upper():
        icon = 'compass'
    elif 'stair' in str(name).lower() or 'LECTURE PHANTOM' in str(personality).upper():
        icon = 'zap'
    elif 'milk tea' in str(name).lower() or 'tea' in str(name).lower():
        icon = 'clock'
    else:
        icon = 'bed-double'
    
    print(f'''        {{
            "id": "{location_id}",
            "location": "{location}",
            "name": "{name}",
            "description": "{description}",
            "icon": "{icon}",
            "model_id": "{model_id}",
            "rarity": "{rarity}",
            "is_secret": False,
            "sample_rating": {sample_ratings}
        }},''')
