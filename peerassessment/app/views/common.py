from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from app.models import *
import json
import logging
from django.db import *
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from app.status import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from app.exceptions import *
from django.contrib.auth.hashers  import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.core.urlresolvers import reverse
import datetime
try:
    from functools import wraps
except:
    from django.utils.functional import wraps

# Get an instance of a logger
logger = logging.getLogger(__name__)

# View Decorators
# Functions here are usesul as decorator for the other endpoints
# They perform useful tasks that are common to several methods.

def ajax_endpoint(func):
    """
        Formats the response to the JSON format
        and handles exceptions for AJAX endpoints
    """
    def func_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return HttpResponse(json.dumps(result), status = HTTP_200_OK)
        except MethodNotAllowedException as e:
            return HttpResponse(status = HTTP_405_METHOD_NOT_ALLOWED)
        except ValidationError as e:
            return HttpResponse(json.dumps(e.message_dict), status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(json.dumps({"error" : e.message}), status = HTTP_500_INTERNAL_SERVER_ERROR)
    return func_wrapper

def login_required_ajax(function=None,redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax view

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)

def types_required(types=[]):
    """
        Checks if the logged user inside the request
        has one of the required types
    """
    def decorator(func):
        def inner_decorator(request,*args, **kwargs):
            for type in types:
                try:
                    if hasattr(request.user, type):
                        return func(request, *args, **kwargs)
                except:
                    pass
            raise PermissionDenied()
        return wraps(func)(inner_decorator)
    return decorator