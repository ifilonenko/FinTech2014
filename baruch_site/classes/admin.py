from django.contrib import admin
from classes.models import *

admin.site.register(Class)
admin.site.register(BasketClassMembership)
admin.site.register(ClassEnrollment)