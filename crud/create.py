
from datetime import date
from sqlalchemy import null, update, and_
from sqlalchemy.orm import Session, load_only
from models.base import *
import datetime 
import json
import time


## 파트 생성
def part(
    *,
    db : Session,
    p_02:str,
    p_03:str,
    p_04:str,
    p_05:str,
    p_06:str,
    p_07:str,
    p_08:str,
    p_09:str,
    p_10:str,
    max_count:int,
    start_date:date,
    end_date:date,
    ):
    year = datetime.date.today().year
    if db.query(Part).filter(and_((Part.p_01 == f"{year}_PJT"),(Part.p_02==p_02),(Part.p_03==p_03),(Part.p_04==p_04),(Part.p_05==p_05),(Part.p_06==p_06),(Part.p_07==p_07),(Part.p_08==p_08),(Part.p_09==p_09),(Part.p_10==p_10))).first()==None:
        new_part = Part(
            p_01=f"{year}_PJT",
            p_02=p_02,
            p_03=p_03,
            p_04=p_04,
            p_05=p_05,
            p_06=p_06,
            p_07=p_07,
            p_08=p_08,
            p_09=p_09,
            p_10=p_10,
            max_count = max_count,
            start_day=start_date,
            end_day=end_date,
            state = True,
        )
        db.add(new_part)
        db.commit()
        return True
    else:
        return False
## 유저 생성
def user(
    *,
    db : Session,
    Employee_number:str,
    Name:str,
    email:str,
    field:str
):
    
    if db.query(User).filter((User.employee_number == Employee_number)|(User.email==email)).first()==None:
        new_user = User(
            employee_number = Employee_number,
            name = Name,
            email = email,
            state = True,
            field = field
        )
        db.add(new_user)
        db.commit()
        return True
    else:
        return False

def error_list(
    *,
    db : Session,
    error:str
):
    if db.query(Error_list).filter(Error_list.error==error).first()==None:
        new_error_list = Error_list(
            error=error,
        )
        db.add(new_error_list)
        db.commit()
        return True
    else:
        return False

