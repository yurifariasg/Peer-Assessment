from django.shortcuts import render
from django.shortcuts import render_to_response
from models import *

# Place our views here
def index(request):
    template = { 'complement' : 'World', 'student_count' : len(Student.objects.all()) }
    return render_to_response("index.html", template)
