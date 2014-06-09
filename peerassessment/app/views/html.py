from common import *

# View Endpoints
# Endpoints from here and below are used for common GET requests
# All these endpoints should render a HTML template for display

def index(request):
    """
        Index endpoint.

        This is the base endpoint of the page.
    """
    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            return redirect(reverse(student_dashboard))
        elif hasattr(request.user, 'professor'):
            return redirect(reverse(professor_dashboard))

    return render_to_response("index.html")


@login_required()
@types_required(["student"])
def student_dashboard(request):
    """
        Student Dashboard endpoint.

        This is the endpoint for the student's dashboard.
    """
    return render_to_response("student/index.html", \
        {'user':request.user, 'assignments': list(request.user.student.assignments.all())})

@login_required()
@types_required(["professor"])
def professor_dashboard(request):
    """
        Professor Dashboard endpoint.

        This is the endpoint for the professor's dashboard.
    """
    assignments = list(Assignment.objects.filter(owner = request.user.professor).all())

    return render_to_response("professor/index.html", \
        {'user': request.user, 'assignments': assignments})

@login_required()
@types_required(["professor"])
def create_assignment_page(request):
    return render_to_response("professor/create_assignment.html", \
        {'user': request.user})
