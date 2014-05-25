from django.db import models
import json
from django.core.exceptions import ValidationError

# Place our models here

class Credential(models.Model):
    """
        This class holds information to authenticate a user.
        It is used to enable authentication of a user in the system.
    """
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def clean(self):
        # Don't allow users with less than 3 characters on their name
        if self.password == None or len(self.password) <= 3:
            raise ValidationError({"password": ['This field has less than 3 characters.']})


class User(models.Model):
    """
        This class holds common information regarding a simple person or user.
        This class cannot be instanciated and it is used to hold common information.
    """
    name = models.CharField(max_length=100)
    credential = models.ForeignKey('Credential')

    def clean(self):
        # Don't allow users with less than 3 characters on their name
        if self.name == None or len(self.name) <= 3:
            raise ValidationError({"name": ['This field has less than 3 characters.']})

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


class Student(User):
    """
        This class holds information of a student registered in the system.
        It is used to identify a single student in the system.
    """
    assignments = models.ManyToManyField('Assignment')

    def __str__(self):
        return json.dumps({ "id" : self.id, "name" : self.name })

class Professor(User):
    """
        This class holds information of a professor registered in the system.
        It is used to identify a single professor in the system.
    """
    owned_assignments = models.ManyToManyField('Assignment')
