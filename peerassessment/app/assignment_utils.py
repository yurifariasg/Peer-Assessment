import models
import random
from exceptions import *
import peerassessment.settings as settings

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
    submissions = models.Submission.objects.filter(assignment = assignment)
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

        allocations.append(models.Allocation( \
            student = participants[i], \
            assignment = assignment, \
            peer1 = peer1, \
            peer2 = peer2, \
            peer3 = participants[i], \
            peer4 = peer4, \
            peer5 = peer5 ) )

    # Just in case, we delete all previous allocations on this assignment
    existing_allocations = models.Allocation.objects.filter(assignment = assignment)
    existing_allocations.delete()

    # Now we save
    for allocation in allocations:
        allocation.save()
    print "Allocation Complete..."
