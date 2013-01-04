# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.contrib.comments.models import Comment
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
    document = models.FileField(upload_to="decision_docs", null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="offsprings")

    def is_closed(self):
        return self.closed_at <= datetime.utcnow().replace(tzinfo=utc)

    def balance(self):
        return self.votes.aggregate(balance=Sum('value')).get('balance', 0)

    def is_consensual(self):
        for vote in self.votes.all():
            if vote.value == -1:
                return False
        return True

    @models.permalink
    def get_absolute_url(self):
        return ('decision_detail', [str(self.pk)])

    def __unicode__(self):
        return "LT-%s : %s" % (self.pk, self.title)

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

# handling of decision creation to notify contact
from django.db.models.signals import post_save

def notify_contact(sender, instance, created, **kwargs):
    """Notify contact when a new decision has been created for review"""
    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    if not settings.DEBUG and settings.AGORA_SEND_MAIL:
        subject = 'A new proposal has been submitted, LT-%s' % instance.pk
        from_email = settings.AGORA_BOT_EMAIL
        to = settings.AGORA_CONTACT
        ctxt = {'obj': instance }
        html_content = render_to_string('agora/email_decision_body.html', ctxt)
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html" # Main content is now text/html
        msg.send()

post_save.connect(notify_contact, sender=Decision)

# handling of closing proposals when everyone voted
def consensus_handler(sender, instance, created, **kwargs):
    """Tries to close proposals when consensus is reached"""
    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.contrib.auth.models import User
    # everyone voted 0 or 1
    is_closed = (User.objects.count() == instance.decision.votes.exclude(value=-1).count())

    if is_closed:
        from datetime import datetime
        decision = instance.decision
        decision.closed_at = datetime.now()
        decision.save()
        if settings.AGORA_SEND_MAIL:
            subject = 'Proposal LT-%s has been accepted' % decision.pk
            from_email = settings.AGORA_BOT_EMAIL
            to = settings.AGORA_CONTACT
            ctxt = {'obj': decision }
            html_content = render_to_string('agora/email_decision_ok_body.html', ctxt)
            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = "html" # Main content is now text/html
            msg.send()

post_save.connect(consensus_handler, sender=Vote)

# handling of notification of new comments
def notify_comment(sender, instance, created, **kwargs):
    """Tries to close proposals when consensus is reached"""
    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string

    if isinstance(instance.content_object, Decision) and settings.AGORA_SEND_MAIL:
        decision = instance.content_object
        subject = 'New comment on LT-%s has been accepted' % decision.pk
        from_email = settings.AGORA_BOT_EMAIL
        to = settings.AGORA_CONTACT
        ctxt = {'obj': instance }
        html_content = render_to_string('agora/email_decision_comment_body.html', ctxt)
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html" # Main content is now text/html
        msg.send()

post_save.connect(notify_comment, sender=Comment)

def notify_last_missing(sender, instance, created, **kwargs):
    """Notify last person who did not vote"""
    from django.contrib.auth.models import User
    from django.conf import settings
    last_users = User.objects.exclude(pk__in=[vote["user"] for vote in instance.decision.votes.values("user")])
    if last_users.count() == 1 and settings.AGORA_SEND_MAIL:
        retardataire = last_users[0]
        subject = "Votre avis est requis pour LT-%s" % (instance.decision.pk)
        text = u"Tout le monde a voté sauf vous. Veuillez vous rendre à l'adresse http://%s%s" % (settings.AGORA_SITE_URL, instance.decision.get_absolute_url())
        retardataire.email_user(subject, text)

post_save.connect(notify_last_missing, sender=Vote)
