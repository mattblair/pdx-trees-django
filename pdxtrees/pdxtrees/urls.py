from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'pdxtrees.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # send everything else to the trees app:
    url(r'^', include('trees.urls', namespace='trees')),
    #url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^(?P<url>.*/)$', views.flatpage),
]
