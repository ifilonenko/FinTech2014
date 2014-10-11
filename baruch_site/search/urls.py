from django.conf.urls import patterns, url
from search import views

#Using Generic Views for pearPoll

urlpatterns = patterns('',
     url(r'^results$', views.search_results, name='search_results'),
)
