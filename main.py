from fastapi import FastAPI,Request,Form
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse,RedirectResponse,Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from db.session import *
import smtplib
from crud import create,get,update
from func import *
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="seoreu")
db_session = next(get_db())

templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/favicon.ico")
async def favicon():
	return FileResponse(os.path.join(os.getcwd(),"static/img/logo.ico"))


@app.get("/")
async def home(request:Request):
    part_dic = get.all_part(db=db_session)
    part_list = {}
    data = {}
    mean = {}
    count = {}
    for part_name,part_info in part_dic.items():
        part_list[f"{part_name.split('-')[6]}-{part_name.split('-')[7]}-{part_name.split('-')[8]}"]=part_name.split("-")[-1]
        log_info = get.log_part(db=db_session,part_id = part_info[0])
        day_work={}
        total_count = 0
        worker=[]
        for log in log_info:
            worker.append(log.user_id)
            try:
                day_work[log.work_day] +=1
            except:
                day_work[log.work_day] =1
        if len(day_work) != 0:
            mean[part_name]=f"{str(int(sum(day_work.values())/len(day_work.keys())))}:{len(set(worker))}"
        else:
            mean[part_name]=f"{str(0)}:0"
        total_count=sum(day_work.values())
        data[part_name]= int((total_count/part_info[1])*100)
        count[part_name]=f"{total_count}/{part_info[1]}"
    return templates.TemplateResponse('index.html',{'request':request,'data':data,'count':count,'part':part_list,'bar_data':mean})

@app.get("/main/login")
async def login_page(request:Request):
	page_file = f"login.html"
	return templates.TemplateResponse(page_file,{'request':request})

@app.post("/main/login_check")
async def login_check(request:Request,response:Response,InputEmail: str = Form(...),InputPassword: str = Form(...)):
	smtp = smtplib.SMTP('smtp.cafe24.com',587)   # 587: 서버의 포트번호
	smtp.ehlo()
	#smtp.starttls()   # tls방식으로 접속, 그 포트번호가 587
	try:
		smtp.login(InputEmail, InputPassword)
		user_session = get.user_session(db=db_session,email=InputEmail)
		request.session["name"]=user_session.name
		request.session["field"]=user_session.field
		return RedirectResponse(url="/", status_code=302)
	except:
		return RedirectResponse(url=f"/main/login", status_code=302)
@app.get("/main/logout")
async def logout(request:Request):
	request.session.clear()

	return RedirectResponse(url="/", status_code=302)

@app.post("/main/add_user")
async def add_user(request:Request,Employee_number: str = Form(...),Name: str = Form(...),email: str = Form(...),field: str = Form(...)):
	create.user(db=db_session,Employee_number=Employee_number,Name=Name,email=email,field=field)
	return RedirectResponse(url="/", status_code=302)

@app.get("/main/change_info")
async def change_info(request:Request):
    page_file = f"change_user.html"
    user_info = get.all_user(db=db_session)
    user_name = []
    for user in user_info:
        user_name.append(user.name)
    return templates.TemplateResponse(page_file,{'request':request,'user_name':user_name})

@app.post("/main/change_info_search")
async def change_info_search(request:Request,name: str = Form(None)):
    page_file = f"change_user.html"
    user_info=get.all_user(db=db_session)
    user_name = []
    for user in user_info:
        user_name.append(user.name)
    user = get.true_user(db=db_session,name=name)
    if user:
        return templates.TemplateResponse(page_file,{'request':request,'user_name':user_name,'employee_number':user.employee_number,'name':user.name,'email':user.email,'state':user.state,'field':user.field})
    else:
        return RedirectResponse(url="/main/change_info")

	
@app.post("/main/change_info_do")
async def change_user(request:Request,employee_number: str = Form(...),name: str = Form(...),email: str = Form(...),state: bool = Form(None),field: str = Form(None)):
	try:
		update.user(db=db_session,employee_number=employee_number,name=name,email=email,state=state,field=field)
		return RedirectResponse(url="/", status_code=302)
	except:
		return RedirectResponse(url="/main/change_info", status_code=302)


@app.get("/download/{part}")
def dwonload_file(request:Request,part:str):
    if part == "all":
        file_name=f"all_log"
        workbook = xlsxwriter.Workbook(f"{os.getcwd()}/file/{file_name}.xlsx")
        part_dict=get.all_part(db=db_session)
        ws = workbook.add_worksheet("All_log")
        make_df(part_dict = part_dict,ws=ws)
    else:
        file_name=f"{part}_log"
        l_class = part.split("-")[0]
        m_class = part.split("-")[1]
        s_class = part.split("-")[-1]
        workbook = xlsxwriter.Workbook(f"{os.getcwd()}/file/{file_name}.xlsx")
        ws = workbook.add_worksheet(f"{l_class}-{m_class}-{s_class}")
        make_df(db=db_session,l_class=l_class,m_class=m_class,s_class=s_class,ws=ws)
    workbook.close()
    file_path=os.path.join(os.getcwd(),f"file/{file_name}.xlsx")
    return FileResponse(path=file_path,media_type='application/octet-stream',filename=f"{file_name}_{datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}.xlsx")