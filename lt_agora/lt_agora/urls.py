from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

from tastypie.api import Api
from agora.api import DecisionResource, VoteResource, UserResource
from agora.models import Decision
from agora.forms import DecisionForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^accounts/', include('accounts.urls')),
)

# website views
from agora.views import index
urlpatterns += patterns('agora.views',
    url(r'^$', login_required(index), name='home'),
    url(r'^about/?$', 'about', name='about'),
    url(r'^logout/?$', 'index', name='logout'),
)

# generic views
decision_info_dict = {
    'queryset': Decision.objects.all(),
}
author_info_dict = {
    'queryset': User.objects.all(),
}
decision_cinfo_dict = {
  'form_class': DecisionForm,
  'login_required': True,
}

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object
urlpatterns += patterns('',
    url(r'^decision/all/?$',
        login_required(object_list),
        decision_info_dict,
        name="decision_list"),
    url(r'^decision/create/?$',
        login_required(create_object),
        decision_cinfo_dict,
        name="decision_create"),
    url(r'^decision/(?P<object_id>\d+)/$',
        login_required(object_detail),
        decision_info_dict,
        name="decision_detail"),
    # author part :
    url(r'^author/(?P<object_id>\d+)/$',
        login_required(object_detail),
        author_info_dict,
        name="author_detail"),
)

# api views
v1_api = Api(api_name='v1')
v1_api.register(DecisionResource())
v1_api.register(VoteResource())
v1_api.register(UserResource())

urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
