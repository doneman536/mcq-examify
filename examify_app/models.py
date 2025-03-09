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


# Create your models here.
