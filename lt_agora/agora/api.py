from django.contrib.auth.models import User

from tastypie.authentication import Authentication, BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import Validation
from tastypie import fields

from agora.models import Decision, Vote

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = Authentication()
        authorization = Authorization()


class DecisionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Decision.objects.all()
        resource_name = 'decision'
        authentication = Authentication()
        authorization = Authorization()


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
    user = fields.ForeignKey(UserResource, 'user', full=True)
    decision = fields.ForeignKey(DecisionResource, 'decision', full=True)
    
    class Meta:
        queryset = Vote.objects.all()
        resource_name = 'vote'
        authentication = Authentication()
        authorization = Authorization()
        validation = AwesomeValidation()
        filtering = {
            'decision': ALL,
            'user': ALL_WITH_RELATIONS,
        }

