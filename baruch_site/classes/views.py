from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from django.db import IntegrityError

from polls.forms import CorkForm, BasketForm
from polls.models import Cork, Basket, CorkBasketMembership, Choice, Vote

from classes.forms import ClassForm
from classes.models import Class, ClassEnrollment, BasketClassMembership

from polls.helper import datetimeSerializer

import json

# Put this import here because csrf token wasn't being sent back with the forms in 'new_class' and 'get_classe_edit_form'
#   Not sure how to avoid this.
from django.core.context_processors import csrf

''' Browser views '''

@login_required(login_url='polls:index')
def class_detail(request, class_id):

    tclass = get_object_or_404(Class, pk=class_id)

    context = RequestContext(request, {
        'user': request.user,
        'tclass': tclass,
    })

    return render_to_response('classes/classes_index.html', context)

@login_required(login_url='polls:index')
def edit_class(request, class_id):
    tclass = get_object_or_404(Class, pk=class_id)

    if tclass.owner.pk == request.user.pk:
        if request.method == 'POST':
            form = ClassForm(request.POST, instance = tclass)
            if form.is_valid():
                # tclass.pub_date = datetime.datetime.now()
                tclass = form.save(commit=False)
                tclass.owner = request.user
                tclass.save()


                response = json.dumps({'status': 'ok'})
                return HttpResponse(response, status=278)

            else:
                context = {
                    'class_form': form,
                    'show': True,
                    'tclass': tclass
                }
                context.update(csrf(request))

                t = get_template('classes/classes_editTabpane.html')
                return HttpResponse(t.render(Context(context)))
    
    response = json.dumps({'status': 'unauthorized'})
    return HttpResponse(response, status=401)

''' Ajax views '''

@login_required(login_url='polls:index')
def new_class(request):
    if request.method == 'POST' and request.is_ajax():
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.owner = request.user
            new_class.save()

            # may want to change this redirect
            # the redirect should be handled with ajax so
            # you can get the current page
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            context = {
                'class_form': form
            }
            context.update(csrf(request))
            t = get_template('classes/create_class_form.html')
            return HttpResponse(t.render(Context(context)))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)

@login_required(login_url='polls:index')
def delete_class(request, class_id):
    if request.method == 'POST' and request.is_ajax():

        tclass = get_object_or_404(Class, pk=class_id)
        profile_request = tclass.owner
        tclass.delete()

        return HttpResponseRedirect(reverse('accounts:profile', args=(request.user,)))
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)

@login_required(login_url='polls:index')
def get_class_edit_form(request):
    if request.method == 'POST' and request.is_ajax():

        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        if not (tclass.owner == request.user):
            return render_to_response('classes/classes_editTabpane.html', {'show': False})

        form = ClassForm(instance = tclass)
        context = {
            'class_form': form,
            'show': True,
            'tclass': tclass
        }
        context.update(csrf(request))

        return render_to_response('classes/classes_editTabpane.html', context)
    raise Http404

@login_required(login_url='polls:index')
def add_basket_to_class(request):
    if request.method == 'POST' and request.is_ajax():
        class_id = request.POST.get('class_id')
        basket_id = request.POST.get('basket_id')
        # voting = bool(request.POST.get('open_for_voting'))

        basket = get_object_or_404(Basket, pk=basket_id)
        class_to_add = get_object_or_404(Class, pk=class_id)

        try:
            BasketClassMembership.objects.create(basket=basket, tclass=class_to_add)
        except IntegrityError:
            response = json.dumps({'status': 'duplicate error'})
            return HttpResponse(response, status=400)


        response = json.dumps({'status': 'ok'})
        return HttpResponse(response)
    else:
        response = json.dumps({'status': 'unauthorized'})
        return HttpResponse(response, status=401)        


def get_baskets_for_class(request):

    if request.method == "POST" and request.is_ajax():

        class_id = int(request.POST.get('class_id'))
        page = int(request.POST.get('page'))

        tclass = get_object_or_404(Class, pk=class_id)

        if not (tclass.owner == request.user or tclass in request.user.taking.all()):
            return render_to_response('classes/classes_basketTabpane.html', {'show': False})

        # paginator = Paginator(tclass.basketclassmembership_set.all(), 10)
        paginator = Paginator(BasketClassMembership.objects.filter(tclass = tclass), 10)

        try:
            baskets = paginator.page(page)
        except PageNotAnInteger:
            baskets = paginator.page(1)
        except EmptyPage:
            baskets = paginator.page(paginator.num_pages)

        context = {
            "baskets": baskets,
            "tclass": tclass,
            "show": True,
            "user": request.user
        }

        return render_to_response('classes/classes_basketTabpane.html', context)

    raise Http404

