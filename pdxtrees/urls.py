from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'pdxtrees.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/$', 'trees.views.public_logout', name='logout_url'),
    
    # send everything else to the trees app:
    url(r'^', include('trees.urls', namespace='trees')),
    #url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^(?P<url>.*/)$', views.flatpage),
]
