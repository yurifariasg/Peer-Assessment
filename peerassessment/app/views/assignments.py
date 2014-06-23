from common import *

# Endpoints here are related to assignments.

@require_http_methods(["POST"])
@login_required_ajax()
@types_required(["student"])
@ajax_endpoint
def submit(request):
    """
        Submits an assignment.
        This API shall receive the URL from a student for a open assignment.
        The JSON content should have the following format:
        {
            "url" : "a valid url",
            "assignment_id" : "the assignment id"
        }
    """
    json_body = json.loads(request.body)

    url = json_body.get("url")
    assignment_id = json_body.get("assignment_id")

    if not url:
        raise ValidationError({"url" : ["Field cannot be blank."]})
    if not assignment_id:
        raise ValidationError({"assignment_id" : ["Field cannot be blank."]})

    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except:
        raise ValidationError({"assignment_id" : ["Not found."]})

    submission = Submission( \
        student = request.user.student, \
        assignment = assignment, \
        url = url \
        )

    submission.full_clean()
    submission.save()

    return { }

@require_http_methods(["POST"])
@login_required_ajax()
@types_required(["student"])
@ajax_endpoint
def grade(request):
    """
    Grading assignment endpoint
    The API shall receive the grade for each one of
    the criterias for the paired students.
    The content should be a json in the following format:
    {
        "assignment" : 1,
        "grades" : [
            {
                "peer" : 1,
                "grades" : [
                    {
                        "criteria" : 1,
                        "grade" : 8.0
                    },
                    {
                        "criteria" : 2,
                        "grade" : 5.0
                    }
            },
            {
                "peer" : 2,
                "grades" : [
                    {
                        "criteria" : 1,
                        "grade" : 7.0
                    },
                    {
                        "criteria" : 2,
                        "grade" : 10.0
                    }
            }
        ]
    }
    Grades must go from 0.0 to 10.0
    """
    json_body = json.loads(request.body)
    assignment_id = json_body.get("assignment", -1)
    json_grades = json_body.get("grades", [])

    requesting_student = request.user.student
    assignment = Assignment.get(id=assignment_id)
    allocation = Allocation.get(assignment=assignment, student=requesting_student)



    grades = []

    for peer_body in json_body:
        peer_id = peer_body.get("peer")
        peer_grades = peer_body.get("grades", [])

        for peer_grade in peer_grandes:

            # assert criteria is from this assignment
            criteria = peer_grade.get("criteria", -1)

            grade = Grade( \
                grade = peer_grade.get("grade"), \
                assignment = assignment, \
                owner = requesting_student, \
                student = get_peer(peer_id, allocation), \
                criteria = criteria \
            )
            grade.full_clean()
            grades.append(grade)

    for grade in grades:
        grade.save()

    return { }


@require_http_methods(["POST"])
@login_required_ajax()
@types_required(["professor"])
@ajax_endpoint
def create(request):
    """
        Create assignment endpoint
         The API shall receive the name of the assignment,
         the end date for each stage: Submission, Discussion,
         Grading, the criterias and their weight in the final grade.
         The content should be a json in the following format:
         {
             "name" : "Assignment Name",
             "submission_end_date" : "Y-m-dTH:M:S",
             "discussion_end_date" : "Y-m-dTH:M:S",
             "grading_end_date" : "Y-m-dTH:M:S",
             "criterias" : [
                 {"name" : "Criteria Name", "weight" : 1.0}
             ]
         }
         Criterias weight must sum to 1.0.
         Dates must be in UTC.
    """
    json_body = json.loads(request.body)

    name = json_body.get("name")
    submission_end_date = get_date("submission_end_date", json_body)
    discussion_end_date = get_date("discussion_end_date", json_body)
    grading_end_date = get_date("grading_end_date", json_body)

    json_criterias = json_body.get("criterias", [])
    criterias = []

    weight_sum = 0.0

    for criteria in json_criterias:
        criteria_name = criteria.get("name")
        criteria_weight = criteria.get("weight")

        try:
            criteria_weight = float(criteria_weight)
            weight_sum += criteria_weight
            criterias.append({"name" : criteria_name, "weight" : criteria_weight })
        except ValueError:
            raise ValidationError({"weight" : ["not a valid float value"]})

    if abs(weight_sum - 1.0) > 0.001:
        raise ValidationError({"weight_sum" : [ "sum must be 1.0, it is " + str(weight_sum) ]})

    try:
        created_criterias = []

        assignment = Assignment(
            name = name, \
            owner = request.user.professor, \
            submission_end_date = submission_end_date, \
            discussion_end_date = discussion_end_date, \
            grading_end_date = grading_end_date, \
            )
        assignment.full_clean()
        assignment.save()

        for criteria in criterias:
            created_criteria = AssignmentCriteria(text = criteria["name"], weight = criteria["weight"], assignment = assignment)

            created_criteria.full_clean()
            created_criteria.save()
            created_criterias.append(created_criteria)

        # TODO: Get Students from a discipline only
        students = Student.objects.all()
        assignment.student_set.add(*students)
        assignment.save()

    except Exception as e:
        if (assignment != None and assignment.id != None):
            assignment.delete()
        for criteria in created_criterias:
            if criteria != None and criteria.id != None:
                criteria.delete()
        raise e

    return { "id" : assignment.id, "criterias" : [ created_criteria.id for created_criteria in created_criterias ] }

