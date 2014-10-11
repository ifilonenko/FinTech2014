from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.ForeignKey(User, unique=True)
    # add fields of Author later
    def __unicode__(self):
       return self.name 