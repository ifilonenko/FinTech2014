from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core import serializers
from django.db.models import Q

from polls.models import Cork, Basket, CorkBasketMembership, Reference, Choice, Vote
from polls.forms import CorkForm, BasketForm
from polls.helper import datetimeSerializer

from classes.models import Class
from classes.forms import ClassForm

from itertools import izip

import json
# import datetime
import watson

''' Browser views '''

def index_view(request):

    context = RequestContext(request, {})
    
    

    context.update({'reg_success': request.GET.get('reg_success', False)})
    context.update({'login_success': request.GET.get('login_success', None)})

    if request.user.is_authenticated():

        # look up for corks owned by the user and their
        # followings and limit the query by ten
        # todo: limit the query by a number the user chooses
        #cork = get_object_or_404(Cork, pk=cork_id)
        #private = cork.privates

        ineligible_corks = ~Q(private=True)
        user_follows = Q(owner__in=request.user.relationships.following())
        user_updates = Q(owner=request.user)
        #latest_corks = Cork.objects.filter((Q(user_updates=user_updates)| Q(user_follows=user_follows)) & ~Q(eligible_corks=True)).order_by('-update')[:10]
        latest_corks = Cork.objects.filter(user_updates|user_follows & ineligible_corks).order_by('-update')[:10]

        # get the three latest baskets (for the dropdown menu)
        all_baskets = Basket.objects.filter(owner=request.user).order_by('-update')
        latest_baskets = all_baskets[:3]

        context.update({'latest_poll_list': latest_corks})
        context.update({'latest_basket_list': latest_baskets})
        context.update({'all_baskets': all_baskets})
        context.update({'user': request.user})


    return render_to_response('polls/dashboard.html', context)


@login_required(login_url='polls:index')
def basket_detail(request, basket_id):

    basket = get_object_or_404(Basket, pk=basket_id)
    the_corks = CorkBasketMembership.objects.filter(basket=basket)
    references = Reference.objects.filter(basket=basket)

    context = RequestContext(request, {})

    context.update({'corks': the_corks})
    context.update({'user': request.user})
    context.update({'basket': basket})
    context.update({'references': references})

    return render_to_response('polls/basket_detail.html', context)

''' Ajax views '''

@login_required(login_url='polls:index')
def save_cork(request):

    if request.method == 'POST':
        form = CorkForm(request.POST, request.FILES)
        if form.is_valid():
            cork = form.save(commit=False)
            cork.owner = request.user
            cork.save()
            for choice in request.POST.getlist('choices'):
                c = Choice()
                c.poll = cork
                c.choice_text = choice
                c.save()
                
            form.save_m2m()

            return HttpResponseRedirect(reverse('polls:index'))
        else:
            context = RequestContext(request, {
                'form': form,
                'choices': request.POST.getlist('choices')
            })

            t = get_template('polls/create_cork.html')
            return HttpResponse(t.render(Context(context)))


@login_required(login_url='polls:index')
def edit_cork(request, cork_id):
    cork = get_object_or_404(Cork, pk=cork_id)
    if cork.owner.pk == request.user.pk:
        if request.method == 'POST':
            ## Not sure how to deal with image, since it resaves on each submit
            form = CorkForm(request.POST, request.FILES, instance = cork)
            if form.is_valid():
                # cork.image.delete()
                cork = form.save(commit=False)
                cork.owner = request.user
                cork.save()

                newChoices = request.POST.getlist('choices')
                oldChoices = Choice.objects.filter(poll = cork)
                choices = []
                index = 0
                
                for choice_text in newChoices:
                    try:
                        choices.append(oldChoices[index])
                        choices[index].choice_text = choice_text
                        index += 1
                        # choice.save()

                    except IndexError:
                        choices.append(Choice())
                        choices[index].poll = cork
                        choices[index].choice_text = choice_text
                        # choice.save()
                        index += 1
                
                index2 = 0
                for choice in oldChoices:
                    if index <= index2:
                        choice.delete()
                    index2 += 1

                for choice in choices:
                    choice.save()

                form.save_m2m()

                return HttpResponseRedirect(reverse('polls:index'))
            else:
                context = RequestContext(request, {
                    'form': form,
                    'choices': request.POST.getlist('choices')
                })

                t = get_template('polls/edit_cork.html')
                return HttpResponse(t.render(Context(context)))
        elif request.method == 'GET':
            form = CorkForm(instance = cork)
            choices = Choice.objects.filter(poll = cork)
            context = RequestContext(request, {
                'form': form,
                'choices': choices
            })

            t = get_template('polls/edit_cork.html')    
            return HttpResponse(t.render(Context(context)))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)


@login_required(login_url='polls:index')
def cork_delete(request, cork_id):
    try:
        cork = Cork.objects.get(pk=cork_id)
    except (KeyError, Cork.DoesNotExist):
        response = json.dumps({'status': 'fail'})
        return HttpResponse(response, status=400) # bad request status error

    if cork.owner == request.user:
        cork.delete()
        response = json.dumps({'status': 'ok'})
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)


