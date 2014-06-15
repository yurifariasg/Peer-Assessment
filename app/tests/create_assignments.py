import requests
import json
from datetime import datetime, date, time, timedelta
from create_users import *
import time

def test():
    professor_request = requests.post(BASE_URL + "/login", data=json.dumps({"email" : PROFESSOR_CREDENTIALS["email"], "password" : PROFESSOR_CREDENTIALS["password"]}))

    print professor_request.text
    assert(professor_request.status_code == 200)

    def createDate(daysFromNow):
        end_date = datetime.utcnow()
        end_date += timedelta(minutes = daysFromNow)
        return end_date.strftime('%Y-%m-%dT%H:%M:%S')

    content = {
        "name" : "New Assignment",
        "submission_end_date" : createDate(0),
        "discussion_end_date" : createDate(1),
        "grading_end_date" : createDate(2),
        "criterias" : [
            {"name" : "Portugues da Atividade", "weight" : 0.2},
            {"name" : "Criterio de avaliacao que voce deve responder", "weight" : 0.3},
            {"name" : "Criterio de avaliacao que voce deve responder", "weight" : 0.1},
            {"name" : "Criterio de avaliacao que voce deve responder", "weight" : 0.4}
        ]
    }

    professor_request = requests.post(BASE_URL + "/assignment/create", data=json.dumps(content), cookies=professor_request.cookies)
    print professor_request.text
    assert(professor_request.status_code == 200)

    assignment_id = json.loads(professor_request.text)["id"]
    criteria_id = json.loads(professor_request.text)["criterias"][0]

    for student in STUDENTS_CREDENTIALS:
        student_request = requests.post(BASE_URL + "/login", data=json.dumps({"email" : student["email"], "password" : student["password"]}))
        print student_request.text
        assert(student_request.status_code == 200)

        student_cookies = student_request.cookies
        student["cookies"] = student_cookies

        student_request = requests.post(BASE_URL + "/assignment/submit", data = json.dumps({"url" : "http://url.com", "assignment_id" : assignment_id}), cookies = student_cookies)

        print student_request.text
        assert(student_request.status_code == 200)

        student_request = requests.post(BASE_URL + "/assignment/submit", data = json.dumps({"url" : "http://url.com", "assignment_id" : assignment_id}), cookies = student_cookies)

        print student_request.text
        assert(student_request.status_code == 400) # BadRequest

    time.sleep(60)

    print "Sending Messages..."
    for student in STUDENTS_CREDENTIALS:

        message = {
            "assignment_id" : assignment_id,
            "messages" : [{
                "peer" : 1,
                "criteria" : criteria_id,
                "message" : "to peer 1"
            },
            {
                "peer" : 2,
                "criteria" : criteria_id,
                "message" : "to peer 2"
            },
            {
                "peer" : 3,
                "criteria" : criteria_id,
                "message" : "to peer 3"
            },
            {
                "peer" : 4,
                "criteria" : criteria_id,
                "message" : "to peer 4"
            },
            {
                "peer" : 5,
                "criteria" : criteria_id,
                "message" : "to peer 5"
            }]
        }
        student_request = requests.post(BASE_URL + "/assignment/message", data = json.dumps(message), cookies = student["cookies"])
        print student_request.text
        assert(student_request.status_code == 200)


    print "OK"

if __name__ == "__main__":
    test()
