from django.conf.urls import patterns, url

from users import views

#Using Generic Views for pearPoll

urlpatterns = patterns('',
     url(r'^registration/$', views.user_registration, name='registration'),
     url(r'^login/$', views.user_login, name='login'),
     url(r'^logout/$', views.user_logout, name='logout'),
     url(r'^profile/(?P<username>\w+)/$', views.user_profile, name='profile'),
     url(r'^settings/$', views.user_settings, name='settings'),
     
     url(r'^ajax/follow/(?P<username>\w+)/$', views.user_follow, name='user_follow'),
     url(r'^ajax/unfollow/(?P<username>\w+)/$', views.user_unfollow, name='user_unfollow'),
     url(r'^ajax/user_corks/(?P<username>\w+)/$', views.user_corks, name='user_corks'),
     url(r'^ajax/user_baskets/(?P<username>\w+)/$', views.user_baskets, name='user_baskets'),
     url(r'^ajax/user_classes/(?P<username>\w+)/(?P<relationship>\w+)/$', views.user_classes, name='user_classes'),
     url(r'^ajax/user_relationships/(?P<username>\w+)/(?P<relationship>\w+)/$', views.user_relationships, name='user_relationships'), 
)
