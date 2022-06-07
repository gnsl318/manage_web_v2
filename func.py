import os
from db.session import *
from crud import get,create,update
import xlsxwriter
import json
import operator
import collections
db_session = next(get_db())


def make_df(part_dict,ws):
    headers = ["연도","사업형태","사업종류","거래처","분야","파트","카테고리","세부카테고리","작업구분","버전","Name","Date","Raw","Result","Label_total","Label"]
    row = 1
    for i,header in enumerate(headers):
        ws.write(0,i,header)
    for part_name,part_info in part_dict.items():
        logs = get.log_part(db=db_session,part_id = part_info[0])
        dic ={}
        for log in logs:
            data = json.loads(log.info)
            user_name = log.user.name
            work_day = log.work_day
            try:
                if dic[f"{work_day}_{user_name}"]:
                    pass
            except:
                dic[f"{work_day}_{user_name}"]=[0,0,0,{}]
            if data == "raw_file":
                dic[f"{work_day}_{user_name}"][0] +=1
            else:
                dic[f"{work_day}_{user_name}"][1] +=1
                labels = 0
                for label,label_count in data.items():
                    labels +=label_count
                    try:
                        dic[f"{work_day}_{user_name}"][3][label] += label_count
                    except:
                        dic[f"{work_day}_{user_name}"][3][label] = label_count
                dic[f"{work_day}_{user_name}"][2] += labels
        
        col = 0
        dic=dict(sorted(dict(dic).items()))
        for h in range(part_name.count("-")+1):
            ws.write(row,col,part_name.split("-")[h])
            col+=1
        for k,v in dic.items():
            col = 10
            ws.write(row,col,k.split("_")[1])
            ws.write(row,col+1,k.split("_")[0])
            ws.write(row,col+2,v[0])
            ws.write(row,col+3,v[1])
            ws.write(row,col+4,v[2])
            v[3] = dict(sorted(dict(v[3]).items()))
            col = 15
            for label,label_count in v[3].items():
                ws.write(row,col,f"{label}:{label_count}")
                col+=1
            row+=1
        #ws.autofilter('A1:F1')
    return ws

def label_work(part_id,name:None,start_date:None,end_date:None):
    logs = get.log_name_date(db=db_session,part_id=part_id,name=name,start_date=start_date,end_date=end_date)
    counter = collections.Counter()
    work={}
    for log in logs:
        if log.info != json.dumps("raw_file"):
            counter.update(json.loads(log.info))
            log_work_day = log.work_day.strftime("%Y-%m-%d")
            try:
                work[log_work_day] +=1
            except:
                work[log_work_day] = 1
    label = dict(sorted(dict(counter).items()))
    work = dict(sorted(dict(work).items()))
    return json.dumps(label),json.dumps(work)