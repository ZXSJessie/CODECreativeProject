import pandas as pd
import re
import json

# Read the Excel file
df = pd.read_excel('assets/Location_data.xlsx')

print("="*80)
print("EXCEL FILE INSPECTION")
print("="*80)
print(f"\nColumn names: {df.columns.tolist()}")
print(f"\nFirst column name: '{df.columns[0]}'")
print("\nColumn A (first column) data:")
for i in range(min(10, len(df))):
    print(f"  Row {i}: {df.iloc[i, 0]}")

print("\n" + "="*80)
print("LOCATION DATA EXTRACTION")
print("="*80)

# Filter out rows with NaN in the Primary Dimension column
df = df[df['Primary Dimension - Sleep Personality'].notna()]

locations = []

for idx, row in df.iterrows():
    # Column A should be the name
    name_from_col_a = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else f"Location {idx}"
    subtitle = str(row['Subtitle']) if pd.notna(row['Subtitle']) else f"Location {idx}"
    full_desc = str(row[' Copy']) if pd.notna(row[' Copy']) else ""
    personality = str(row['Primary Dimension - Sleep Personality']) if pd.notna(row['Primary Dimension - Sleep Personality']) else ""
    
    # Clean up - use column A if available, otherwise use subtitle
    name = name_from_col_a.strip().strip('"').strip()
    
    # Extract model ID from the link
    model_id = "b26a267e5a2a4779a0c55814ded990e9"  # default
    link = row['link']
    if pd.notna(link):
        match = re.search(r'models/([a-f0-9]+)/embed', str(link))
        if match:
            model_id = match.group(1)
    
    # Determine rarity and personality type
    if 'C (Comfort)' in personality:
        personality_type = 'C'
        rarity = 'LEGENDARY'
        icon = 'sofa'
    elif 'S (Stimulation)' in personality:
        personality_type = 'S'
        rarity = 'EPIC'
        icon = 'zap'
    elif 'A (Adaptability)' in personality:
        personality_type = 'A'
        rarity = 'UNCOMMON'
        icon = 'compass'
    elif 'R (Ritual)' in personality:
        personality_type = 'R'
        rarity = 'RARE'
        icon = 'clock'
    else:
        personality_type = 'C'
        rarity = 'COMMON'
        icon = 'map-pin'
    
    # Create simple location ID
    location_id = f"loc-{idx}"
    
    # Clean and format description
    clean_desc = full_desc.replace('\n', ' ').replace('  ', ' ').strip()
    
    locations.append({
        'id': location_id,
        'name': name,
        'subtitle': subtitle,
        'description': clean_desc,
        'icon': icon,
        'model_id': model_id,
        'rarity': rarity,
        'is_secret': False,
        'personality': personality_type
    })

# Print full information
for loc in locations:
    print(f"\nLocation ID: {loc['id']}")
    print(f"Name (Column A): {loc['name']}")
    print(f"Subtitle (Column): {loc['subtitle']}")
    print(f"Description: {loc['description']}")
    print(f"Model ID: {loc['model_id']}")
    print(f"Rarity: {loc['rarity']}")
    print(f"Icon: {loc['icon']}")
    print("-" * 80)

