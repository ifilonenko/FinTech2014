from django.contrib import admin
from polls.models import *
from users.models import *

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5

class CorkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question', 'owner', 'tags', 'image', 'private']})
        ]

    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'update', 'was_published_recently')
    list_filter = ['pub_date', TaggitListFilter]
    search_fields = ['question']

class BasketAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question', 'owner', 'tags', 'references', 'image']})
    #     ]

    list_filter = ['pub_date', TaggitListFilter]
    search_fields = ['name']

# #MODELS AND ADMIN.PY CONFLICT POSSIBLY NEED TO CHANGE ORDER TABLE ALTERING IN MYSQL
# #class tagsInline(admin.ModelAdmin): 
#     #fields = ['tag_text']

admin.site.register(Author)
admin.site.register(Reference)
admin.site.register(Cork, CorkAdmin)
admin.site.register(CorkBasketMembership)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Choice)
admin.site.register(Vote)