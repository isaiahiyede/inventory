from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
from django.template.context import RequestContext
from django.db.models import Count
from django import template
from itertools import chain

import re
import hashlib
import random, datetime
import urllib
import time
import json
# import stripe

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from wfm_general.models import *
from wfm_client.models import *
from wfm_client.forms import itemForm, requestOrderForm, requestItemForm
from WFM_INV.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

# Create your views here.



def get_order_number(model):	
  ID =  str(random.randrange(11, 99)) + str(datetime.date.today())[2:].replace("-", "") + str(random.randrange(11, 99))
  if model.objects.filter(ordernumber = ID).exists():
	  ID = str(random.randrange(10, 99)) + str(datetime.date.today())[2:].replace("-", "") + str(random.randrange(11, 99))
  return  ID 





def jsondump(response_list):
	return json.dumps(list(response_list), cls=DjangoJSONEncoder)

    



def all_items_in_db():
	all_items  = item.objects.values_list('item_name', flat = True)
	return jsondump(all_items)





@login_required()
def item_processing(request,admin,template_name):
	print "i want to process a request"
	context         = {}
	rp              = request.POST
	print 'RP:', rp
	form            = requestItemForm(rp, request.FILES)
	item_name       = rp.get('name')
	item_qty        = rp.get('quantity')
	item_cat        = rp.get('category')
	item_num        = rp.get('number')
	user            = request.user
	context['form'] = requestItemForm()

	if form.is_valid():			
		itemRequest_form             = form.save(commit=False)
		itemRequest_form.user        = user
		itemRequest_form.name        = item_name
		itemRequest_form.category    = item_cat
		itemRequest_form.quantity    = item_qty
		itemRequest_form.number      = item_num
		itemRequest_form.status	 	 = "Pending"
		itemRequest_form.department  = user.useraccount.department
		print "itemRequest_form.department:",itemRequest_form.department
		itemRequest_form.created_on  = datetime.datetime.now()
		itemRequest_form.save()
		request_item               = requestItem.objects.get(pk = itemRequest_form.pk)
		context['request_item']    = request_item
		show_delete_btn            = True
		context['show_delete_btn'] = show_delete_btn
		return render(request,template_name,context)

	else:
		print form.errors
		return HttpResponse(json.dumps(form.errors), content_type='application/json')






@login_required()
def request_form(request):
	print "i want to place a request"
	context = {}
	rp      = request.POST
	print 'rp', rp
	if request.method == "POST":
		form = requestItemForm()
		template_name = 'wfm_client_snippet/item_record.html'
		return item_processing(request, False, template_name)

	else:
		print "request is a get method"
		form = OrderItemForm()
		return render(request,'wfm_client/requestPage.html',context)






@login_required()
def client_page(request):
	print "i am at the request page"
	context = {}
	items_requested = requestItem.objects.filter(user=request.user, request_placed=False, deleted=False)
	items_in_cart   = items_requested.count()
	context['items_requested'] = items_requested
	context['items_in_cart']   = items_in_cart
	all_items     			   = all_items_in_db()
	context['all_items']       = all_items
	print "all_items:",all_items
	return render(request,'wfm_client/requestPage.html',context)
	





@login_required()
def client_requestViewPage(request):
	context = {}
	request_user = request.user
	order_number = get_order_number(requestOrder)
	print "order_number:", order_number
	rp              = request.POST
	all_items       = requestItem.objects.filter(user = request_user, request_placed=False, deleted=False)
	items_in_cart   = all_items.count()
	context['items_requested'] = all_items
	context['items_in_cart']   = items_in_cart
	count_orders = all_items.count()
	created_on   = datetime.datetime.now()
	if request.method == "POST":
		request_order_form = requestOrderForm(data = request.POST)
		if request_order_form.is_valid():
			user_request_order_form               = request_order_form.save(commit = False)
			user_request_order_form.ordernumber   = order_number
			user_request_order_form.requestee     = request_user
			user_request_order_form.created_on_by = created_on
			user_request_order_form.status        = "new"
			user_request_order_form.save()
			order = requestOrder.objects.get(ordernumber = order_number)
			all_items.update(request_placed = True, requestOrder = order)
			response = redirect(reverse('client:request_order_list_view'))
			return response

		else:
			print request_order_form.errors
			print "There is an error somewhere"
			reuqest_order_form = requestOrderForm()
			return render(request,'wfm_client/requestPage.html',context)

	else:
		response = redirect(reverse('client:client_page'))
		return response

	




