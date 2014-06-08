from django.db import models
import json
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Place our models here

class PAModel(models.Model):
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
    user = models.OneToOneField(User, primary_key=True) # Credential

    def clean(self):
        # Don't allow users with less than 3 characters on their name
        if len(self.user.username) < 3:
            raise ValidationError({"username": ['This field has less than 3 characters.']})
        if self.user.email == None:
            raise ValidationError({"email": ['This field cannot be blank.']})

    class Meta:
        abstract = True

class Submission(PAModel):
    """
        This class holds information regarding a student submission.
    """
    student = models.ForeignKey('Student')
    assignment = models.ForeignKey('Assignment')
    url = models.URLField(max_length=200)

    class Meta:
        unique_together = (("student","assignment"),)

class AssignmentCriteria(PAModel):
    """
        This class holds information regarding a student submission.
    """
    text = models.CharField(max_length=500)
    assignment = models.ForeignKey('Assignment')
    weight = models.FloatField()

class Message(PAModel):
    """
        This class holds information regarding student message on an assignment.
    """
    date = models.DateTimeField(auto_now = True)
    owner = models.ForeignKey('Student', related_name="received_messages")
    recipient = models.ForeignKey('Student', related_name="sent_messages")
    criteria = models.ForeignKey('AssignmentCriteria')
    assignment = models.ForeignKey('Assignment')
    text = models.CharField(max_length=500)

class Grade(PAModel):
    """
        This class holds information regarding a grade on an assignment.
    """
    grade = models.FloatField()
    assignment = models.ForeignKey('Assignment')
    owner = models.ForeignKey('Student', related_name="sent_grades")
    student = models.ForeignKey('Student', related_name="received_grades")
    criteria = models.ForeignKey('AssignmentCriteria')

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

    name = models.CharField(max_length=500)
    stage = models.CharField(max_length=10, choices=STAGES, default='Submission')

    submission_end_date = models.DateTimeField()
    discussion_end_date = models.DateTimeField()
    grading_end_date = models.DateTimeField()

    owner = models.ForeignKey('Professor')

class Allocation(PAModel):
    """
        This class holds information regarding a student's allocation in an assignment.
    """
    student = models.ForeignKey('Student')

    peer1 = models.ForeignKey('Student', related_name="+")
    peer2 = models.ForeignKey('Student', related_name="+")
    peer3 = models.ForeignKey('Student', related_name="+")
    peer4 = models.ForeignKey('Student', related_name="+")


class Student(Person):
    """
        This class holds information of a student registered in the system.
        It is used to identify a single student in the system.
    """
    assignments = models.ManyToManyField('Assignment')

    def __str__(self):
        return json.dumps({ "email" : self.user.email, "name" : self.user.username, "type" : self.getType() })

    def getType(self):
        return "student"

class Professor(Person):
    """
        This class holds information of a professor registered in the system.
        It is used to identify a single professor in the system.
    """

    def getType(self):
        return "professor"
