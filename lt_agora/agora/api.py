from tastypie.resources import ModelResource
from agora.models import Decision, Vote


class DecisionResource(ModelResource):
    class Meta:
        queryset = Decision.objects.all()
        resource_name = 'decision'


class VoteResource(ModelResource):
    class Meta:
        queryset = Vote.objects.all()
        resource_name = 'vote'
