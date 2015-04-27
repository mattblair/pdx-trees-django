from django.conf.urls import patterns, url

from trees import views

urlpatterns = [
    
    # ex: /
    url(r'^$', views.index, name='index_url'),
    
    # ex: /list/
    #url(r'^list/$', views.tree_list, name='list_url'),
    
    # /gallery/ - show most recent photos in some kind of grid? clicking goes to tree detail
    # /gallery/<search agruments, like genus, or bbox?>/
    
    # /missing/
    url(r'^missing/$', views.missing_list, name='missing_list_url'),
    # /genus/<fragment>/
    url(r'^genus/(?P<genus_fragment>[\w-]+)/$', views.genus_search, name='genus_search_url'),

    # /year/
    url(r'^year/$', views.year_list, name='year_list_url'),
    
    # /year/<year>/
    url(r'^year/(?P<year>[\w-]+)/$', views.year_detail, name='year_detail_url'),

    # /tree/<tree_id>/
    url(r'^tree/(?P<treeid>\d+)/$', views.tree_detail, name='tree_detail_url'),
    
    # /tree/<tree_id>/submit/ -- upload photo, enter metadata with cc details
    #url(r'^tree/(?P<id>\d+)/$', views.tree_submit, name='tree_submit_url'),
    # /tree/<tree_id>/<media_id>/ 
    # does it make sense to have an url for each media item?
    #url(r'^tree/(?P<id>\d+)/$', views.tree_media, name='tree_media_url'),
    
    # legacy urls to support image delivery for v1.0 of the app:
    
]