@login_required(login_url='polls:index')
def save_basket(request):
    if request.method == 'POST':
        form = BasketForm(request.POST, request.FILES)
        if form.is_valid():
            basket = form.save(commit=False)
            basket.owner = request.user

            try: 
                basket.save()
            except IntegrityError:
                form._errors['name'] = ["this basket name already exists"]
                references = request.POST.getlist('description')
                links = request.POST.getlist('link')
                refList = izip(references, links)
                context = {
                    'basket_form': form,
                    'refList': refList
                }
                context.update(csrf(request))
                corks = form.cleaned_data.get('corks', [])
                if corks:
                    t = get_template('polls/create_basket_from_cork.html') 
                else:
                    t = get_template('polls/create_basket.html')
                return HttpResponse(t.render(Context(context)))

            # Store Basket References
            references = request.POST.getlist('description')
            links      = request.POST.getlist('link')
            for reference, url in izip(references, links):
                if not reference == '':
                    ref = Reference.objects.create(basket=basket, description=reference, url=url)
                        
            # Store Cork in Basket
            corks = form.cleaned_data.get('corks', [])
            for cork in corks:
                CorkBasketMembership.objects.create(cork=cork, basket=basket)

            # # Store Tags
            tags = form.cleaned_data['tags']
            for tag in tags:
                basket.tags.add(tag)

            response = json.dumps({'status': 'ok'})
            return HttpResponse(response, status=278)
        else:
            references = request.POST.getlist('description')
            links = request.POST.getlist('link')
            refList = izip(references, links)

            corks        = form.cleaned_data.get('corks', [])
            context = {
                'basket_form': form,
                'refList': refList
            }
            context.update(csrf(request))

            if corks:
                t = get_template('polls/create_basket_from_cork.html') 
            else:
                t = get_template('polls/create_basket.html')
            return HttpResponse(t.render(Context(context)))


@login_required(login_url='polls:index')
def basket_edit_save(request, basket_id):

    json_data = json.loads(request.POST.get('json_data'))
    deleted_items = json_data['deleted']
    sorting = json_data['sorting'] #get('sorting')

    # here

    for deleted in deleted_items:
        try:
            CorkBasketMembership.objects.get(pk = deleted).delete()
        except (KeyError, CorkBasketMembership.DoesNotExist):
            response = json.dumps({'status': 'fail'})
            return HttpResponse(response)

    for position in sorting:
        member = CorkBasketMembership.objects.get(pk = position['cork_id'])
        member.position = int(position['position'])
        member.save()

    response = json.dumps({'status': 'ok'})
    return HttpResponse(response)

@login_required(login_url='polls:index')
def basket_edit(request, basket_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    if basket.owner.pk == request.user.pk:
        if request.method == 'POST':
            form = BasketForm(request.POST, instance = basket)
            if form.is_valid():
                basket = form.save(commit=False)
                basket.owner = request.user

                try: 
                    basket.save()
                except IntegrityError:
                    form._errors['name'] = ["this basket name already exists"]
                    references = Reference.objects.filter(basket = basket)
                    context = {
                        'form': form,
                        'references': references
                    }
                    context.update(csrf(request))
                    
                    t = get_template('polls/edit_basket.html')
                    return HttpResponse(t.render(Context(context)))

                # Store Basket References
                references_pk = request.POST.getlist('reference_pk')
                references = request.POST.getlist('description')
                links      = request.POST.getlist('link')
                
                for idx, val in enumerate(references_pk):
                    ref = Reference.objects.filter(pk=val)
                    if idx >= len(references):
                        ref.delete()
                        continue

                    if references[idx] == '':
                        ref.delete()
                    else:
                        ref.update(description=references[idx], url=links[idx])

                for idx in range(len(references)):
                    if idx >= len(references_pk) and not references[idx] == '':
                        Reference.objects.create(basket=basket, description=references[idx], url=links[idx])
    
                # Store Tags
                tags = form.cleaned_data['tags']
                for tag in tags:
                    basket.tags.add(tag)

                return HttpResponseRedirect(reverse('polls:basket_detail', args=(basket_id,) ))
            else:
                references = Reference.objects.filter(basket = basket)
                context = RequestContext(request, {
                    'form': form,
                    'references': references
                })

                t = get_template('polls/edit_basket.html')
                return HttpResponse(t.render(Context(context)))
        elif request.method == 'GET':
            references = Reference.objects.filter(basket = basket)
            form = BasketForm(instance = basket)
            context = RequestContext(request, {
                'form': form,
                'references': references
            })

            t = get_template('polls/edit_basket.html')    
            return HttpResponse(t.render(Context(context)))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)



@login_required(login_url='polls:index')
def basket_delete(request, basket_id):
    try:
        basket = Basket.objects.get(pk=basket_id)
    except (KeyError, Basket.DoesNotExist):
        response = json.dumps({'status': 'fail'})
        return HttpResponse(response, status=400) # bad request status error

    if basket.owner == request.user:
        basket.delete()
        response = json.dumps({'status': 'ok'})
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)

@login_required(login_url='polls:index')
def save_cork_to_basket(request):

    cork_id = request.GET.get('cork_id')
    basket_id = request.GET.get('basket_id')

    cork = Cork.objects.get(pk=cork_id)
    basket = Basket.objects.get(pk=basket_id)
    # here
    try:
        CorkBasketMembership.objects.create(cork=cork, basket=basket)
    except IntegrityError:
        response = json.dumps({'status': 'duplicate error'})
        return HttpResponse(response)

    response = json.dumps({'status': 'ok'})
    return HttpResponse(response)
