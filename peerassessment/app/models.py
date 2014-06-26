from django.db import models as dbmodels
import json
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import assignment_utils

# Place our models here

class PAModel(dbmodels.Model):
    """
        This class holds common information to all models in the system.
    """
    def try_delete():
        try:
            self.delete()
        except:
            pass

    class Meta:
        abstract = True

class Person(PAModel):
    """
        This class holds common information regarding a simple person.
        It cannot be instanciated and is used to hold common information.
    """
    user = dbmodels.OneToOneField(User, primary_key=True) # Credential

    def clean(self):
        # Don't allow users with less than 3 characters on their name
        if len(self.user.username) < 3:
            raise ValidationError({"username": ['This field has less than 3 characters.']})
        if self.user.email == None:
            raise ValidationError({"email": ['This field cannot be blank.']})

    class Meta:
        abstract = True

class AssignmentCriteria(PAModel):
    """
        This class holds information regarding a student submission.
    """
    text = dbmodels.CharField(max_length=500)
    assignment = dbmodels.ForeignKey('Assignment')
    weight = dbmodels.FloatField()

class Message(PAModel):
    """
        This class holds information regarding student message on an assignment.
    """
    date = dbmodels.DateTimeField(auto_now = True)
    owner = dbmodels.ForeignKey('Student', related_name="received_messages")
    recipient = dbmodels.ForeignKey('Student', related_name="sent_messages")
    criteria = dbmodels.ForeignKey('AssignmentCriteria')
    text = dbmodels.CharField(max_length=500)

class Grade(PAModel):
    """
        This class holds information regarding a grade on an assignment.
    """
    grade = dbmodels.FloatField( \
        validators = [MinValueValidator(0.0), MaxValueValidator(10.0)])
    assignment = dbmodels.ForeignKey('Assignment')
    owner = dbmodels.ForeignKey('Student', related_name="sent_grades")
    student = dbmodels.ForeignKey('Student', related_name="received_grades")
    criteria = dbmodels.ForeignKey('AssignmentCriteria')

class Allocation(PAModel):
    """
        This class holds information regarding a student's allocation in an assignment.
    """
    student = dbmodels.ForeignKey('Student')
    assignment = dbmodels.ForeignKey('Assignment')

    peer1 = dbmodels.ForeignKey('Student', related_name="+")
    peer2 = dbmodels.ForeignKey('Student', related_name="+")
    peer3 = dbmodels.ForeignKey('Student', related_name="+")
    peer4 = dbmodels.ForeignKey('Student', related_name="+")
    peer5 = dbmodels.ForeignKey('Student', related_name="+")

    class Meta:
        unique_together = (("student","assignment"),)

class Assignment(PAModel):
    """
        This class holds information regarding an assignment to be sent to students.
        It is used to hold grades, students and the professor who created it.
    """
    STAGES = (
        ('Submission', 'Submission'),
        ('Discussion', 'Discussion'),
        ('Grading', 'Grading'),
        ('Closed', 'Closed'),
    )

    name = dbmodels.CharField(max_length=500)
    stage = dbmodels.CharField(max_length=10, choices=STAGES, default='Submission')

    submission_end_date = dbmodels.DateTimeField()
    discussion_end_date = dbmodels.DateTimeField()
    grading_end_date = dbmodels.DateTimeField()

    owner = dbmodels.ForeignKey('Professor')

    def update_stage(self):
        current_date = timezone.now()
        new_stage = None
        if current_date > self.submission_end_date:
            if current_date > self.discussion_end_date:
                if current_date > self.grading_end_date:
                    new_stage = "Closed"
                else:
                    new_stage = "Grading"
            else:
                new_stage = "Discussion"
        else:
            new_stage = "Submission"

        if new_stage != "Submission" and not self.has_allocations():
            assignment_utils.allocate(self)

        self.stage = new_stage

    def has_allocations(self):
        allocations = Allocation.objects.filter(assignment = self)
        return len(allocations) > 0


class Submission(PAModel):
    """
        This class holds information regarding a student submission.
    """
    student = dbmodels.ForeignKey('Student')
    assignment = dbmodels.ForeignKey('Assignment')
    url = dbmodels.URLField(max_length=200)

    class Meta:
        unique_together = (("student","assignment"),)

class Student(Person):
    """
        This class holds information of a student registered in the system.
        It is used to identify a single student in the system.
    """
    assignments = dbmodels.ManyToManyField('Assignment')

    def __str__(self):
        return json.dumps({ "email" : self.user.email, "name" : self.user.username, "type" : self.getType() })

    def id(self):
        return self.user.id

    def getType(self):
        return "student"

class Professor(Person):
    """
        This class holds information of a professor registered in the system.
        It is used to identify a single professor in the system.
    """

    def getType(self):
        return "professor"
