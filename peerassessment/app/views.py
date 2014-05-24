from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import *
import json
import logging
from django.db import *

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
        { "name" : "user name" , "login" : "user login", "password" : "user password" }

        Returns:
        HTTP Code 200: Id of the User
        HTTP Code 400: E-mail already in use or other exception
    """
    if (request.method != "POST"):
        return HttpResponse("Method Not Allowed", status=405)
    try:
        jsonBody = json.loads(request.body)

        name = jsonBody.get("name")
        login = jsonBody.get("login")
        password = jsonBody.get("password") # TODO: Should encrypt

        credential = Credential.objects.create(login = login, password = password)
        student = Student.objects.create(name = name, credential = credential)

        if credential.id != None and student.id != None:
            return HttpResponse(student.id, status=200)

    except IntegrityError as e:
        return HttpResponse("E-mail already in use", status=400)
    except Exception as e:
        logger.debug(e)
        pass
    return HttpResponse("Bad Request", status=400)