@login_required(login_url='polls:index')
def basket_order_and_votes(request):
    if request.method == "POST" and request.is_ajax():
        class_id = int(request.POST.get('class_id'))
        page = 1

        # Basket Voting
        basket_class_id = request.POST.get('basket_class_id')
        last_basket_class_id = request.POST.get('last_basket_class_id')
        if basket_class_id:
            basket_class = get_object_or_404(BasketClassMembership, pk=basket_class_id)
            if request.user == basket_class.tclass.owner:
                basket_class.open_for_voting = not basket_class.open_for_voting
                basket_class.save()
            else:
                raise Http404
        
        if last_basket_class_id:
            last_basket_class = get_object_or_404(BasketClassMembership, pk=last_basket_class_id)
            if request.user == last_basket_class.tclass.owner:
                last_basket_class.open_for_voting = not last_basket_class.open_for_voting
                last_basket_class.save()
            else:
                raise Http404

        # Basket Ordering
        tclass = get_object_or_404(Class, pk=class_id)

        if not (tclass.owner == request.user or tclass in request.user.taking.all()):
            return render_to_response('classes/classes_basketTabpane.html', {'show': False})

        json_data = json.loads(request.POST.get('json_data'))
        deleted_items = json_data['deleted']
        sorting = json_data['sorting']

        for deleted in deleted_items:
            try:
                BasketClassMembership.objects.get(pk = deleted).delete()

            except (KeyError, BasketClassMembership.DoesNotExist):
                response = json.dumps({'status': 'fail'})
                return HttpResponse(response)

        for position in sorting:
            member = BasketClassMembership.objects.get(pk = position['basket_id'])
            member.position = int(position['position'])
            member.save()

        paginator = Paginator(tclass.basketclassmembership_set.all(), 10)

        try:
            baskets = paginator.page(page)
        except PageNotAnInteger:
            baskets = paginator.page(1)
        except EmptyPage:
            baskets = paginator.page(paginator.num_pages)

        context = {
            "baskets": baskets,
            "tclass": tclass,
            "show": True,
            "user": request.user
        }

        context.update(csrf(request))
        t = get_template('classes/classes_basketTabpane.html')
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def get_students_for_class(request):

    if request.method == "POST" and request.is_ajax():

        class_id = int(request.POST.get('class_id'))
        page = int(request.POST.get('page'))

        tclass = get_object_or_404(Class, pk=class_id)

        if not(tclass.owner == request.user):
            return render_to_response('classes/classes_studentsTabpane.html', {'show': False})

        paginator = Paginator(tclass.enrollment.all(), 10)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        context = {
            "students": students,
            "tclass": tclass,
            "show": True
        }

        return render_to_response('classes/classes_studentsTabpane.html', context)

    raise Http404

@login_required(login_url='polls:index')
def remove_student_from_class(request):
    if request.method == "POST" and request.is_ajax():

        class_id = int(request.POST.get('class_id'))
        page = int(request.POST.get('page'))
        student_id = int(request.POST.get('student_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        if not(tclass.owner == request.user):
            return render_to_response('classes/classes_studentsTabpane.html', {'show': False})

        ClassEnrollment.objects.get(tclass=tclass, student=student_id).delete()

        paginator = Paginator(tclass.enrollment.all(), 10)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        context = {
            "students": students,
            "tclass": tclass,
            "show": True
        }

        return render_to_response('classes/classes_studentsTabpane.html', context)

    raise Http404

@login_required(login_url='polls:index')
def manage_vote(request):
    if request.method == "POST" and request.is_ajax():
        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        t = get_template('classes/classes_manageVoteTabpane.html')

        if tclass.owner != request.user:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))
        
        basket_class = BasketClassMembership.objects.filter(tclass=tclass, open_for_voting=True)
        
        try:
            basket_class = basket_class[0]          # there should only be one basket open at a time
            cork_baskets = CorkBasketMembership.objects.filter(basket=basket_class.basket)
        except IndexError:
            context = {'show': True}
            return HttpResponse(t.render(Context(context)))        

        context = {
            'show': True,
            'basket_class': basket_class,
            'cork_baskets': cork_baskets
        }
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def cork_viewer(request):
    if request.method == "POST" and request.is_ajax():
        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        t = get_template('classes/classes_corkviewerTabpane.html')

        if tclass.owner != request.user:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))
        
        basket_class = BasketClassMembership.objects.filter(tclass=tclass, open_for_voting=True)

        try:
            basket_class = basket_class[0]          # there should only be one basket open at a time
        except IndexError:
            context = {'show': True}
            return HttpResponse(t.render(Context(context))) 

        if basket_class.cork_to_vote_on == None:
            context = {
                'show': True,
                'cork': False
            }
        else:
            context = {
                'show': True,
                'cork': basket_class.cork_to_vote_on.cork
            }
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def change_cork_to_vote_on(request):
    if request.method == "POST" and request.is_ajax():
        basket_class_id = int(request.POST.get('basket_class_id'))
        basket_class = get_object_or_404(BasketClassMembership, pk=basket_class_id)

        if basket_class.tclass.owner != request.user:
            response = json.dumps({'status': 'unauthorized'})
            return HttpResponse(response, status=401)

        if not basket_class.open_for_voting:
            response = json.dumps({'result': 'basket was not opened for voting'})
            return HttpResponse(response)

        reset_votes = bool(request.POST.get('reset_votes'))
        if reset_votes:
            basket_class.second_vote = False
            basket_class.cork_to_vote_on = None
            basket_class.save()
            response = json.dumps({'result': 'all corks closed for voting'})
            return HttpResponse(response)

        second_vote = bool(request.POST.get('second_vote'))
        cork_to_vote_on = int(request.POST.get('cork_to_vote_on'))

        basket_class.second_vote = second_vote
        basket_class.cork_to_vote_on = get_object_or_404(CorkBasketMembership, pk=cork_to_vote_on)
        basket_class.save()

        response = json.dumps({'status': 'ok'})
        return HttpResponse(response, status = 278)

    raise Http404

