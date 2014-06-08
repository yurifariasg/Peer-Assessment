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
    """
    json_body = json.loads(request.body)

    def get_date(parameter):
        if json_body.get(parameter):
            parameter_date = datetime.datetime.strptime(json_body.get(parameter), '%Y-%m-%dT%H:%M:%S')
            return parameter_date
        else:
            raise ValidationError({parameter : ["parameter does not exist."]})

    name = json_body.get("name")
    submission_end_date = get_date("submission_end_date")
    discussion_end_date = get_date("discussion_end_date")
    grading_end_date = get_date("grading_end_date")

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

    if weight_sum != 1.0:
        raise ValidationError({"weight_sum" : [ "sum must be 1.0" ]})

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

    return { "id" : assignment.id }
