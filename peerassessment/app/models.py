from django.db import models

# Place our models here

class Credential(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class User(models.Model):
    name = models.CharField(max_length=100)
    credential = models.ForeignKey('Credential')

    class Meta:
        abstract = True

class AssignmentStage(models.Model):
    name = models.CharField(max_length=100)

class Assignment(models.Model):
    stage = models.ManyToManyField('AssignmentStage')
    owner = models.ForeignKey('Professor')
    students = models.ManyToManyField('Student')

class Student(User):
    assignments = models.ManyToManyField('Assignment')

class Professor(User):
    owned_assignments = models.ManyToManyField('Assignment')
