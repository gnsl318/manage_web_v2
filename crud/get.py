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

def log_name(
    *,
    db:Session,
    part_id:int,
    name:str,
):
    name_id = db.query(User).filter(User.name==name).first().id
    log_info=db.query(Logs).filter(and_(Logs.part_id == part_id,Logs.user_id == name_id)).all()
    return log_info

def log_name_date(
    *,
    db:Session,
    part_id:int,
    name:str,
    start_date:str,
    end_date:str
):
    if start_date is None:
        start_date = datetime.datetime.strptime(f"{date.today().year}0101","%Y%m%d")
    if end_date is None:
        end_date = datetime.datetime.strptime(f"{int(date.today().year)+1}1231","%Y%m%d")
    if name is None:
        log_info=db.query(Logs).filter(and_((Logs.part_id == part_id),(Logs.work_day>=start_date),(Logs.work_day<=end_date))).all()
    else:
        name_id = db.query(User).filter(User.name==name).first().id
        log_info=db.query(Logs).filter(and_((Logs.part_id == part_id),(Logs.user_id == name_id),(Logs.work_day>=start_date),(Logs.work_day<=end_date))).all()
    return log_info

def error_name_date(
    *,
    db:Session,
    part_id:int,
    name:str,
    start_date:date,
    end_date:date,
    part_name:str
):
    if start_date is None:
        start_date = datetime.datetime.strptime(f"{date.today().year}0101","%Y%m%d")
    if end_date is None:
        end_date = datetime.datetime.strptime(f"{int(date.today().year)+1}1231","%Y%m%d")
    if name is None:
        error_info=db.query(Error).filter(and_(Error.part_id == part_id,Error.error_day>=start_date,Error.error_day<=end_date)).all()
    else:
        name_id = db.query(User).filter(User.name==name).first().id
        error_info=db.query(Error).filter(and_(Error.part_id == part_id,Error.user_id == name_id,Error.error_day>=start_date,Error.error_day<=end_date)).all()
    error_dic={}
    if error_info:
        for i,error in enumerate(error_info):
            error_dic[i] = [error.id,error.user.name,part_name,error.file_name,error.error.error,error.error_day]
    return error_dic