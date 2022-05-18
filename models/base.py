from sqlalchemy import Column, Integer, String, ForeignKey, Time, func, Boolean, Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import sys
import os
from db.session import Base,engine

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  employee_number = Column(String(3000),unique=True)
  name = Column(String(3000))
  field = Column(String(3000))
  email = Column(String(3000),unique=True)
  state = Column(Boolean)

class Part(Base):
  __tablename__='part'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  p_01  = Column(String(3000))
  p_02  = Column(String(3000))
  p_03  = Column(String(3000))
  p_04  = Column(String(3000))
  p_05  = Column(String(3000))
  p_06  = Column(String(3000))
  p_07  = Column(String(3000))
  p_08  = Column(String(3000))
  p_09  = Column(String(3000))
  p_10  = Column(String(3000))
  max_count = Column(Integer)
  start_day = Column(Date)
  end_day = Column(Date)
  state = Column(Boolean)


class Raw(Base):
  __tablename__ = 'raw'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  part_id = Column(Integer,ForeignKey("part.id"))
  part  = relationship("Part")
  raw_name = Column(String(3000))
  change_name = Column(String(3000))
  chnage_day = Column(Date)

class Logs(Base):
  __tablename__ = "log"
  id = Column(Integer, primary_key = True, autoincrement=True,index=True)
  part_id = Column(Integer,ForeignKey("part.id"))
  part = relationship("Part")
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User")
  work_day = Column(Date)
  file_name = Column(String(3000))
  info = Column(String(3000))

class Check_Logs(Base):
  __tablename__ = "check_log"
  id = Column(Integer, primary_key = True, autoincrement=True,index=True)
  part_id = Column(Integer,ForeignKey("part.id"))
  part = relationship("Part")
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User")
  work_day = Column(Date)
  file_name = Column(String(3000))
  info = Column(String(3000))

class Test_log(Base):
  __tablename__ = "test_log"
  id = Column(Integer, primary_key = True, autoincrement=True,index=True)
  part_id = Column(Integer,ForeignKey("part.id"))
  part = relationship("Part")
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User")
  work_day = Column(Date)
  file_name = Column(String(3000))
  info = Column(String(3000))

class Error_list(Base):
  __tablename__ = 'error_list'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  error = Column(String(3000))

class Error(Base):
  __tablename__= 'error'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User",foreign_keys=[user_id])
  part_id = Column(Integer,ForeignKey("part.id"))
  part = relationship("Part")
  file_name = Column(String(3000))
  error_id =Column(Integer,ForeignKey("error_list.id"))
  error = relationship("Error_list")
  error_day = Column(Date)
  clear_day = Column(Date)
  clear_user_id = Column(Integer,ForeignKey("users.id"))
  clear_user = relationship("User",foreign_keys=[clear_user_id])


class Check_Error(Base):
  __tablename__= 'check_error'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User",foreign_keys=[user_id])
  part_id = Column(Integer,ForeignKey("part.id"))
  part = relationship("Part")
  file_name = Column(String(3000))
  error_id =Column(Integer,ForeignKey("error_list.id"))
  error = relationship("Error_list")
  error_day = Column(Date)
  clear_day = Column(Date)
  clear_user_id = Column(Integer,ForeignKey("users.id"))
  clear_user = relationship("User",foreign_keys=[clear_user_id])


