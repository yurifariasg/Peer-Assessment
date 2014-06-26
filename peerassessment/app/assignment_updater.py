from datetime import datetime
from models import *
from django.utils import timezone
import random
import assignment_utils

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

    for assignment in needs_update_submission:
        # Should do the allocation
        assignment_utils.allocate(assignment)

        assignment.stage = "Discussion"
        assignment.save()

    for assignment in needs_update_discussion:
        assignment.stage = "Grading"
        assignment.save()

    for assignment in needs_update_grading:
        assignment.stage = "Closed"
        assignment.save()
