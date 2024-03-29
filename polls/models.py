import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    done_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def create(cls,question_text,done_by,pub_date):
        question=cls(question_text=question_text,done_by=done_by,pub_date=pub_date)
        return  question

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
