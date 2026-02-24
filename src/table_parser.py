import re

def parse_markdown_table(markdown_string: str) -> list[dict]:
    lines = markdown_string.strip().split('\n')
    
    # Find the table by looking for the header separator (e.g., |---|---|)
    header_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'\|.*---.*\|', line):
            header_idx = i - 1
            break
            
    if header_idx < 0:
        return []

    headers = [h.strip() for h in lines[header_idx].strip('|').split('|')]
    rows = []
    
    for line in lines[header_idx + 2:]:
        line = line.strip()
        if not line.startswith('|'):
            break
            
        columns = [c.strip() for c in line.strip('|').split('|')]
        
        # Zip headers and columns
        row_dict = {}
        for h, c in zip(headers, columns):
            # Sometimes markdown tables have extra spaces
            row_dict[h] = c
            
        # Optional validation
        if row_dict and "ID" in row_dict:
            rows.append(row_dict)
            
    return rows
