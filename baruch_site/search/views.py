from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q

from polls.forms import CorkForm, BasketForm
from polls.models import Basket, Cork


from classes.models import Class
from classes.forms import ClassForm

import watson

@login_required(login_url='polls:index')
def search_results(request):
    search_term = request.GET.get('s')
    content_type = request.GET.get('content_type')
    ignore_search = False
    
    if content_type == "cork":
        _content_type = Cork
    elif content_type == "basket":
        _content_type = Basket
    elif content_type == "user":
        _content_type = User
    elif content_type == "class":
        _content_type = Class
    else:
        ignore_search = True
        search_results = []

    if not ignore_search:
        search_results = watson.search(search_term, models=(_content_type,))

    context = RequestContext(request, {
        'search_entry_list': search_results,
        'query': search_term,
        'user': request.user,
        'content_type': content_type
    })

#Attempting to filter out content (Cork/Basket) that has been marked as private
    #context = RequestContext(request, {})

    #ineligible_corks = ~Q(private=True)
    #user_updates = Q(owner=request.user)

    #latest_baskets = Basket.objects.filter(user_updates & ineligible_corks).order_by('-pub_date')[:3]
    #context.update({'latest_basket_list': latest_baskets})

    #ineligible_corks = ~Q(private=True)
    #user_follows = Q(owner__in=request.user.relationships.following())
    #user_updates = Q(owner=request.user)

    #latest_corks = Cork.objects.filter(private=True).order_by('-update')[:3]
    #latest_baskets = Basket.objects.filter(owner=request.user).order_by('-pub_date')[:3]

    #context.update({'latest_poll_list': latest_corks})
    #context.update({'latest_basket_list': latest_baskets})

    return render_to_response('search/search_results.html', context)