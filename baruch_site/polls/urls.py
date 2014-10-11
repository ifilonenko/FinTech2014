from django.conf.urls import patterns, url

from polls import views

#Using Generic Views for pearPoll

urlpatterns = patterns('',
     url(r'^$', views.index_view, name='index'),
     url(r'^save_to_basket$', views.save_cork_to_basket, name='save_to_basket'),
     url(r'^basket/(?P<basket_id>\d+)$', views.basket_detail, name='basket_detail'),
     # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
     url(r'^new_cork$', views.save_cork, name='new_cork'),
     url(r'^edit_cork/(?P<cork_id>\d+)$', views.edit_cork, name='edit_cork'),
     url(r'^new_basket$', views.save_basket, name='new_basket'),
     url(r'^edit_basket_save/(?P<basket_id>\d+)$', views.basket_edit_save, name="edit_basket_save"),
     url(r'^edit_basket/(?P<basket_id>\d+)$', views.basket_edit, name="edit_basket"),
     url(r'^delete_basket/(?P<basket_id>\d+)$', views.basket_delete, name="delete_basket"),
     url(r'^delete_cork/(?P<cork_id>\d+)$', views.cork_delete, name="delete_cork"),
)
