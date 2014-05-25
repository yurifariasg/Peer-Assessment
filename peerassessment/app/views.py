from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import *
import json
import logging
from django.db import *
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from status import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

# View Endpoints
# Endpoints frmo here and below are used for GET requests
# All these endpoints should render a HTML template for display

def index(request):
    """ Index endpoint.

        This is the base endpoint of the page.
    """
    template = { 'complement' : 'World', 'student_count' : len(Student.objects.all()) }
    return render_to_response("index.html", template)



# AJAX Endpoints
# Endpoints from here and below are used from AJAX-like requests
# They do not render any HTML but work like a REST API.
# Receiving content as JSON and replying with JSON content and HTTP Codes.

def register(request):
    """
        Register endpoint.
        
        This method register a new user from a HTTP POST Request.
        The content of this request should be a json formatted as:
        { "name" : "user name" , "email" : "user email",
        "password" : "user password", "type" : "student" }

        Returns:
        HTTP Code 200: The created user
        HTTP Code 400: JSON containing the invalid parameters
    """
    if (request.method != "POST"):
        return HttpResponse("Method Not Allowed", status = HTTP_405_METHOD_NOT_ALLOWED)
    try:
        jsonBody = json.loads(request.body)

        name = jsonBody.get("name")
        email = jsonBody.get("email")
        password = jsonBody.get("password") # TODO: Should encrypt
        userType = jsonBody.get("type")

        credential = Credential(email = email, password = password)
        credential.full_clean()
        credential.save()

        try:
            user = None
            if userType != None and userType.lower() == "student":
                user = Student(name = name, credential = credential)
            elif userType != None and userType.lower() == "professor":
                user = Professor(name = name, credential = credential)
            else:
                raise ValidationError({"type": ["type not found"]})

            if user != None:
                user.full_clean()
                user.save()
                return HttpResponse(str(user), status = HTTP_201_CREATED)

        except Exception as e:
            # In case we fail to create the student. Delete credentials.
            credential.delete()
            raise e # Re-throw the exception

    except ValidationError as e:
        return HttpResponse(json.dumps(e.message_dict), status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(json.dumps({"error" : e.message}))
    return HttpResponse("{}", status = HTTP_400_BAD_REQUEST)
