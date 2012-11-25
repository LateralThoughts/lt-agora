from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
                       url(r'^login/$', 
                        'django.contrib.auth.views.login', 
                        {'template_name': 'accounts/login.html'}, name="auth_login"),

                       url(r'^logout/$', 
                        'django.contrib.auth.views.logout', 
                        {'template_name': 'accounts/logout.html'}, name="auth_logout"),
)
