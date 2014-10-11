from django.db import models
from django.contrib.auth.models import User
from polls.models import Basket, CorkBasketMembership
from taggit.managers import TaggableManager
from exceptions import ClassNotActive, TakingOwnClass
import watson
import datetime

class Class(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    private = models.BooleanField()     # hide corks/baskets from public pages
    active = models.BooleanField()      # whether the class is viewable/open for enrollment
    pub_date = models.DateTimeField('date published',auto_now_add=True, auto_now=False)
    update = models.DateTimeField('date updated', auto_now_add=True, auto_now=True)

    tags = TaggableManager(blank=True)
    baskets = models.ManyToManyField(Basket, through='BasketClassMembership', related_name='baskets')
    
    enrollment = models.ManyToManyField(User, through='ClassEnrollment', related_name='taking')
    owner = models.ForeignKey(User, verbose_name=u'Professor', related_name='teaching')

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = "Class"
        verbose_name_plural = "Classes"


class BasketClassMembership(models.Model):

    basket = models.ForeignKey(Basket)
    tclass = models.ForeignKey(Class, verbose_name='class')
    position = models.IntegerField(default = 0)
    open_for_voting = models.BooleanField(default=False)
    cork_to_vote_on = models.ForeignKey(CorkBasketMembership, blank=True, null=True, default=None)   # The cork_basket that is currently being voted
    second_vote = models.BooleanField(default=0)                            # Is this the second vote?

    def __unicode__(self):
        return "%s in %s" % (self.basket.name, self.tclass.name)

    class Meta(object):
        ordering = ['position']
        unique_together = ('basket', 'tclass')
        verbose_name = "Basket/Class relationship"
        verbose_name_plural = "Basket/Class relationship"

class ClassEnrollment(models.Model):

    tclass = models.ForeignKey(Class, verbose_name='class')
    student = models.ForeignKey(User)

    ACTION_DROP = 'drop'
    ACTION_ENROLL = 'enroll'

    def __unicode__(self):
        return "<Enrollment: \"%s\", %s>" % (self.student.last_name + ", " + self.student.first_name, self.tclass.name)

    def save(self, *args, **kwargs):
        if not self.tclass.active:
            raise ClassNotActive(self.tclass.name)
        elif self.tclass.owner == self.student:
            raise TakingOwnClass(self.tclass.name)

        return super(ClassEnrollment, self).save()
        
    class Meta:
        unique_together = ('student', 'tclass')
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollment"

watson.register(Class, fields=("name", "description", "tags", "owner"))