@login_required(login_url='polls:index')
def vote_on_cork(request):
    if request.method == "POST" and request.is_ajax():
        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        t = get_template('classes/classes_voteTabpane.html')

        if not (tclass.owner == request.user or tclass in request.user.taking.all()):
            context = {'show': False}
            return HttpResponse(t.render(Context(context)))

        basket_class = BasketClassMembership.objects.filter(tclass=tclass, open_for_voting=True)
        
        try:
            basket_class = basket_class[0]          # there should only be one basket open at a time
        except IndexError:
            context = {'show': True}
            return HttpResponse(t.render(Context(context)))        

        try:
            vote = Vote.objects.filter(cork_basket= basket_class.cork_to_vote_on, user=request.user, second_vote=basket_class.second_vote)
            vote = vote[0]      # get the unique vote
        except (Vote.DoesNotExist, IndexError):
            vote = None

        context = RequestContext(request, {
            'show': True,
            'basket_class': basket_class,
            'second_vote': int(basket_class.second_vote),
            'user_voted': vote
        })

        
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def submit_vote(request, cork_basket_id, second_vote):
    if request.method == "POST":
        p = get_object_or_404(CorkBasketMembership, pk=cork_basket_id)

        if second_vote == "1":
            second_vote = True
        else:
            second_vote = False

        # check if user is enrolled in this class!!

        try:
            selected_choice = p.cork.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):     
            from django.http import Http404
            return HttpResponse("You didn't select a valid choice!", status=404)
        else:

            try:
                Vote.objects.create(choice=selected_choice, cork_basket=p, user=request.user, second_vote=second_vote)
                # error in new migration
            except IntegrityError:      
                return HttpResponse("You already voted on this cork!", status=400)
            else:
                response = json.dumps({'status': 'ok'})
                return HttpResponse(response, mimetype="application/json")
    raise Http404

@login_required(login_url='polls:index')
def get_stats_for_class(request):
    if request.method == "POST" and request.is_ajax():
        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        t = get_template('classes/classes_statsTabpane.html')

        if tclass.owner != request.user:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))

        try:
            basket_classes = BasketClassMembership.objects.filter(tclass=tclass)
        except IntegrityError:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))

        open_basket_class = BasketClassMembership.objects.filter(tclass=tclass, open_for_voting=True)

        try: 
            cork_baskets = CorkBasketMembership.objects.filter(basket=open_basket_class[0].basket)
        except IndexError:
            open_basket_class = None
            cork_baskets = None

        context = {
            'show': True,
            'basket_classes': basket_classes,
            'cork_baskets': cork_baskets,
        }
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def get_stats_for_basket_in_class(request):
    if request.method == "POST" and request.is_ajax():
        basket_id = int(request.POST.get('basket_id'))
        class_id = int(request.POST.get('class_id'))
        tclass = get_object_or_404(Class, pk=class_id)

        t = get_template('classes/classes_statsAccordion.html')

        if tclass.owner != request.user:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))

        try:
            cork_baskets = CorkBasketMembership.objects.filter(basket=basket_id)
            basket_class =  BasketClassMembership.objects.filter(tclass=tclass, basket=basket_id)
        except IntegrityError:
            context = {
                'show': False
            }
            return HttpResponse(t.render(Context(context)))

        basket_class = basket_class[0]
        context = {
            'show': True,
            'cork_baskets': cork_baskets,
            'basket_class': basket_class
        }
        return HttpResponse(t.render(Context(context)))
    raise Http404

@login_required(login_url='polls:index')
def manage_enrollment(request):

    if request.method == "POST" and request.is_ajax():

        class_id = request.POST.get('class_id')
        action = request.POST.get('action')
        tclass = get_object_or_404(Class, pk=class_id)

        if action == ClassEnrollment.ACTION_ENROLL:

            try:
                ClassEnrollment.objects.create(tclass=tclass, student=request.user)
                response = {'result': 'enrolled'}
            except Exception as e:
                response = {'result': 'failed', 'reason': str(e)}

        elif action == ClassEnrollment.ACTION_DROP:

            try:
                ClassEnrollment.objects.get(tclass=tclass, student=request.user).delete()
                response = {'result': 'dropped'}
            except Exception as e:
                response = {'result': 'failed', 'reason': str(e)}

        else:

            response = {'result': 'failed', 'reason': 'unknown'}
        
        return HttpResponse(json.dumps(response), mimetype="application/json")

    raise Http404

