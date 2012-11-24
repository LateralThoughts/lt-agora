from django.contrib.auth.models import User

from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.validation import Validation
from tastypie import fields

from agora.models import Decision, Vote

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class DecisionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Decision.objects.all()
        resource_name = 'decision'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class AwesomeValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Not quite what I had in mind.'}

        errors = {}
        try:
            decision = Decision.objects.get(pk=bundle.data['decision'].split("/")[-2])
            user = User.objects.get(pk=bundle.data['user'].split("/")[-2])
            votes = Vote.objects.filter(decision=decision, user=user)
            if votes.count() != 0:
                votes.delete()
        except:
            pass
        return errors


class VoteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    decision = fields.ForeignKey(DecisionResource, 'decision')
    
    class Meta:
        queryset = Vote.objects.all()
        resource_name = 'vote'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        validation = AwesomeValidation()
