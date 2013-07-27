from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

from tastypie.api import Api
from agora.api import DecisionResource, VoteResource, UserResource
from agora.views import *

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

urlpatterns += patterns('',
    url(r'^decision/all/?$',
        login_required(DecisionListView.as_view()),
        name="decision_list"),
    url(r'^decision/create/?$',
        login_required(DecisionCreateView.as_view()),
        name="decision_create"),
    url(r'^decision/(?P<pk>\d+)/$',
        login_required(DecisionDetailView.as_view()),
        name="decision_detail"),
    # author part :
    url(r'^author/(?P<pk>\d+)/$',
        login_required(AuthorDetailView.as_view()),
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
