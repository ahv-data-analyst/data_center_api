from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://data_analyst_admin:local_password@localhost:7550/data_center")
engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

class TrshMembershipNumber(Base):
    __tablename__ = "trsh_membership_numbers"    
    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_date = Column(String, nullable=False)
    trsh_membership_number = Column(String, nullable=False, unique=True)
    assessment_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birth_of_date = Column(String, nullable=False)
    country_of_attendance = Column(String, nullable=False)
    province = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    cell_number = Column(String, nullable=False)
    year_of_arrival = Column(String, nullable=False)
    serving_group = Column(String, nullable=False)

class AssessmentTest(Base):
    __tablename__ = "assessment_tests"
    assessment_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    membership_number = Column(String, ForeignKey("trsh_membership_numbers.trsh_membership_number"), nullable=False, default="0")
    assessment_code = Column(String, nullable=False)
    assessment_results = Column(Integer, nullable=False, default=0)
    interview_results = Column(String, nullable=False, default="Pending")
    assessment_date = Column(String, nullable=False)
    pass_fail = Column(String, nullable=False, default="Pending")
    unique_code = Column(String, nullable=False, default="Pending")
    progression_letter = Column(String, nullable=False)
    serving_group = Column(String, nullable=False)

    TrshMembershipNumber = relationship("TrshMembershipNumber")

if __name__ == "__main__":
    print("[*] Creating database schema...")    
    Base.metadata.create_all(engine)
    print("[*] Database schema created successfully.")