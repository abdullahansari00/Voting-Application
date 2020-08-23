from django.db import models

# Create your models here.

class Question(models.Model):
	username = models.CharField(max_length=20)
	question = models.TextField()
	option = models.TextField()
	count = models.IntegerField()

class Vote(models.Model):
	voter = models.CharField(max_length=20)
	username = models.CharField(max_length=20)
	question = models.TextField()
	option = models.TextField()