from datetime import date
from sqlalchemy import null, update, and_
from sqlalchemy.orm import Session, load_only
from models.base import *
import datetime
import json
import time


def user(
    *,
    db:Session,
    employee_number:str,
    name:str,
    email:str,
    state:str,
    field:str
):
    user = db.query(User).filter(User.employee_number == employee_number).first()
    user.name=name
    user.email=email
    user.state=state
    user.field=field
    db.commit()
    return user