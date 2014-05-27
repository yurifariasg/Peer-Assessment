from django.db import models
import json
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Place our models here

class Person(models.Model):
    """
        This class holds common information regarding a simple person.
        This class cannot be instanciated and it is used to hold common information.
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


class AssignmentStage(models.Model):
    """
        This class holds information regarding the stage of an assignment.
    """
    name = models.CharField(max_length=100)


class Assignment(models.Model):
    """
        This class holds information regarding an assignment to be sent to students.
        It is used to hold grades, students and the professor who created it.
    """
    stage = models.ManyToManyField('AssignmentStage')
    owner = models.ForeignKey('Professor')
    students = models.ManyToManyField('Student')


class Student(Person):
    """
        This class holds information of a student registered in the system.
        It is used to identify a single student in the system.
    """
    assignments = models.ManyToManyField('Assignment')

    def __str__(self):
        return json.dumps({ "email" : self.user.email, "name" : self.user.username })

class Professor(Person):
    """
        This class holds information of a professor registered in the system.
        It is used to identify a single professor in the system.
    """
    owned_assignments = models.ManyToManyField('Assignment')
