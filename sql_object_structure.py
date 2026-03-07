from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer,String, VARCHAR, TIMESTAMP, BOOLEAN,Float,DateTime, text,create_engine
TblObject = declarative_base()
class Violation(TblObject):
    __tablename__ = 'violation_data'
    #__table_args__ = ({"schema": "public"})
    vid = Column(VARCHAR(50), primary_key=True)
    car_no = Column(VARCHAR(15))
    proccess_time = Column(DateTime)
    violation_time = Column(DateTime)
    violation_address = Column(VARCHAR(200))
    violation_content = Column(VARCHAR(200))
    proccess_status = Column(VARCHAR(10))
    pay_status = Column(VARCHAR(10))
    violation_points = Column(VARCHAR(10))
    violation_fines = Column(VARCHAR(10))
    company = Column(VARCHAR(20))
    resource = Column(VARCHAR(10))
    refresh_time = Column(DateTime)