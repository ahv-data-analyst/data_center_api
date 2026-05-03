from database.AbstractDAO import AbstractDAO
from models.records import AssessmentRecord
from typing import List, Optional, Tuple
from csv import reader

class AssessmentRepo(AbstractDAO):
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()
        self._create_table()
        self._load_data()
        
    def _create_table(self) -> None:
        query: str = """CREATE TABLE IF NOT EXISTS assessment_tests (
            assessment_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            membership_number TEXT NOT NULL,
            assessment_code TEXT NOT NULL,
            assessment_results INTEGER NOT NULL,
            interview_results TEXT NOT NULL,
            assessment_date TEXT NOT NULL,
            pass_fail TEXT,
            unique_code TEXT,
            progression_letter TEXT,
            serving_group TEXT NOT NULL,
            UNIQUE(membership_number, assessment_id)
        );"""
        self.cursor.execute(query)
        
    def _load_data(self) -> None:
        assessment_records: List[AssessmentRecord] = []
        file_path: str = "data/THE SPIRITUAL HOME KINGDOM DATABASE 2026(assessment_test).csv"
        with open(file_path, "r", encoding='cp1252') as f:
            file_data = reader(f)
            next(file_data)
            
            for i in file_data:
                if not i: continue
                mark: int = 0
                if i[5] != "" and i[5] != " ":  mark = int(i[5])
                record = AssessmentRecord(
                    i[0],
                    i[1], i[2], i[3], i[4], mark,
                    i[6], i[7], i[9]
                )
                record.add_interview_result()
                record.add_pass_fail()
                record.add_unique_code()
                record.set_progression_letter()
                
                self.insert(record)
                
                
    def insert_many(self, data: List[Tuple]) -> None:
        with self.conn:
            self.cursor.execute("""
                INSERT OR IGNORE INTO assessment_tests (
                    assessment_id, 
                    name, 
                    surname, 
                    membership_number, 
                    assessment_code, 
                    assessment_results, 
                    interview_results, 
                    assessment_date, 
                    unique_code, 
                    serving_group, 
                    pass_fail,
                    progression_letter) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (
                    data
                )
            )
        
    def insert(self, data: AssessmentRecord) -> None:
        with self.conn:
            self.cursor.execute("""
                INSERT OR IGNORE INTO assessment_tests (
                    assessment_id, 
                    name, 
                    surname, 
                    membership_number, 
                    assessment_code, 
                    assessment_results, 
                    interview_results, 
                    assessment_date, 
                    unique_code, 
                    serving_group, 
                    pass_fail,
                    progression_letter) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (data.assessment_id, 
                 data.name, 
                 data.surname, 
                 data.membership_number, 
                 data.assessment_code, 
                 data.assessment_result, 
                 data.interview_result, 
                 data.assessment_date,
                data.unique_code,
                data.serving_group,
                 data.pass_fail,
                 data.progression_letter
                 )
            )
            
    def fetch_all(self) -> List[AssessmentRecord]:
        self.cursor.execute("SELECT * FROM assessment_tests")
        rows = self.cursor.fetchall()
        return [AssessmentRecord(
            row[0], row[1], row[2], row[3], row[4], row[5], 
            row[6], row[7], row[10], row[8], row[11], row[9]
            ) for row in rows]
        
    def fetch_one(self, record_id):
        self.cursor.execute("SELECT * FROM assessment_tests WHERE membership_number LIKE ?", (f"%{record_id}%",))
        row = self.cursor.fetchone()
        return AssessmentRecord(
        row[0], row[1], row[2], row[3], row[4], row[5], 
        row[6], row[7], row[10], row[8], row[11], row[9]
        )

    def fetch(self, membership_number: str) -> Optional[AssessmentRecord]:
        self.cursor.execute("SELECT * FROM assessment_tests WHERE membership_number LIKE ?", (f"%{membership_number}%",))
        rows = self.cursor.fetchall()
        return [AssessmentRecord(
        row[0], row[1], row[2], row[3], row[4], row[5], 
        row[6], row[7], row[10], row[8], row[11], row[9]
        ) for row in rows]
    
    def fetch_page(self, page: int, limit: int, group):
        offset = (page - 1) * limit
        
        query = "SELECT * FROM assessment_tests"
        params = []
        
        if group:
            query += "WHERE serving_group = ?"
            params.append(group)
            
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        result = self.cursor.execute(query, params).fetchall()
        
        total_count = self.cursor.execute("SELECT COUNT(*) FROM assessment_tests").fetchone()[0]
        
        data = [
            AssessmentRecord(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[10], row[8], row[11], row[9]
            ) for row in result
        ]
        
        return total_count, data
    
    def update_assessment_results(self, membership_number: str, data: AssessmentRecord) -> None:
        with self.conn:
            self.cursor.execute(
                """UPDATE assessment_tests SET 
                assessment_results=?, 
                interview_results=?,
                pass_fail=?
                WHERE membership_number=?""", 
                (
                    data.assessment_result,
                    data.interview_result,
                    data.pass_fail,
                    membership_number
                )
            )
            
    def get_count(self):
        return self.cursor.execute("SELECT COUNT(*) FROM assessment_tests").fetchone()[0]

    # def delete(self, record_id: int) -> None:
    #     with self.conn:
    #         self.cursor.execute("DELETE FROM assessment_tests WHERE id=?", (record_id,))