@login_required()
def request_order_list_view(request):
	context = {}
	print "i got here too"		
	client              = User.objects.get(email=request.user.email)
	request_orders      = requestOrder.objects.filter(requestee=client, deleted=False)
	request_order_list  = [order.ordernumber for order in request_orders]
	order_dict          = {}
	all_order_list      = []

	for order_number in request_order_list:
		order_in_view = ""
		order_list    = []
		for order in request_orders:
			if order.ordernumber == order_number:
				order_list.append(order)
		try:
			order_in_view = order_list[0]
		except:
			order_in_view = order
		order_dict[order_number]   = {'order_list':order_list, 'order':order_in_view}
	all_order_list.append(order_dict)
	
	return render(request,'wfm_client/requestViewPage.html',{'grouped_order_list': all_order_list[0]})





	
@login_required
def confirmRequest(request):
	context = {}
	print "i am at the confirmation page"
	items_requested = requestItem.objects.filter(user=request.user, request_placed=False, deleted=False)
	items_in_cart   = items_requested.count()
	context['items_requested'] = items_requested
	context['items_in_cart']   = items_in_cart
	all_items     			   = all_items_in_db()
	context['all_items']       = all_items	
	return render(request,'wfm_client/confirmRequests.html',context)






@login_required
def deleteItem(request,item_id,action):

	action_taker = request.user.username
	current_time = datetime.datetime.now()

	if action == "item":
		item_to_delete = requestItem.objects.filter(id=item_id)

		if item_to_delete.exists():
			item_to_delete.update(deleted_on=current_time, deleted=True, deleted_by=action_taker)
			# messages.info(request,"Item was sucessfully deleted")

		else:
			messages.info(request,"Item does not exist")

	elif action == "request":
		request_to_delete = requestOrder.objects.get(id=item_id)
	
		if request_to_delete.exists():
			request_to_delete.update(deleted_on_by=current_time, deleted=True, deleted_by=action_taker)
			messages.info(request,"Request was sucessfully deleted")

		else:
			messages.info(request,"Request does not exist")			

	return redirect(request.META['HTTP_REFERER'])






@login_required
def editItem(request):
	action_taker = request.user.username
	current_time = datetime.datetime.now()

	rp = request.POST
	print "rP:", rp
	qty       = rp.get('item_quantity')
	name      = rp.get('item_name')
	
	try:
		item_cat  = item.objects.get(item_name__iexact=name)
		category  = item_cat.item_category
		number    = item_cat.item_num

	except:
		
		category = 'Miscellanous'
		number   = "Msc001"

	item_id   = rp.get('item_id')	

	itemRequestToEdit              = requestItem.objects.get(id=item_id)
	itemRequestToEdit.name         = name
	itemRequestToEdit.category     = category
	itemRequestToEdit.quantity 	   = qty
	itemRequestToEdit.number       = number
	itemRequestToEdit.edited_on    = current_time
	itemRequestToEdit.edited_by    = action_taker
	itemRequestToEdit.save()
	messages.info(request,"item was successfully edited")

	return redirect(request.META['HTTP_REFERER'])






@login_required
def show_item_history(request,item_id):
	item_history  = requestItem.objects.get(id=item_id)
	if item_history.exists():
		created_on    = item_history.created_on
		edited_by     = item_history.edited_by
		edited_on     = item_history.edited_on	
		deleted_on    = item_history.deleted_on
		deleted_by    = item_history.deleted_by
		return JsonResponse({'created_on':created_on, 'edited_on':edited_on, 'edited_by':edited_by,
			'deleted_on':deleted_on, 'deleted_by':deleted_by})
	else:
		messages.info(request,'No history for this item')
		return redirect(request.META['HTTP_REFERER'])






@login_required
def getCategory(request):
	rp =  request.POST
	print 'rP:',rp
	name_of_item = rp.get('item_request_name')
	print "NAME:", name_of_item
	try:
		item_name = item.objects.get(item_name__iexact=name_of_item)
		item_category = item_name.item_category
		item_number  = item_name.item_num
	except:
		item_category = 'Miscellanous'
		item_number = 'Msc001'
	print 'Category:', item_category
	return JsonResponse({'item_category':item_category,"item_number":item_number})




