from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
                       url(r'^login/$', 
                        'social_auth.views.auth', 
                        {'backend': 'google-oauth2'}, name="auth_login"),

                       url(r'^logout/$', 
                        'django.contrib.auth.views.logout', 
                        {'template_name': 'accounts/logout.html'}, name="auth_logout"),
)
