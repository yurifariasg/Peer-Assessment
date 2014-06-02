from datetime import datetime
from models import *
from django.utils import timezone
import random

# This file holds functions related to the update of stages of an assignment.

def update_assignments():
    """
        Checks for assignments that needs to be updated and perform update operations.
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

    print str(len(needs_update_submission)) + " needs to update from submission"
    print str(len(needs_update_discussion)) + " needs to update from discussion"
    print str(len(needs_update_grading)) + " needs to update from grading"

    for assignment in needs_update_submission:

        # Should do the allocation
        allocate(assignment)

        assignment.stage = "Discussion"
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

    if len(participants) < 5:
        raise ValidationError({"Assignment": ["Has less than 5 submissions."]})

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
            peer3 = participants[i + 1 - len(participants)]
        else:
            peer3 = participants[i + 1]

        if i + 2 >= len(participants):
            peer4 = participants[i + 2 - len(participants)]
        else:
            peer4 = participants[i + 2]

        allocations.append(Allocation( \
            student = participants[i], \
            peer1 = peer1, \
            peer2 = peer2, \
            peer3 = peer3, \
            peer4 = peer4 ) )

    for allocation in allocations:
        allocation.save()
