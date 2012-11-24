from django.db import models
from django.contrib.auth.models import User


class Decision(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    user = models.ForeignKey(User, related_name="decisions")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)


class Vote(models.Model):
    DECISION_VOTE_CHOICES = (
        ('1', 'Sustained'),
        ('0', 'Ignored'),
        ('-1', 'Revoked'),
    )

    decision = models.ForeignKey(Decision, related_name="votes")
    user = models.ForeignKey(User, related_name="votes")
    value = models.IntegerField(choices=DECISION_VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
