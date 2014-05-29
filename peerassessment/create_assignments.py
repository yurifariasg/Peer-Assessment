import requests
import json
from datetime import datetime, date, time, timedelta

req = requests.post("http://localhost:8000/login", data=json.dumps({"email":"professor@mail.com", "password":"12345678"}))

print req.text
assert(req.status_code == 200)

cookies = req.cookies

def createDate(daysFromNow):
    end_date = datetime.utcnow()
    end_date += timedelta(days = daysFromNow)
    return end_date.strftime('%Y-%m-%dT%H:%M:%S')

content = {
    "name" : "New Assignment",
    "submission_end_date" : createDate(1),
    "discussion_end_date" : createDate(2),
    "grading_end_date" : createDate(3),
    "criterias" : [
        {"name" : "Hello Criteria", "weight" : 1.0}
    ]
}

req = requests.post("http://localhost:8000/assignment/create", data=json.dumps(content), cookies=cookies)
print req.text
assert(req.status_code == 200)
