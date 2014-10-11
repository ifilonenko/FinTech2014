from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q
from django.shortcuts import get_list_or_404

from polls.models import Basket, Cork 

from users.forms import RegistrationForm, SettingsForm

import json

''' Browser views '''

def user_registration(request):

    form = RegistrationForm()

    context = RequestContext(request, {
        'form': form,
        'user': request.user
        })


    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.set_password(form.cleaned_data["password"])
            model_instance.save()

            return HttpResponseRedirect(reverse('polls:index')+'?reg_success=true')
        else:
            context.update({'form': form})

    return render_to_response('users/user_registration.html', context)

def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index')+'?login_success=true')
        else:
            # if we ever create a view to inform a user
            # that their account has been deactivate
            # this is the place to redirect to that page
            return HttpResponseRedirect(reverse('polls:index')+'?login_success=false')
    
    return HttpResponseRedirect(reverse('polls:index')+'?login_success=false')

@login_required(login_url='polls:index')
def user_settings(request):

    final_form = SettingsForm(instance=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            model_instance = form.save(commit=False)
            if form.cleaned_data["password"]:
                model_instance.set_password(form.cleaned_data["password"])
            model_instance.save()
            return HttpResponseRedirect(reverse('accounts:settings'))
        else:
            final_form = form


    context = RequestContext(request, {
        'user': request.user,
        'user_form': final_form,
    })

    return render_to_response('users/user_settings.html', context)

@login_required(login_url='polls:index')
def user_profile(request, username):

    profile_request = get_object_or_404(User, username = username)

    context = RequestContext(request, {
        'user': request.user,
        'user_profile': profile_request,
    })
    
    return render_to_response('users/user_profile.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

''' Ajax views '''

@login_required(login_url='polls:index')
def user_corks(request, username):
    if request.method == 'POST':

            profile_request = get_object_or_404(User, username = username)
            all_baskets = Basket.objects.filter(owner=request.user).order_by('-pub_date')
            latest_baskets = all_baskets[:3]

            context = RequestContext(request, {
                'user': request.user,
                'user_profile': profile_request,
            })
            context.update({'latest_basket_list': latest_baskets})
            context.update({'all_baskets': all_baskets})

            t = get_template('users/cork_tabPane.html')
            return HttpResponse(t.render(Context(context)))
    

@login_required(login_url='polls:index')
def user_baskets(request, username):
    if request.method == 'POST':

        profile_request = get_object_or_404(User, username = username)

        context = RequestContext(request, {
            'user': request.user,
            'user_profile': profile_request,
        })

        t = get_template('users/basket_tabPane.html')
        return HttpResponse(t.render(Context(context)))


@login_required(login_url='polls:index')
def user_classes(request, username, relationship):
    if request.method == 'POST' and request.is_ajax():

        page = request.POST.get('page')
        profile = get_object_or_404(User, username = username)
        try:
            paginator = Paginator(getattr(profile, relationship).all(), 10)
        except AttributeError:
            response = {'result': 'invalid request'}
            return HttpResponse(json.dumps(response), status = 400)

        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            classes = paginator.page(paginator.num_pages)

        context = {
            "classes": classes,
            "user": profile,
            "relationship": relationship
        }

        return render_to_response('users/classes_tabPane.html', context)


@login_required(login_url='polls:index')
def user_relationships(request, username, relationship):
    if request.method == 'POST' and request.is_ajax():

        page = request.POST.get('page')
        profile = get_object_or_404(User, username = username)
        try:
            paginator = Paginator(getattr(profile.relationships, relationship)(), 10)
        except AttributeError:
            response = {'result': 'invalid request'}
            return HttpResponse(json.dumps(response), status = 400)

        try:
            classes = paginator.page(page)
        except PageNotAnInteger:
            classes = paginator.page(1)
        except EmptyPage:
            classes = paginator.page(paginator.num_pages)

        context = {
            "users": classes,
            "user": profile,
            "relationship": relationship
        }

        return render_to_response('users/user_relationships_tabPane.html', context)

@login_required(login_url='polls:index')
def user_follow(request, username):

    if request.is_ajax():
        user_to_follow = get_object_or_404(User, username = username)
        request.user.relationships.add(user_to_follow)
        response = {'result': 'followed'}
        return HttpResponse(json.dumps(response), mimetype="application/json")

    raise Http404

@login_required(login_url='polls:index')
def user_unfollow(request, username):

    if request.is_ajax():
        user_to_unfollow = get_object_or_404(User, username = username)
        rel = request.user.relationships.remove(user_to_unfollow)
        response = {'result': 'unfollowed'}
        return HttpResponse(json.dumps(response), mimetype="application/json")

    raise Http404
