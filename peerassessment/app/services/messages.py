from common import *

def is_peer(student, allocation):
    """
        Checks if the student is in the given allocation.
    """
    if student == allocation.peer1 or\
        student == allocation.peer2 or\
        student == allocation.peer3 or\
        student == allocation.peer4 or\
        student == allocation.peer5:
        return True
    return False

def validate_message_sender(sender, target_submission):
    """
        Checks if the sender is allowed to send a message to the given submission.
    """

    # Check if he is owner
    is_owner = sender == target_submission.student
    if is_owner:
        return True

    # Check if submission owner is sender's peer
    allocation = Allocation.objects.filter(\
        assignment = target_submission.assignment,\
        student = sender).first()

    # We could make this one-line but let's leave this way to make it more readable
    if allocation != None and is_peer(target_submission.student, allocation):
        return True
    return False

def validate_criteria(criteria, target_submission):
    """
        Validates the given criteria regarding the submission it will be placed.
    """
    if criteria.assignment != target_submission.assignment:
        raise ValidationError({"criteria" : ["Criteria not from assignment."]})

def submit_message_to(message, submission, criteria, sender, related_peer):
    """
        Submits 'message' from 'sender' on the 'criteria' of the given 'submission'.
        This function performs only model validation.
        The related peer is used to identify the conversation messages, which
        will be from/to related_peer <-> submission_owner
        related_peer is expected to be an optional int from 1-5 to specify
        the peer. If not specified the sender will be the related_peer.
    """
    related_peer_model = sender
    if related_peer:
        # Check who is the submission owner
        if submission.owner == request.user.student:
            # If he is the owner of the submission, the related_peer
            # is his peer
            allocation = Allocation.objects.filter(\
                assignment = submission.assignment,\
                student = sender).first()
            related_peer_model = get_peer(allocation, related_peer)
        else:
            # If he is not the submission owner, then he is the related_peer
            pass

    message = Message( \
        owner = sender, \
        submission = submission, \
        criteria = criteria, \
        text = message,\
        related_peer = related_peer_model)

    # Model Validation
    message.full_clean()
    message.save()

def get_messages_for(submission, criteria, related_peer):
    """
        Gets all messages of a given submission, criteria and related_peer.
    """
    messages = Message.objects.filter(\
        submission = submission, criteria = criteria, \
        related_peer = related_peer).order_by('date').all()
    return messages
