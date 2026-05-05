from database.database_manager import DatabaseManager 

def get_data_grouped_by_date():
    query = "SELECT serving_group FROM assessment_tests"
    
    grouped_data = []
    with DatabaseManager('data/ahv_data.db') as db:
        data = db.connection.execute(query).fetchall()
        
        for i in data:
            entry = {
               'serving_groups': data,
            }
            grouped_data.append(entry)
    
    print(f"Records found: {len(grouped_data)}")
    
    
        
    return grouped_data
print(get_data_grouped_by_date())