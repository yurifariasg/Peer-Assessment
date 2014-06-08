from common import *

# View Endpoints
# Endpoints from here and below are used for common GET requests
# All these endpoints should render a HTML template for display

def index(request):
    """
        Index endpoint.

        This is the base endpoint of the page.
    """
    return render_to_response("index.html")


@login_required()
@types_required(["student"])
def student_dashboard(request):
    return render_to_response("student/index.html", {'user':request.user.username})

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
