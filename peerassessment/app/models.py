from django.db import models

# Place our models here

class Credential(models.Model):
    """
        This class holds information to authenticate a user.
        It is used to enable authentication of a user in the system.
    """
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class User(models.Model):
    """
        This class holds common information regarding a simple person or user.
        This class cannot be instanciated and it is used to hold common information.
    """
    name = models.CharField(max_length=100)
    credential = models.ForeignKey('Credential')

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


class Professor(User):
    """
        This class holds information of a professor registered in the system.
        It is used to identify a single professor in the system.
    """
    owned_assignments = models.ManyToManyField('Assignment')
