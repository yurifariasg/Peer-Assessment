
BASE_URL = "http://localhost:8000"

import requests
import json

STUDENT_CREDENTIALS = {
	"firstname" : "Joao",
	"lastname" : "da Silva Pinto",
	"password" : "12345678",
	"email" : "student@mail.com",
	"type" : "student"
}

PROFESSOR_CREDENTIALS = {
	"firstname" : "Tomas",
	"lastname" : "Souza Fagundes",
	"password" : "12345678",
	"email" : "professor@mail.com",
	"type" : "professor"
}

# Create a student

def test():
	result = requests.post(BASE_URL + "/register", data= json.dumps(STUDENT_CREDENTIALS))
	assert(result.status_code == 200)
	result = requests.post(BASE_URL + "/register", data= json.dumps(PROFESSOR_CREDENTIALS))
	assert(result.status_code == 200)

	# Now, let create several students
	for i in range(20):

		credentials = {
			"firstname" : "student" + str(i),
			"lastname" : "test",
			"password" : "12345678",
			"email" : "student" + str(i) + "@mail.com",
			"type" : "student"
		}

		result = requests.post(BASE_URL + "/register", data= json.dumps(credentials))
		assert(result.status_code == 200)
	print "OK"

if __name__ == "__main__":
	test()
