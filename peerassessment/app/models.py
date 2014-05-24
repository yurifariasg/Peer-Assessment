from django.db import models

# Place our models here

"""
    Credential class
    This class holds information to authenticate a user.
    It is used to enable authentication of a user in the system.
"""
class Credential(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

"""
    User class
    This class holds common information regarding a simple person or user.
    This class cannot be instanciated and it is used to hold common information.
"""
class User(models.Model):
    name = models.CharField(max_length=100)
    credential = models.ForeignKey('Credential')

    class Meta:
        abstract = True

"""
    AssignmentStage class
    This class holds information regarding the stage of an assignment.
"""
class AssignmentStage(models.Model):
    name = models.CharField(max_length=100)

"""
    Assignment class
    This class holds information regarding an assignment to be sent to students.
    It is used to hold grades, students and the professor who created it.
"""
class Assignment(models.Model):
    stage = models.ManyToManyField('AssignmentStage')
    owner = models.ForeignKey('Professor')
    students = models.ManyToManyField('Student')

"""
    Student class
    This class holds information of a student registered in the system.
    It is used to identify a single student in the system.
"""
class Student(User):
    assignments = models.ManyToManyField('Assignment')

"""
    Professor class
    This class holds information of a professor registered in the system.
    It is used to identify a single professor in the system.
"""
class Professor(User):
    owned_assignments = models.ManyToManyField('Assignment')
