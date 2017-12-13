from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserAccount(models.Model):
    # all user fields
    password2                =    models.CharField(max_length=50, blank=True, null=True)
    user                     =    models.OneToOneField(User)
    phone_number             =    models.CharField(max_length = 15, null = True, blank = True)
    title                    =    models.CharField(max_length=50, null=True)
    department				 =    models.CharField(max_length = 15, null = True, blank = True)
    # shipping_address       =    models.CharField(max_length=500, null=True)
    created_on               =    models.DateTimeField(auto_now_add = True)
    edited_on            	 =    models.DateTimeField(auto_now_add = True)
    deleted_on               =    models.DateTimeField(auto_now_add = True)   
    created_by_admin         =    models.BooleanField(default = False)
    changed_password         =    models.BooleanField(default = False)
    profile_up_to_date       =    models.BooleanField(default = False)    
   
    def __unicode__(self):
        return '%s %s' %(self.user.first_name.upper(), self.user.last_name.upper())
