from __future__ import unicode_literals

from django.db import models


class QuestionLevel(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    level = models.ForeignKey(QuestionLevel)
    order = models.PositiveIntegerField(default=0)
    question = models.TextField()
    answer = models.CharField(max_length=100)
    format = models.BooleanField(default=True, blank=False)

    def __unicode__(self):
        return self.question
