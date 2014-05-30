from common import *

# Endpoints here are related to assignments.

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
        submission = None
        discussion = None
        grading = None
        created_criterias = []

        assignment = Assignment(name = name, owner = request.user.professor)
        assignment.full_clean()
        assignment.save()

        submission = AssignmentStage(name = 'Submission', assignment = assignment, end_date = submission_end_date)
        submission.full_clean()
        submission.save()

        discussion = AssignmentStage(name = 'Discussion', assignment = assignment, end_date = discussion_end_date)
        discussion.full_clean()
        discussion.save()

        grading = AssignmentStage(name = 'Grading', assignment = assignment, end_date = grading_end_date)

        grading.full_clean()
        grading.save()

        for criteria in criterias:
            created_criteria = AssignmentCriteria(text = criteria["name"], weight = criteria["weight"], assignment = assignment)

            created_criteria.full_clean()
            created_criteria.save()
            created_criterias.append(created_criteria)

        # TODO: Get Students from a discipline only
        students = Student.objects.all()
        assignment.students.add(*students)
        assignment.save()

    except Exception as e:
        if (assignment != None and assignment.id != None):
            assignment.delete()
        if (submission != None and submission.id != None):
            submission.delete()
        if (discussion != None and discussion.id != None):
            discussion.delete()
        if (grading != None and grading.id != None):
            grading.delete()
        for criteria in created_criterias:
            if criteria != None and criteria.id != None:
                criteria.delete()
        raise e

    return { "id" : assignment.id }
