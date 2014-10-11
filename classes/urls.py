from django.conf.urls import patterns, url
from classes import views

#Using Generic Views for pearPoll

urlpatterns = patterns('',
    url(r'^class/(?P<class_id>\d+)$', views.class_detail, name='class_detail'),
    url(r'^class/class_edit/(?P<class_id>\d+)$', views.edit_class, name='edit_class'),
    url(r'^class/vote/(?P<cork_basket_id>\d+)/(?P<second_vote>\d)$', views.submit_vote, name='submit_vote'),
    
    url(r'^ajax/new_class$', views.new_class, name='new_class'),
    url(r'^ajax/class_delete/(?P<class_id>\d+)$', views.delete_class, name='delete_class'),
    url(r'^ajax/class_form$', views.get_class_edit_form, name='get_class_edit_form'),
    url(r'^ajax/get/baskets$', views.get_baskets_for_class, name='get_baskets_for_class'),
    url(r'^ajax/get/students$', views.get_students_for_class, name='get_students_for_class'),
    url(r'^ajax/get/stats$', views.get_stats_for_class, name='get_stats_for_class'),
    url(r'^ajax/get/stats/basket$', views.get_stats_for_basket_in_class, name='get_stats_for_basket_in_class'),
    url(r'^ajax/remove/student$', views.remove_student_from_class, name='remove_student_from_class'),
    url(r'^ajax/manage_enrollment$', views.manage_enrollment, name='manage_enrollment'),
    url(r'^ajax/add_basket_to_class$', views.add_basket_to_class, name='add_basket_to_class'),
    url(r'^ajax/basket_order_votes$', views.basket_order_and_votes, name='basket_order_and_votes'),
    url(r'^ajax/manage_voting$', views.manage_vote, name='manage_vote'),
    url(r'^ajax/cork_viewing$', views.cork_viewer, name='cork_viewer'),
    url(r'^ajax/change_cork_to_vote_on$', views.change_cork_to_vote_on, name='change_cork_to_vote_on'),
    url(r'^ajax/vote$', views.vote_on_cork, name='vote_on_cork')
)
