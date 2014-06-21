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

def signup(request):
    """
        Signup endpoint.

        This is the endpoint for the user signup 
    """
    return render_to_response("signup.html")


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
@types_required(["student"])
def discussion_page(request, assignment_id = None):
    """
        Student Discussion endpoint.
        This is the endpoint for the student's discussion on a assignment
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    #allocation = Allocation.filter(assignment = assignment, student = request.user.student)
    allocation = get_object_or_404(Allocation, student = request.user.student, assignment = assignment)
    criterias = AssignmentCriteria.objects.filter(assignment = assignment).all()
    request_student = request.user.student

    content = {
        'user' : request.user,
        'assignment' : assignment,
        'peers' : {
            1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : []
        }
    }

    for criteria in criterias:
        for peer_id in content['peers'].keys():

            peer_student = get_peer(peer_id, allocation)

            messages = Message.objects.filter( \
                Q(owner = request_student, recipient = peer_student, criteria = criteria) |
                Q(owner = peer_student, recipient = request_student, criteria = criteria) \
                ).order_by('date').all()

            content['peers'][peer_id].append( \
                {"criteria" : criteria, \
                "messages": messages}
            )
    return render_to_response("student/discussion.html", \
        {'user': request.user, \
        'messages' : content})

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


@login_required()
@types_required(["student"])
def submit_assignment_page(request, assignment_id):

    assignment = get_object_or_404(Assignment, id=assignment_id)
    criterias = AssignmentCriteria.objects.filter(assignment = assignment).all()

    return render_to_response("student/submit_assignment.html", \
        {'user': request.user, 'criterias': criterias, 'assignment': assignment})







