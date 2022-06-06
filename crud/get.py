from datetime import date
from sqlalchemy import null, update, and_
from sqlalchemy.orm import Session, load_only
from models.base import *
import datetime
import json
import time



def all_part(
    *,
    db:Session,
):
    part_dic ={}
    part_info = db.query(Part).all()
    for part in part_info:
        part_dic[f"{part.p_01}-{part.p_02}-{part.p_03}-{part.p_04}-{part.p_05}-{part.p_06}-{part.p_07}-{part.p_08}-{part.p_09}-{part.p_10}"]=[part.id,part.max_count,part.state]
    return part_dic

def log_part(
    *,
    db:Session,
    part_id:int,
):
    log_info = db.query(Logs).filter(Logs.part_id == part_id).all()
    return log_info

def user_session(
    *,
    db:Session,
    email:str
): 
    user = db.query(User).filter(User.email==email).first()
    return user

def all_user(
    *,
    db:Session,
):
    user_info = db.query(User).all()
    return user_info

def true_user(
    *,
    db:Session,
    name:str
):
    if db.query(User).filter(User.name==name).first():
        return True
    else:
        return False