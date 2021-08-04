from flask import Flask, request, make_response
app = Flask(__name__)
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
config = {
  "type": "service_account",
  "project_id": "esp-casmir",
  "private_key_id": "15152b61045649e6a1adf3683448b1ff537be8e3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/KQt/yICvbis4\n3frE1nOIEvvfCNgsqjQr6fyUbcJicbkV3k2MgobEVA5fKUhtcd5SV6qOPlmge2bg\nPiFTrNAtEeGidVew20F+F6am1SIa/BAJGmalJ9gw0SSA8BGAt5xKv7LMxvCvCmki\nFIsq/BjzqStBi/YgGMNi4CSgs7fepILOb4IYBRNmE6ja+ApsmgP2gqLfCaJEqD7z\nYvsHmo9e28vBDRAW9GV0KldA+JuaQMTbmoQHYlLEjqZ630+fIcuH14MGmMt8+E/6\ncXIkY7dlkTSG+Mm4ugux+POyCXz/+7k2v/U0Ft/MsfcdxpOOoMPCYp1NxsiF/+7k\nurNCCod3AgMBAAECggEACJZvSfrNGSnMWZ4ooAN4UOJ1cTlu/gwEEv2h113aRTI8\nW935mDiG6wv8UfcYpgi0XE5MPwlQXR7Iv4XbA8Ii31t1ylFrh+pEVhtO5SDJtZz2\n8B8WVxC5VsbBKo+ztuzItyzx0ImWvMOtdxalgoqtE56DxHU6sIocQPVhKoetrhvx\nqFe3JyhxETcWrVw5W7hAkBaVri+4KWf2FX56bhP3OzMXLrrAWBY1D8kYRpUsm2dY\nsXXhgkNnIL6NpXCJh9vyU0XZg9LGlfGJY9d0+L41ZuEcUHzh6D0awI2LvA0t+Mq+\nfZgMevirS98iV9I/Q16y/xBrbKRn3c3y9OoERlBfDQKBgQDjKTb7/IaALSJxWo3D\nLJybiLpWt/VjqDUjDM2OQbN4qPSrShounOXEAgLNdxQMQikUiKqb4vjahU09V0wG\nS9dGqGjMg94NwNGqlNF/Yx+yIc2+1uUo2fBTaylLi0p8PNVArD7HvRTyHB/p2i5m\ngsjmfImYh1w72dIAovj2j9sddQKBgQDXbczZY5kaz0++F7gyalrMYQuwykChz97u\nCaJfb4LHE9cuc1TeayesnqyvTqwY7Hq/SC18VrTo4U2UNajpNZleO5JLaitZ9BRF\nMhNoQK13PHGqNmZXzk9Dh8gU4DipJYRpeBFDsZmT6J3qodeV13y1DKBbL2GuAA9u\ncy01FKyXuwKBgQDHsReQ9TEXxJWeqEgu5yzU3aFRUm35qYjswviAsekfjQdo/L9/\ncpXZdRsZnDCXhiGu12WDnEe/caew4OkIL+uTRcC66MFvva2TEzgHkA/w/B5uQWM6\nQjwuWOn4av6TsLaXH9QgqmubWnYDkbVwkFAjrh8XYwcF5jniLWJG/bdVcQKBgDVC\nFeSgdNdl7SbnokgEdxIT49n/Bl96jnh2tUe2v7QLuaToKlEaWKKaT8K/RlibDfWA\nGI6muO7h1FYRtgKBl7ruK0qtoq4IY4J/0MBzTO8vaEJWVJLclEfzp4lRrXBTsBqK\n7mm33GnulivNewi2T0RLLNGeMx3bMfVyT/jRdaHFAoGBAJBRsd80rCfnBgyw4kSk\np/ZmaZpr6i25jMn+jGb81VYcyUYvy+gemVsUOtT0DX5dgjqiWdVUHTqqSRDmbRdX\nChgTIqMuRo9KkEV0sM2Ev1y+/idi5oKIj0hV3b+lpVT0u9a57Fj8pFsMgl3ER29g\n5rH2j3pjV+WKrkWV+dZam2hE\n-----END PRIVATE KEY-----\n",
  "client_email": "esp-googlesheet@esp-casmir.iam.gserviceaccount.com",
  "client_id": "115321639341364521471",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/esp-googlesheet%40esp-casmir.iam.gserviceaccount.com"
}


credentials = ServiceAccountCredentials.from_json_keyfile_dict(config, scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("YABATECH STUDENTS")  #open sheet
students_sheet = sheet.sheet1  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

all_students = {}
students = []
ids = []
headings = []


def update_students_dict():
    global all_students, students, ids, headings
    all_students = {}
    students = []
    ids = []
    headings = []
    std = students_sheet.col_values(1)[1:]
    ids = students_sheet .col_values(2)[1:]
    all_students = {}
    for s in range(len(std)):
        if std[s] != '':
            all_students.update({ids[s]:std[s]})
    for h in students_sheet.row_values(1)[2:]:
        if h != "":
            headings.append(h)
    for s in std:
        if s != "":
            students.append(s)
    print("Updated Students")
    print(all_students)
    print(headings)
    print("students:",students)


def get_student_name(id):
    return all_students[str(id)]


def get_student_row_on_table(id):
    return ids.index(str(id)) + 2


def get_date():
    return str(datetime.utcnow().date())


def get_time():
    return str(datetime.utcnow().replace(hour=datetime.utcnow().hour+1)).split(" ")[1]


def add_attendance(id):
    global headings
    row = get_student_row_on_table(str(id))
    if not get_date() in headings:
        print("Creating new date column")
        students_sheet.update_cell(1, len(headings) + 3, get_date())
        # update heading
        update_students_dict()
        col = len(headings)+2
    else:
        print("date column exist")
        col = headings.index(get_date())+3
    time.sleep(1.5) #give it some time
    students_sheet.update_cell(row, col, get_time())


def add_student(name, id):
    row = len(students)+2
    students_sheet.update_cell(row, 1, name)  # name
    students_sheet.update_cell(row, 2, str(id))  # id
    update_students_dict()


def clear_attendance():
    students_sheet.clear()
    students_sheet.insert_row(["Name", "Print ID"], index=1)
    update_students_dict()


update_students_dict()
app = Flask(__name__)


@app.route("/get_name", methods=['GET'])
def get_n():
    id = request.args.get('id')
    return get_student_name(id)


@app.route("/add_student", methods=['GET'])
def add_s():
    try:
        name = request.args.get('name')
        id = request.args.get('id')
        add_student(name, id)
    except:
        pass
    return make_response('done!')


@app.route("/add_attendance", methods=['GET'])
def add_atd():
    try:
        id = request.args.get('id')
        add_attendance(id)
    except:
        pass
    return "done"


@app.route("/clr", methods=['GET'])
def clr():
    try:
        clear_attendance()
    except:
        pass
    return "done"

@app.route("/")
def home():
    return "ESP ATTENDANCE SERVER"


if __name__ == '__main__':
    app.run()

# #######################################################################################################