@require_http_methods(["POST"])
@login_required_ajax()
@types_required(["professor"])
@ajax_endpoint
def edit(request):
    """
        Edit an assignment endpoint
        The API shall receive the name of the assignment,
        the end date for each stage: Submission, Discussion,
        Grading, the criterias and their weight in the final grade.
        The content should be a json in the following format:
        {
            "id" : assignment_id
            "name" : "Assignment Name",
            "submission_end_date" : "Y-m-dTH:M:S",
            "discussion_end_date" : "Y-m-dTH:M:S",
            "grading_end_date" : "Y-m-dTH:M:S",
            "criterias" : [
                 {"id" : id, "name" : "Criteria Name", "weight" : 1.0}
            ]
        }
        Criterias weight must sum to 1.0.
        The criteria id is optional, if not provided, a new criteria will be created.
        All criterias should be specified on the request, otherwise they will be deleted.
        Dates must be in UTC.
    """
    json_body = json.loads(request.body)

    name = json_body.get("name")
    submission_end_date = get_date("submission_end_date", json_body)
    discussion_end_date = get_date("discussion_end_date", json_body)
    grading_end_date = get_date("grading_end_date", json_body)

    json_criterias = json_body.get("criterias", [])
    criterias = []

    weight_sum = 0.0

    for criteria in json_criterias:
        criteria_id = criteria.get("id", None)
        criteria_name = criteria.get("name", None)
        criteria_weight = criteria.get("weight", None)

        try:
            criteria_weight = float(criteria_weight)
            weight_sum += criteria_weight
            criterias.append({"id" : criteria_id, "name" : criteria_name, "weight" : criteria_weight })
        except ValueError:
            raise ValidationError({"weight" : ["not a valid float value"]})

    if abs(weight_sum - 1.0) > 0.001:
        raise ValidationError({"weight_sum" : [ "sum must be 1.0, it is " + str(weight_sum) ]})

    try:
        edited_criterias = []
        assignment = Assignment.objects.get(id = json_body.get("id"))

        if name:
            assignment.name = name

        if submission_end_date:
            assignment.submission_end_date = submission_end_date

        if discussion_end_date:
            assignment.discussion_end_date = discussion_end_date

        if grading_end_date:
            assignment.grading_end_date = grading_end_date

        assignment.full_clean()
        assignment.save()

        for criteria in criterias:
            if criteria.get("id"):
                model_criteria = AssignmentCriteria.objects.get(id = criteria["id"])
                model_criteria.text = criteria["name"]
                model_criteria.weight = criteria["weight"]
            else:
                model_criteria = AssignmentCriteria(\
                    text = criteria["name"], weight = criteria["weight"], assignment = assignment)

            model_criteria.full_clean()
            model_criteria.save()
            edited_criterias.append(model_criteria)

        # Now, delete criterias that were not send on the request
        all_model_assignment_criterias = AssignmentCriteria.objects.filter(assignment = assignment)
        for criteria in all_model_assignment_criterias:
            wasEdited = False
            for edited_criteria in edited_criterias:
                if criteria.id == edited_criteria.id:
                    wasEdited = True
                    break

            if not wasEdited:
                criteria.delete()

        # Now, update the assignment stage.
        assignment.updateStage()

        assignment.save()

    except Exception as e:
        raise e

    return { }

@require_http_methods(["POST"])
@login_required_ajax()
@types_required(["student"])
@ajax_endpoint
def send_messages(request):
    """
        Send messages to peers in an assignment's criteria.
        It reseives a list of messages.
        The content should be a json in the following format:
        {
            "assignment_id" : assignment_id,
            "messages" : [{
                "peer" : peer_id,
                "criteria" : criteria_id,
                "message" : "message content"
            }]
        }
    """
    json_body = json.loads(request.body)
    assignment_id = json_body.get("assignment_id")

    parsed_messages = []
    messages = json_body.get("messages", [])

    assignment = Assignment.objects.get(id = assignment_id)
    allocation = Allocation.objects.get( \
        student = request.user.student, assignment = assignment)

    def get_criteria(criteria_id):
        criteria = AssignmentCriteria.objects.get(id = criteria_id)
        assert(criteria.assignment == assignment)
        return criteria

    for message in messages:

        criteria = get_criteria(message.get("criteria"))
        if criteria.assignment != assignment:
            raise ValidationError({"criteria" : ["Criteria not from assignment."]})

        message = Message( \
            owner = request.user.student, \
            recipient = get_peer(message.get("peer"), allocation), \
            criteria = criteria, \
            text = message.get("message", ""))
        message.full_clean()

        parsed_messages.append(message)

    for parsed_message in parsed_messages:
        parsed_message.save()

    return { }
