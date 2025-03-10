from django.db import models


class Topic_Selector(models.Model):
    Mode_Choices = {
        "low": "low",
        "medium": "medium",
        "high": "high",
    }
    topic = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    No_of_questions = models.IntegerField(default=0)
    mode = models.CharField(max_length=20, choices=Mode_Choices.items(), default="low")

    def __str__(self):
        return self.topic
    


class UserSignup(models.Model) :
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    history = models.FileField(upload_to='history/',blank=True, null=True)


    def __str__(self):
        return self.username




# Create your models here.
