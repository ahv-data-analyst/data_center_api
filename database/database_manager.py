import sqlite3
import pathlib
from typing import Self
from database.assessment_repo import AssessmentRepo
from database.membership_repo import MembershipRepo
from database.pilgrimage_repo import PilgrimageRepo

class DatabaseManager():    
    def __init__(self, file_path: str) -> None:
        path_obj = pathlib.Path(file_path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        self.database_path = path_obj
        
    def __enter__(self) -> Self:
        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute('PRAGMA foreign_keys = ON;')
        self.members = MembershipRepo(self.connection)
        self.assessments = AssessmentRepo(self.connection)
        self.pilgrimage = PilgrimageRepo(self.connection)
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.connection.commit()
        self.connection.close()