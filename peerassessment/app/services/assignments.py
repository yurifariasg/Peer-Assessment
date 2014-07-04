from common import *

def create_or_update_criteria(description, weight, assignment, id = None):
    """
        Creates or updates an existing criteria if id is passed.
        The criteria is created/updated using the given data.
    """
    if not id:
        # Creating
        criteria = AssignmentCriteria(text = description, weight = weight,\
            assignment = assignment)
    else:
        # Editing
        criteria = AssignmentCriteria.objects.get(id)
        criteria.text = description
        criteria.weight = weight
        criteria.assignment = assignment

    criteria.full_clean()
    criteria.save()
    return criteria

def create_or_update_assignment(name, owner, submission_end_date, discussion_end_date,\
        grading_end_date, id = None):
    """
        Creates or updates an existing assignment if id is passed.
        The assignment is created/updated using the given data.
    """
    if not id:
        # Creating
        assignment = Assignment(
            name = name, \
            owner = owner, \
            submission_end_date = submission_end_date, \
            discussion_end_date = discussion_end_date, \
            grading_end_date = grading_end_date)
    else:
        # Editing
        assignment = Assignment.objects.get(id = id)
        assignment.name = name
        assignment.owner = owner
        assignment.submission_end_date = submission_end_date
        assignment.discussion_end_date = discussion_end_date
        assignment.grading_end_date = grading_end_date

    assignment.full_clean()
    assignment.save()

    if not id:
        # If newly created, add students (can't add before)
        # TODO: Get Students from a discipline only
        students = Student.objects.all()
        assignment.student_set.add(*students)
        assignment.save()

    return assignment

def create_or_update_grade(grade_giver, assignment, submission, criteria, grade_value):
    """
        Creates or updates an existing grade.
        A grade will be updated if the system already have a grade with the same
        the assignment, owner, submission and criteria.
        The grade is created and updated using the given data.
    """
    existing_grade = Grade.objects.filter(\
        assignment = assignment, \
        owner = grade_giver, \
        submission = submission, \
        criteria = criteria \
    ).first()

    if existing_grade:
        grade = existing_grade
        grade.grade = grade_value
    else:
        grade = Grade( \
            grade = grade_value, \
            assignment = assignment, \
            owner = grade_giver, \
            submission = submission, \
            criteria = criteria \
        )

    grade.full_clean()
    grade.save()
    return grade

def get_submissions_of_peers(assignment, allocation):
    """
        Gets the submissions of the peers from the given allocation.
    """
    return {
        1: Submission.objects.get(assignment = assignment, student = allocation.peer1),
        2: Submission.objects.get(assignment = assignment, student = allocation.peer2),
        3: Submission.objects.get(assignment = assignment, student = allocation.peer3),
        4: Submission.objects.get(assignment = assignment, student = allocation.peer4),
        5: Submission.objects.get(assignment = assignment, student = allocation.peer5)
    }

def create_or_update_submission(owner, assignment, url):
    """
        Create or updates a submission with the given parameters.
        A submission is updated if there already exists a submission
        with the same owner and assignment.
    """
    submission = Submission.objects.filter(student = owner, assignment = assignment).first()

    if submission:
        submission.url = url
    else:
        submission = Submission( \
            student = owner, \
            assignment = assignment, \
            url = url)

    submission.full_clean()
    submission.save()

    return submission

def update_assignments():
    """
        Checks for assignments that needs to be updated and perform update operations.
        This updates is solely related to the STAGE of an assignment.
    """
    assignments = Assignment.objects.exclude( \
        stage="Closed")

    needs_update_submission = []
    needs_update_discussion = []
    needs_update_grading = []
    now = timezone.now()

    for assignment in assignments:
        if assignment.stage == "Submission" and \
            assignment.submission_end_date < now:
            needs_update_submission.append(assignment)

        elif assignment.stage == "Discussion" and \
            assignment.discussion_end_date < now:
            needs_update_discussion.append(assignment)

        elif assignment.stage == "Grading" and \
            assignment.grading_end_date < now:
            needs_update_grading.append(assignment)

    for assignment in needs_update_submission:
        # Should do the allocation
        allocate(assignment)

        assignment.stage = "Discussion"
        assignment.save()

    for assignment in needs_update_discussion:
        assignment.stage = "Grading"
        assignment.save()

    for assignment in needs_update_grading:
        assignment.stage = "Closed"
        assignment.save()


def allocate(assignment):
    """
        Allocates students in an assignment.
        This function only allocates students that had submitted the assignment.

        The allocation is done using the Jacques' Algorithm, available at:
        https://sites.google.com/site/fpcc12014/avaliacao
    """
    # This has a huge memory overhead, due to the QuerySet evaluation
    # We need to improve this later on
    # https://docs.djangoproject.com/en/dev/ref/models/querysets/#when-querysets-are-evaluated
    submissions = Submission.objects.filter(assignment = assignment)
    participants = list([submission.student for submission in submissions])
    random.shuffle(participants)

    allocations = []

    if len(participants) < 5 and settings.FORCE_5_STUDENTS_MINIMUM_ALLOCATION:
        raise ValidationError({"Could not allocate": ["has less than 5 submissions."]})

    print "Allocating " + str(len(participants)) + " participants..."
    # Perform Jacques' Algorithm
    for i in range(len(participants)):

        if i - 2 < 0:
            peer1 = participants[i - 2 + len(participants)]
        else:
            peer1 = participants[i - 2]

        if i - 1 < 0:
            peer2 = participants[i - 1 + len(participants)]
        else:
            peer2 = participants[i - 1]

        if i + 1 >= len(participants):
            peer4 = participants[i + 1 - len(participants)]
        else:
            peer4 = participants[i + 1]

        if i + 2 >= len(participants):
            peer5 = participants[i + 2 - len(participants)]
        else:
            peer5 = participants[i + 2]

        allocations.append(Allocation( \
            student = participants[i], \
            assignment = assignment, \
            peer1 = peer1, \
            peer2 = peer2, \
            peer3 = participants[i], \
            peer4 = peer4, \
            peer5 = peer5 ) )

    # Just in case, we delete all previous allocations on this assignment
    existing_allocations = Allocation.objects.filter(assignment = assignment)
    existing_allocations.delete()

    # Now we save
    for allocation in allocations:
        allocation.save()
    print "Allocation Complete..."
