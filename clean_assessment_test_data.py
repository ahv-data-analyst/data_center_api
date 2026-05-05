from csv import reader, writer
from utils.serving_groups import serving_groups_mapping
from typing import Set

def clean_assessment_data() -> None:
    # 1. PRE-PROCESS MAPPING (Fast Pace Optimization)
    # Create a single lookup dict: {'Inceku': 'Standing Servants', 'Ncecu': 'Standing Servants', ...}
    lookup = {}
    for correct_name, messy_list in serving_groups_mapping.items():
        for item in messy_list:
            lookup[item.strip().lower()] = correct_name

    file_path: str = "data/THE SPIRITUAL HOME KINGDOM DATABASE 2026(assessment_test).csv"
    new_data = []

    # Using 'utf-8-sig' is often safer for CSVs exported from Excel than cp1252
    with open(file_path, "r", encoding='utf-8-sig') as f:
        file_data = reader(f)
        headings = next(file_data)
        new_data.append(headings)
        for i in file_data:
            if not i: 
                continue
            
            # Note: If your file uses ';' as the main delimiter, 
            # you can set delimiter=';' in the reader() instead of split()
            list_data = i
            # if len(list_data) < 10: continue # Guard against short lines
            
            if not list_data[3] or list_data[3] == "-":
                list_data[3] = "0"

            list_data[5] = format_date(list_data[5])
                
            if not list_data[6]:
                list_data[6] = "0"
                    
            # 2. Logic: Remove 'Member' if they have a real role
            new_groups = clean_group(list_data[9])
            list_data[9] = ", ".join(sorted(new_groups))
            
            if "Standing Servants" in new_groups:
                list_data[10] = "True"
            else:
                list_data[10] = "False"
                
            mark = convert_mark(list_data[6])
            
            # 3. Logic: Add the pass or fail depending on marks
            list_data[7] = pass_or_fail(mark, list_data[10])
                
            new_data.append(list_data)
            
    output_file: str = "data/clean-assessemt-test-data.csv"
    with open(output_file, "w", newline='', encoding='utf-8-sig') as f:
        # We use a standard comma delimiter for the output CSV
        write = writer(f)
        write.writerows(new_data)
    
    print(f"Pipeline complete. Processed {len(new_data)} rows.")

def pass_or_fail(mark: int, is_standing_servant: str) -> str:
    if mark == 0:
        return "Pending"
    elif mark >= 60 and is_standing_servant == "True":
        return "Pass"
    elif mark >= 50 and is_standing_servant == "False":
        return "Pass"
    else:
        return "Fail"

def convert_mark(mark: str) -> int:
    try:
        return int(mark)
        
    except ValueError:
        clean_value = mark.replace("\\", "").strip()
        if clean_value.isdigit():
            return int(clean_value)
        else:
            return 0
            
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

def format_date(date_str: str) -> str:
    try:
        return date_str.replace('/', '-')
    except Exception:
        return date_str

if __name__ == "__main__":
    clean_assessment_data()