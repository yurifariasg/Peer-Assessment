import requests
import json
from datetime import datetime, date, time, timedelta
from create_users import *

def test():
    professor_request = requests.post(BASE_URL + "/login", data=json.dumps({"email" : PROFESSOR_CREDENTIALS["email"], "password" : PROFESSOR_CREDENTIALS["password"]}))

    print professor_request.text
    assert(professor_request.status_code == 200)

    def createDate(daysFromNow):
        end_date = datetime.utcnow()
        end_date += timedelta(days = daysFromNow)
        return end_date.strftime('%Y-%m-%dT%H:%M:%S')

    content = {
        "name" : "New Assignment",
        "submission_end_date" : createDate(0),
        "discussion_end_date" : createDate(1),
        "grading_end_date" : createDate(2),
        "criterias" : [
            {"name" : "Hello Criteria", "weight" : 1.0}
        ]
    }

    professor_request = requests.post(BASE_URL + "/assignment/create", data=json.dumps(content), cookies=professor_request.cookies)
    print professor_request.text
    assert(professor_request.status_code == 200)

    assignment_id = json.loads(professor_request.text)["id"]

    student_request = requests.post(BASE_URL + "/login", data=json.dumps({"email" : STUDENT_CREDENTIALS["email"], "password" : STUDENT_CREDENTIALS["password"]}))
    print student_request.text
    assert(student_request.status_code == 200)

    student_cookies = student_request.cookies

    student_request = requests.post(BASE_URL + "/assignment/submit", data = json.dumps({"url" : "http://url.com", "assignment_id" : assignment_id}), cookies = student_cookies)

    print student_request.text
    assert(student_request.status_code == 200)

    student_request = requests.post(BASE_URL + "/assignment/submit", data = json.dumps({"url" : "http://url.com", "assignment_id" : assignment_id}), cookies = student_cookies)

    print student_request.text
    assert(student_request.status_code == 400) # BadRequest


    print "OK"

if __name__ == "__main__":
    test()
