from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.timezone import utc
from datetime import datetime, timedelta

def default_closed_date():
    return datetime.now() + timedelta(days=7)

class Decision(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    user = models.ForeignKey(User, related_name="decisions")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True, default=default_closed_date)

    def is_closed(self):
        return self.closed_at <= datetime.utcnow().replace(tzinfo=utc)

    def balance(self):
        return self.votes.aggregate(balance=Sum('value')).get('balance', 0)

    @models.permalink
    def get_absolute_url(self):
        return ('decision_detail', [str(self.pk)])

    class Meta:
        ordering = ['-closed_at', 'created_at']


class Vote(models.Model):
    DECISION_VOTE_CHOICES = (
        (1, 'Sustained'),
        (0, 'Ignored'),
        (-1, 'Revoked'),
    )

    decision = models.ForeignKey(Decision, related_name="votes")
    user = models.ForeignKey(User, related_name="votes")
    value = models.IntegerField(choices=DECISION_VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
