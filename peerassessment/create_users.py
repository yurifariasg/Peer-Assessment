
BASE_URL = "http://localhost:8000"

import requests
import json

STUDENT_CREDENTIALS = {
	"name" : "student",
	"password" : "12345678",
	"email" : "student@mail.com",
	"type" : "student"
}

PROFESSOR_CREDENTIALS = {
	"name" : "professor",
	"password" : "12345678",
	"email" : "professor@mail.com",
	"type" : "professor"
}

# Create a student

result = requests.post(BASE_URL + "/register", data= json.dumps(STUDENT_CREDENTIALS))
assert(result.status_code == 200)
result = requests.post(BASE_URL + "/register", data= json.dumps(PROFESSOR_CREDENTIALS))
assert(result.status_code == 200)