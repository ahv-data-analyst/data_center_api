from database.AbstractDAO import AbstractDAO
from models.records import PilgrimageRecord
from typing import List, Optional, Tuple
from csv import reader

class PilgrimageRepo(AbstractDAO):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self._create_table()
        
    def _create_table(self):
        query: str = """CREATE TABLE IF NOT EXISTS pilgrimage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_code TEXT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            position TEXT NOT NULL,
            paid_Status TEXT DEFAULT 'NOT PAID',
            travel_status TEXT DEFAULT 'NOT TRAVELLED',
            UNIQUE(unique_code)
        );"""
        self.cursor.execute(query)
        
    def insert(self, record: PilgrimageRecord):
        with self.conn:
            self.cursor.execute("""
                INSERT OR IGNORE INTO pilgrimage (
                    unique_code,
                    name,
                    surname,
                    position,
                    paid_Status,
                    travel_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                (
                    record.unique_code,
                    record.name,
                    record.surname,
                    record.position,
                    record.paid_status,
                    record.travel_status
                )
            )
    
    def fetch_all(self) -> List[PilgrimageRecord]:
        self.cursor.execute("SELECT * FROM pilgrimage")
        rows = self.cursor.fetchall()
        return [PilgrimageRecord(
            row[1], row[2], row[3], row[4], row[5], 
            row[6]
            ) for row in rows]
    
    def fetch_one(self, unique_code: str) -> PilgrimageRecord:
        self.cursor.execute(
            "SELECT * FROM pilgrimage WHERE unique_code=?", 
            (unique_code,)
        )
        row = self.cursor.fetchone()
        if row:
            return PilgrimageRecord(
                row[1], row[2], row[3], row[4], row[5], 
                row[6]
            )
        return None