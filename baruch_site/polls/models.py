from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItem

import datetime
import watson

class Cork(models.Model):
    owner = models.ForeignKey(User)
    question = models.TextField()
    # image = models.ImageField(upload_to="images/", default="site_images/default_cork.png")
    image = models.ImageField(upload_to="images/", blank=True)
    image_url = models.URLField(blank=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True, auto_now=False)
    update = models.DateTimeField('date updated', auto_now_add=True, auto_now=True)
    tags = TaggableManager(blank=True)
    # inPrivateClass = models.BooleanField(default=0)
    private = models.BooleanField(default=False)

    class Meta(object):
      ordering = ['-update']

    def __unicode__(self):
       return self.question
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.update <  now

    was_published_recently.admin_order_field = 'update'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Basket(models.Model):
    owner = models.ForeignKey(User)
    name = models.TextField()
    # corks are not required to create a Basket
    corks = models.ManyToManyField(Cork, through='CorkBasketMembership', related_name='corks', blank=True)
    tags = TaggableManager(blank=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True, auto_now=False)
    update = models.DateTimeField('date updated', auto_now_add=True, auto_now=True)
    # inPrivateClass = models.BooleanField(default=0)
    
    class Meta(object):
        unique_together = ('owner', 'name')
        ordering = ['-update']

    def __unicode__(self):
       return self.name 

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.update <  now

    was_published_recently.admin_order_field = 'update'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class CorkBasketMembership(models.Model):

  cork = models.ForeignKey(Cork)
  basket = models.ForeignKey(Basket)
  position = models.IntegerField(default = 0)

  def __unicode__(self):
        return self.cork.question

  class Meta(object):
        unique_together = ('cork', 'basket')
        ordering = ['position']

class Reference(models.Model):
    
    basket = models.ForeignKey(Basket)
    description = models.TextField(blank=False)
    url = models.URLField(blank=False)

    def __unicode__(self):
       return self.description 

class Choice(models.Model):

    poll = models.ForeignKey(Cork)
    choice_text = models.CharField(max_length=200)
    votes = models.ManyToManyField(User, related_name='votes', through='Vote')

    def __unicode__(self):
        return self.choice_text

class Vote(models.Model):

    choice = models.ForeignKey(Choice)
    cork_basket = models.ForeignKey(CorkBasketMembership, blank=True)     # you can vote on the same cork if it's in a different basket
    # basket_class = models.ForeignKey(BasketClassMembership, blank=True)   # you can vote on the same cork if it's in a different class
    user = models.ForeignKey(User)
    second_vote = models.BooleanField()   # you can vote twice on one cork: before and after the discussion

    def __unicode__(self):
        return '%s on %s, second vote %s, choice %s' % (self.user, self.cork_basket, self.second_vote, self.choice) 

    class Meta(object):
        unique_together = ('user', 'cork_basket', 'second_vote')


#Attempting tag_filter functionality (in admin to begin)
#Still can't resolve tag search ability. Tag filtering will, in time, create a massive
#list in the right sidebar. This won't work in the long term. 

class TaggitListFilter(SimpleListFilter):
  # Readable title which will be displayed in the
  # right admin sidebar just above the filter options.
  title = _('tags')

  # Parameter for the filter that will be used in the URL query.
  parameter_name = 'tag'
  
  def lookups(self, request, model_admin):
    list = []
    tags = TaggedItem.tags_for(model_admin.model)
    for tag in tags:
      list.append( (tag.name, _(tag.name)) )
    return list    

  def queryset(self, request, queryset):
    if self.value():
      return queryset.filter(tags__name__in=[self.value()])


watson.register(Cork, fields=("owner", "tags",))
watson.register(Basket, fields=("owner", "tags",))
watson.register(User, fields=('first_name', 'last_name', 'username', 'email'))