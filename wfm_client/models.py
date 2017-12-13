from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from wfm_general.models import *

# Create your models here.



class item(models.Model):
	user                   = models.ForeignKey(User,null=True,blank=True)
	item_name              = models.CharField(max_length = 50,null=True,blank=True)
	item_category          = models.CharField(max_length = 100,null=True,blank=True)
	item_num               = models.CharField(max_length = 100,null=True,blank=True)
	item_desc              = models.CharField(max_length = 150,null=True,blank=True)
	item_edited_by         = models.CharField(max_length = 150,null=True,blank=True)
	item_quantity          = models.PositiveIntegerField(default=1)
	item_created_on        = models.DateTimeField(auto_now_add = True)
	item_edited_on         = models.DateTimeField(auto_now_add = True)
	item_deleted_on        = models.DateTimeField(auto_now_add = True)
	created_by_admin_on    = models.BooleanField(default = False)
	deleted                = models.BooleanField(default=False) 
	threshold              = models.PositiveIntegerField(default=100)
	item_quantity_required = models.PositiveIntegerField(null=True,blank=True)
	item_image             = models.ImageField(upload_to='item_image/%Y-%m-%d')

	def __unicode__(self):
		return self.item_name.upper() 


class requestOrder(models.Model):
	ordernumber              = models.CharField(max_length = 12, blank=True,null=True)
	requestee                = models.ForeignKey(User, blank=True, null=True) 
	deleted                  = models.BooleanField(default = False)
	deleted_by               = models.CharField(max_length = 100, blank=True,null=True)
	status                   = models.CharField(max_length = 20,  blank=True,null=True) 
	created_on_by            = models.DateTimeField(auto_now_add = True)
	edited_on_by             = models.DateTimeField(auto_now_add = True)
	edited_by                = models.CharField(max_length = 100, blank=True,null=True)
	deleted_on_by            = models.DateTimeField(auto_now_add = True)   
	created_by_admin_on      = models.BooleanField(default = False)

	def getItemsInOrder(self):
		return self.requestitem_set.all()

	def __unicode__(self):
		return self.ordernumber


class requestItem(models.Model):
	user                     = models.ForeignKey(User)
	requestOrder             = models.ForeignKey(requestOrder, blank=True, null=True)
	name                     = models.CharField(max_length = 50, null = True, blank = True)
	category                 = models.CharField(max_length = 50, null = True, blank = True)
	number                   = models.CharField(max_length=50, null=True, blank=True)
	request_placed           = models.BooleanField(default = False)
	quantity                 = models.PositiveIntegerField(null=True,blank=True)
	deleted                  = models.BooleanField(default = False)
	deleted_by               = models.CharField(max_length = 50, blank=True,null=True)
	status                   = models.CharField(max_length = 10, blank=True,null=True) 
	created_on               = models.DateTimeField(auto_now_add = True)
	edited_on            	 = models.DateTimeField(auto_now_add = True)
	edited_by                = models.CharField(max_length = 50, blank=True,null=True)
	department               = models.CharField(max_length = 50, blank=True,null=True)
	deleted_on               = models.DateTimeField(auto_now_add = True)   
	created_by_admin         = models.BooleanField(default = False)

	def __unicode__(self):
		return self.name.upper()

	def request_item_info(self):
		return {"name":self.name,"category":self.category,"number":self.number,"quantity":self.quantity,"status":self.status}
	

class History(models.Model):
	user                    = models.ForeignKey(User,null=True,blank=True)
	created_on              = models.DateTimeField(auto_now_add=True)
	message                 = models.TextField(max_length=250,null=True,blank=True)
	history_type            = models.CharField(max_length=10,null=True,blank=True)
	history_number          = models.CharField(max_length=20,null=True,blank=True)

	def __unicode__(self):
		return unicode(self.user)

	class Meta:
		ordering = ['-created_on']
		verbose_name_plural = "History"
		
		
		





