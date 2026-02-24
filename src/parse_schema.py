import json
import re

def parse_schema():
    with open('data/input/prompt_text.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    schema_line = ""
    for idx, line in enumerate(lines):
        if "(Processing Instructions" in line:
            schema_line = lines[idx]
            break

    # Extract part after "A/C "
    start_str = "A/C "
    data_str = schema_line[schema_line.index(start_str) + len(start_str):]

    # Split the string by matching numbers 1 to 163 followed by space/tab
    # We can split by re.split(r'\b(\d+)\s{2,}', data_str)
    
    # Alternatively find all indices of " 1  ", " 2  ", etc. or spaces
    # Let's clean the string a bit
    data_str = data_str.replace('\u2003', '  ')
    
    rows = []
    # Find all pattern: number followed by spaces, up to the next number followed by spaces
    # Since we know there are 163 IDs
    for i in range(1, 164):
        look_for = f"{i}  "
        next_look_for = f"{i+1}  " if i < 163 else None
        
        # We need a regex or simply string find
        # But wait, the ID might just be "1  " or "1 " depending on replace
        # Let's use regex
        # match ID at start or preceded by spaces
        pass

    # Better approach: We know the columns:
    # 1. ID (integer)
    # 2. Category
    # 3. Description
    # 4. Parameter
    # 5. Content Type
    # 6. Min
    # 7. Max
    # 8. A/C (Atomic / Composite)
    
    # We can use regex to find all matches of Atomic or Composite, which end each row!
    row_pattern = r'(\d+)\s+(.*?)\s\s+(.*?)\s\s+(.*?)\s\s+([A-Za-z]+)\s\s+(.*?)\s*(Atomic|Composite)'
    # wait, Min and max can be "As needed" or numbers. "As needed" might be followed by spaces.
    # Let's just find all matches ending with Atomic or Composite.
    
    # split by Atomic or Composite
    parts = re.split(r'(Atomic|Composite)', data_str)
    
    # parts will be: [row1_start_to_end_minus_A/C, A/C_value, row2_start_to_end_minus_A/C, A/C_value, ...]
    parsed_rows = []
    for i in range(0, len(parts)-1, 2):
        row_content = parts[i].strip()
        ac = parts[i+1].strip()
        
        if not row_content:
            continue
            
        # extract ID (first word)
        match = re.match(r'^(\d+)\s+(.*)', row_content)
        if not match:
            print(f"Skipping: {row_content}")
            continue
            
        row_id = match.group(1)
        rest = match.group(2)
        
        # Split the rest by 2 or more spaces
        cols = [c.strip() for c in re.split(r'\s{2,}', rest) if c.strip()]
        
        parsed_rows.append({
            "ID": row_id,
            "Category": cols[0] if len(cols) > 0 else "",
            "Description": cols[1] if len(cols) > 1 else "",
            "Parameter": cols[2] if len(cols) > 2 else "",
            "Type": cols[3] if len(cols) > 3 else "",
            "MinMax": " | ".join(cols[4:]),
            "A/C": ac
        })
        
    with open('data/input/schema.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_rows, f, indent=2)

    print(f"Parsed {len(parsed_rows)} rows out of 163 expected.")

parse_schema()
