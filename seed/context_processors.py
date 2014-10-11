from django.core.context_processors import csrf
from polls.forms import CorkForm, BasketForm
from classes.forms import ClassForm


def navbar_forms(request):
	

	context = {
		'basket_form': BasketForm(),
		'class_form': ClassForm(),
		'cork_form': CorkForm(),
	}

	return context
