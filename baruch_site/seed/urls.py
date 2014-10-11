from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seed.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', 'seed.views.home', name='home'),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^accounts/', include('users.urls', namespace='accounts')),
    url(r'^classes/', include('classes.urls', namespace='classes')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media/'}),
)
