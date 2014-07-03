from common import *

# Endpoints here are related to assignments.

@require_http_methods(["GET"])
@login_required_ajax()
@types_required(["student"])
@ajax_endpoint
def allocation(request, assignment_id):
    """
        Gets the submissions for a user's peers on a given assignment.
    """
    assignment = Assignment.objects.get(pk = assignment_id)
    allocation = Allocation.objects.get(\
        student = request.user.student,\
        assignment = assignment)

    # Get submissions for each peer
    submissions = assignment_service.get_submissions_of_peers(assignment = assignment, allocation = allocation)

    # Filter to show only Submission ID, URL and Peer Num
    for peer_num in submissions.keys():
        submission = submissions[peer_num]
        submissions[peer_num] = {\
            "submission_id" : submission.id, \
            "url" : submission.url \
        }

    return submissions

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

    assignment_service.create_submission(request.user.student, assignment, url)

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
    assignment = Assignment.objects.get(id=assignment_id)
    allocation = Allocation.objects.get(assignment=assignment, student=requesting_student)
    submissions = assignment_service.get_submissions_of_peers(assignment, allocation)

    grades = []

    for peer_body in json_grades:
        peer_id = peer_body.get("peer")
        peer_grades = peer_body.get("grades", [])

        for peer_grade in peer_grades:

            # assert criteria is from this assignment
            criteria_id = peer_grade.get("criteria", -1)
            criteria = AssignmentCriteria.objects.get(id = criteria_id)

            assignment_service.create_or_update_grade(requesting_student, assignment,\
                submissions[peer_id], criteria, peer_grade.get("grade"))

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

    assignment = None
    try:
        created_criterias = []

        assignment = assignment_service.create_or_update_assignment(name, \
            request.user.professor, submission_end_date, discussion_end_date,\
            grading_end_date)

        for criteria in criterias:
            created_criteria = assignment_service.create_or_update_criteria(\
                criteria["name"], criteria["weight"], assignment)

            created_criterias.append(created_criteria)

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
            model_criteria = assignment_service.create_or_update_criteria(\
                criteria["name"], criteria["weight"], assignment, criteria.get("id"))
            edited_criterias.append(model_criteria)

        # Now, delete criterias that were not sent on the request
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
        assignment.update_stage()

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
        It receives a list of messages.
        The related_peer property tells from which peer the conversation
        is identified from the relation submission_owner <-> related_peer
        If it is not specified, the related_peer will be the sender.
        This means that the sender is commenting on somebody else submission.
        This property should only be used IF the sender IS the owner of the submission.
        The content should be a json in the following format:
        [
            {
                "submission" : submission_id,
                "criteria" : criteria_id,
                "message" : "message content",
                "related_peer" : peer (1-5, Optional)
            },
            {
                "submission" : submission_id,
                "criteria" : criteria_id,
                "message" : "message content",
                "related_peer" : peer (1-5, Optional)
            }
        ]
    """
    messages = json.loads(request.body)
    # Sort messages based on submission_id to increase algorithm efficiency later...
    messages.sort(key=lambda x: x['submission'])

    parsed_messages = []

    for message in messages:

        submission = Submission.objects.get(id = message.get("submission"))
        criteria = AssignmentCriteria.objects.get(id = message.get("criteria"))

        # Validate Criteria
        message_service.validate_criteria(criteria, submission)
        # Validate Sender
        message_service.validate_message_sender(request.user.student, submission)

        # Send Message
        message_service.submit_message_to(message.get("message"), submission, criteria, request.user.student, message.get("related_peer"))

    return { }
