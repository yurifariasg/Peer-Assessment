
from django.core.exceptions import *

# Place system-defined exceptions here

class MethodNotAllowedException(Exception):
    """
    MethodNotAllowedException
    
    This exception encapsulates the HTTP Error MethodNotAllowed
    """
    pass

class BadRequestException(ValidationError):
    """
    BadRequestException
    
    This exception encapsulates the HTTP Error BadRequest.
    It extends ValidationError because both has the same meaning
    inside the system.
    """
    pass