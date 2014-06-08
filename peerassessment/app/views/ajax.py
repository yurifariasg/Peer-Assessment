from common import *
from html import *

# AJAX Endpoints
# This file holds commons endspoints for AJAX-like requests
# They do not render any HTML but work like a REST API.
# Receiving content as JSON and replying with JSON content and HTTP Codes.

@require_http_methods(["POST"])
@ajax_endpoint
def register(request):
    """
        Register endpoint.

        This method register a new user from a HTTP POST Request.
        The content of this request should be a json formatted as:
        { "firstname" : "first name" , "lastname" : "last name",
        "email" : "user email", "password" : "user password",
        "type" : "student" }
        
        Returns:
        HTTP Code 200: The created user
        HTTP Code 400: JSON containing the invalid parameters
    """
    json_body = json.loads(request.body)

    firstname = json_body.get("firstname")
    lastname = json_body.get("lastname")
    username = firstname + lastname
    username = username.replace(" ", "").lower()
    print username
    email = json_body.get("email")
    password = json_body.get("password")
    userType = json_body.get("type")

    if len(password) < 8:
        raise ValidationError({"password": ["password has less than 8 characters."]})

    user = User(username = username, \
         first_name = firstname, last_name = lastname, \
         email = email, password = make_password(password))
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
            return { "user" : str(person) }

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

@require_http_methods(["POST"])
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
    json_body = json.loads(request.body)

    email = json_body.get("email")
    password = json_body.get("password")

    logged_user = authenticate(email=email, password=password)
    if logged_user is not None:
        if logged_user.is_active:
            login(request, logged_user)
            # Redirect to a success page.

            url = ""
            if hasattr(logged_user, 'student'):
                url = reverse(student_dashboard)
            elif hasattr(logged_user, "professor"):
                url = reverse(professor_dashboard)

            return {"url" : url, "session_id" : request.session._session_key}
        else:
            # Return a 'disabled account' error message
            raise BadRequestException({"error": ["disabled account."]})
    else:
        # Return an 'invalid login' error message.
        raise BadRequestException({"error": ["invalid login."]})
