from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from tastypie.api import Api
from agora.api import DecisionResource, VoteResource
from agora.models import Decision

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)

# website views
urlpatterns += patterns('agora.views',
    url(r'^$', 'index', name='home'),
    url(r'^about/?$', 'index', name='about'),
    url(r'^contact/?$', 'index', name='contact'),
    url(r'^logout/?$', 'index', name='logout'),
)

# generic views 
info_dict = {
    'queryset': Decision.objects.all(),
}

urlpatterns += patterns('',
    url(r'^decision/all/?$', 'django.views.generic.list_detail.object_list', info_dict),
    url(r'^decision/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
)

# api views
v1_api = Api(api_name='v1')
v1_api.register(DecisionResource())
v1_api.register(VoteResource())

urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
