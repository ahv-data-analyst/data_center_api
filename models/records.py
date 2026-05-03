from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import date

@dataclass_json
@dataclass
class PilgrimageRecord:
    unique_code: str
    name: str
    surname: str
    Position: str
    paid_Status: str
    travel_status: str
    
    def to_string(self) -> None:
        print(f"""
        Unique Code: {self.unique_code}
        Name: {self.name}
        Surname: {self.surname}
        Position: {self.Position}
        Paid status: {self.paid_Status}
        Travel Status: {self.arrival_status}
        """)

@dataclass_json
@dataclass
class MembershipRecord:
    id: int
    assessment_date: str
    trsh_membership_number: str
    assessment_code: str
    name: str
    surname: str
    gender: str
    birth_of_date: str
    country_of_attendance: str
    province: str
    branch: str
    cell_number: str
    year_of_arrival: str
    serving_group: str
    
    def to_string(self) -> None:
        print(f"""
            id: {self.id}
            assessment_date: {self.assessment_date}
            trsh_membership: {self.trsh_membership}
            assessment_code: {self.assessment_code}
            name: {self.name}
            surname: {self.surname}
            gender: {self.gender}
            birth_of_date: str: {self.birth_of_date}
            country_of_attendance: {self.country_of_attendance}
            province: {self.province}
            cell_number: {self.cell_number}
            year_of_arrival: {self.year_of_arrival}
            serving_group: {self.serving_group}
        """)

@dataclass_json      
@dataclass
class AssessmentRecord:
    assessment_id: str
    name: str
    surname: str
    membership_number: str
    assessment_code: str
    assessment_result: int
    interview_result: str
    assessment_date: str
    serving_group: str
    pass_fail: str = ""
    unique_code: str = ""
    progression_letter: str = ''
    
    def to_string(self) -> None:
        print(f"""
            assessment_id: {self.assessment_id}
            name: {self.name}
            surname: {self.surname}
            membership_number: {self.membership_number}
            assessment_code: {self.assessment_code}
            assessment_result: {self.assessment_result}
            interview_result: {self.interview_result}
            assessment_date: {self.assessment_date}
            unique_code: {self.unique_code}
            serving_group: {self.serving_group}
            pass_fail: {self.pass_fail}
        """)
        
    def add_pass_fail(self) -> None:
        if self.serving_group.lower() == "member" and self.assessment_result >= 50 :
            self.pass_fail = "PASS"
            
        elif self.serving_group.lower() == "member" and self.assessment_result < 50:
            self.pass_fail = "FAIL"
            
        elif self.assessment_result >= 60:
            self.pass_fail = "PASS"
        
        else: 
            self.pass_fail = "FAIL"
    
    def add_unique_code(self) -> None:
        start, end = self.assessment_id.split("-")
        
        if self.membership_number == "" or self.membership_number == "-":
            self.unique_code = "WAITING"
            return
        
        list_code = self.membership_number.split("-")       
        self.unique_code = end.strip() + list_code[-1].strip()
    
    def add_interview_result(self) -> None:
        self.interview_result = "PENDING"
        
    def set_progression_letter(self):
        self.progression_letter = 'NOT RECEIVED'