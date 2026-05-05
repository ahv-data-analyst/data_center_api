from csv import reader, writer
from utils.serving_groups import serving_groups_mapping
from typing import Set

def clean_membership_data() -> None:
    # 1. PRE-PROCESS MAPPING (Fast Pace Optimization)
    # Create a single lookup dict: {'Inceku': 'Standing Servants', 'Ncecu': 'Standing Servants', ...}
    lookup = {}
    for group, members in serving_groups_mapping.items():
        for member in members:
            lookup[member] = group
            
    # 2. LOAD AND PROCESS DATA
    file_path = 'data/THE SPIRITUAL HOME KINGDOM DATABASE 2026(trsh_membership_number).csv'
    output_file: str = 'data/clean-membership-data.csv'
    with open(file_path, 'r') as infile, open(output_file, 'w') as outfile:
        file_data = reader(infile)
        headings = next(file_data)
        writer(outfile).writerow(headings)
        for row in file_data:
            if not row:
                continue

            row[2] = format_date(row[2])

            if not row[3] or row[3] == '-':
                row[3] = '0'

            row[8] = format_date(row[8])
            
            row[13] = get_year(row[13])
            
            row[14] = ', '.join(clean_group(row[14]))

def get_year(date_str: str) -> str:
    try:
        return date_str.split('/')[-1]
    except Exception:
        return date_str

def format_date(date_str: str) -> str:
    try:
        return date_str.replace('/', '-')
    except Exception:
        return date_str

def clean_group(group: str) -> Set[str]:
    raw_groups = group.split(";")
    new_groups = set()
    
    for item in raw_groups:
        # 1. Clean the item of whitespace AND existing quotes
        clean_item = item.strip().replace('"', '').replace("'", "")
        if not clean_item: 
            continue
        found_category = None
        for correct_name, messy_list in serving_groups_mapping.items():
            if clean_item in messy_list:
                found_category = correct_name
                break
        if found_category:
            new_groups.add(found_category)
        else:
            new_groups.add(clean_item)
    
    return new_groups
