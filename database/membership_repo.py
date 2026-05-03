from database.AbstractDAO import AbstractDAO
from models.records import MembershipRecord
from typing import List, Optional, Tuple
from csv import reader

class MembershipRepo(AbstractDAO):
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()
        self._create_table()
        self._load_data()
        
    def _create_table(self) -> None:
        query = """CREATE TABLE IF NOT EXISTS trsh_membership_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_date TEXT NOT NULL,
            trsh_membership_number TEXT NOT NULL,
            assessment_code TEXT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_of_date TEXT NOT NULL,
            country_of_attendance TEXT NOT NULL,
            province TEXT NOT NULL,
            branch TEXT NOT NULL,
            cell_number TEXT NOT NULL,
            year_of_arrival TEXT NOT NULL,
            serving_group TEXT NOT NULL,
            UNIQUE(trsh_membership_number)
        );"""
        self.cursor.execute(query)
        
    def _load_data(self) -> None:
        membership_records: List[Tuple] = []
        file_path: str = "data/THE SPIRITUAL HOME KINGDOM DATABASE 2026(trsh_membership_number).csv"
        with open(file_path, "r", encoding='cp1252') as f:
            file_data = reader(f)
            next(file_data)
            
            for i in file_data:
                if not i: continue
                membership_records.append(
                    (
                        i[2], i[3], i[4], i[5], i[6], i[7], i[8], 
                        i[9], i[10], i[11], i[12], i[13], i[14],
                    )
                )
        
        self.insert_many(membership_records)
        
    def insert_many(self, data: List[Tuple]) -> None:
        with self.conn:
            self.cursor.executemany("""
                INSERT OR IGNORE INTO trsh_membership_numbers (
                    assessment_date, 
                    trsh_membership_number, 
                    assessment_code, 
                    name, 
                    surname, 
                    gender, 
                    birth_of_date, 
                    country_of_attendance, 
                    province, 
                    branch, 
                    cell_number, 
                    year_of_arrival, 
                    serving_group) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (
                    data
                )
            )
        
    def insert(self, data: MembershipRecord) -> None:
        with self.conn:
            self.cursor.execute("""
                INSERT OR IGNORE INTO trsh_membership_numbers (
                    assessment_date, 
                    trsh_membership_number, 
                    assessment_code, 
                    name, 
                    surname, 
                    gender, 
                    birth_of_date, 
                    country_of_attendance, 
                    province, 
                    branch, 
                    cell_number, 
                    year_of_arrival, 
                    serving_group) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (
                    data.assessment_date, 
                    data.trsh_membership_number, 
                    data.assessment_code, data.name, 
                    data.surname, 
                    data.gender, 
                    data.birth_of_date, 
                    data.country_of_attendance, 
                    data.province, 
                    data.branch, 
                    data.cell_number, 
                    data.year_of_arrival, 
                    data.serving_group
                )
            )
            
    def fetch_all(self) -> List[MembershipRecord]:
        self.cursor.execute("SELECT * FROM trsh_membership_numbers")
        rows = self.cursor.fetchall()
        return [MembershipRecord(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 
            row[8], row[9], row[10], row[11], row[12], row[13]
            ) for row in rows]

    def fetch_one(self, membership_number: str) -> Optional[MembershipRecord]:
        self.cursor.execute("SELECT * FROM trsh_membership_numbers WHERE trsh_membership_number=?", (membership_number,))
        row = self.cursor.fetchone()
        if row:
            return MembershipRecord(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 
                row[8], row[9], row[10], row[11], row[12], row[13]
            )
        return None
    
    def fetch_page(self, page: int, limit: int, group):
        offset = (page - 1) * limit
        
        query = "SELECT * FROM trsh_membership_numbers"
        params = []

        if group:
            query += " WHERE serving_group = ?"
            params.append(group)

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        results = self.cursor.execute(query, params).fetchall()
        
        total_count = self.cursor.execute("SELECT COUNT(*) FROM trsh_membership_numbers").fetchone()[0]
        
        data = [MembershipRecord(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 
            row[8], row[9], row[10], row[11], row[12], row[13]
            ) for row in results]
        
        return total_count, data
    
    # def update(self, record_id: int, data: MembershipRecord) -> None:
    #     with self.conn:
    #         self.cursor.execute("UPDATE trsh_membership_numbers SET name=?, value=? WHERE id=?", (data['name'], data['value'], record_id))

    # def delete(self, record_id: int) -> None:
    #     with self.conn:
    #         self.cursor.execute("DELETE FROM trsh_membership_numbers WHERE id=?", (record_id,))