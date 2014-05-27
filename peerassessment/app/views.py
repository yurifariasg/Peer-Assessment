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
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from exceptions import *
from django.contrib.auth.hashers  import *
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)


# View Decorators
# Functions here are usesul as decorator for the endpoints below
# They perform useful tasks that are common to several endpoints

def ajax_endpoint(func):
    def func_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return HttpResponse(json.dumps(result), status = HTTP_200_OK)
        except MethodNotAllowedException as e:
            return HttpResponse(status = HTTP_405_METHOD_NOT_ALLOWED)
        except ValidationError as e:
            return HttpResponse(json.dumps(e.message_dict), status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(json.dumps({"error" : e.message}))
    return func_wrapper

# View Endpoints
# Endpoints from here and below are used for GET requests
# All these endpoints should render a HTML template for display

def index(request):
    """ Index endpoint.

        This is the base endpoint of the page.
    """
    return render_to_response("index.html")


@login_required()
def student_dashboard(request):
    return HttpResponse("You are authenticated as " + str(request.user.student))


# AJAX Endpoints
# Endpoints from here and below are used from AJAX-like requests
# They do not render any HTML but work like a REST API.
# Receiving content as JSON and replying with JSON content and HTTP Codes.

@ajax_endpoint
def register(request):
    """
        Register endpoint.
        
        This method register a new user from a HTTP POST Request.
        The content of this request should be a json formatted as:
        { "name" : "user name" , "email" : "user email",
        "password" : "user password", "type" : "student" }

        Returns:
        HTTP Code 201: The created user
        HTTP Code 400: JSON containing the invalid parameters
    """
    if (request.method != "POST"):
        raise MethodNotAllowedException()

    jsonBody = json.loads(request.body)

    name = jsonBody.get("name")
    email = jsonBody.get("email")
    password = jsonBody.get("password")
    userType = jsonBody.get("type")

    if len(password) < 8:
        raise ValidationError({"password": ["password has less than 8 characters."]})

    user = User(username = name, email = email, password = make_password(password))
    user.full_clean()
    user.save()

    try:
        person = None
        if userType != None and userType.lower() == "student":
            person = Student(user = user)
        elif userType != None and userType.lower() == "professor":
            person = Professor(user = user)
        else:
            raise ValidationError({"type": ["type not found"]})

        if person != None:
            person.full_clean()
            person.save()
            return HttpResponse(str(person), status = HTTP_201_CREATED)

    except Exception as e:
        # In case we fail to create the student. Delete credentials.
        user.delete()
        raise e # Re-throw the exception

@ajax_endpoint
def logout_user(request):
    """
        Logout endpoint.
        
        This method logs a user out of the current session.

        Returns:
        HTTP Code 200: An empty json
        HTTP Code 400: JSON containing the invalid parameters
    """
    if request.user.is_authenticated():
        logout(request)
        return {}
    else:
        raise BadRequestException({"error": ["user not logged."]})

@ajax_endpoint
def login_user(request):
    """
        Login endpoint.
        
        This method authenticates a user from a HTTP POST Request
        and saves its id on the current session.
        The content of this request should be a json formatted as:
        {"email" : "user email", "password" : "user password" }

        Returns:
        HTTP Code 200: The logged user
        HTTP Code 400: JSON containing the invalid parameters
    """
    if (request.method != "POST"):
        raise MethodNotAllowedException()

    jsonBody = json.loads(request.body)

    email = jsonBody.get("email")
    password = jsonBody.get("password")

    logged_user = authenticate(email=email, password=password)
    if logged_user is not None:
        if logged_user.is_active:
            login(request, logged_user)
            # Redirect to a success page.
            return {"user" : str(logged_user)}
        else:
            # Return a 'disabled account' error message
            raise BadRequestException({"error": ["disabled account."]})
    else:
        # Return an 'invalid login' error message.
        raise BadRequestException({"error": ["invalid login."]})
