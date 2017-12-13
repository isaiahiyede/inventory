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
from django.db.models import Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from django.utils import timezone
from django.forms.models import model_to_dict


from itertools import chain

import re
import hashlib
import random, datetime
import urllib
import time
import string
import json

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from wfm_general.models import *
from wfm_client.forms import itemForm
from wfm_client.models import *

# Create your views here.


def getCatPrefix(word):
	new_time = (re.sub('[:,-.]',',',str(datetime.datetime.now()))).replace(" ",",").split(',')[5:]
	current_time = "".join(new_time)	
	return word[0].upper() + word[1].upper() + word[-1].upper() + str(random.randrange(0, 9)) + current_time + str(random.randrange(0, 9))


def all_same(items):
	return all(x==items[0] for x in items)


@login_required
def admindashboard(request):
	# print request.session.keys()
	context = {}
	if 'search_with_all' in request.session:
		# print "search all"
		all_orders = requestOrder.objects.filter(
				(Q(requestee__email__iexact=request.session['request_item']) |
				Q(ordernumber__iexact=request.session['request_item']) | 
				Q(requestee__first_name__icontains=request.session['request_item']) |
				Q(requestee__last_name__icontains=request.session['request_item'])) &
				Q(created_on_by__range=[request.session['startdate'], request.session['enddate']]),
				deleted=False
				)

		# print "all_orders:",all_orders

		del request.session['request_item']
		del request.session['search_with_all']
		del request.session['startdate']
		del request.session['enddate']

	elif 'search_with_request_item' in request.session:
		# print "search item"
		all_orders = requestOrder.objects.filter(
			(Q(requestee__email__iexact=request.session['request_item']) |
			Q(ordernumber__iexact=request.session['request_item'])|
			Q(requestee__first_name__icontains=request.session['request_item']) |
			Q(requestee__last_name__icontains=request.session['request_item'])),
			deleted=False
			)

		# print "all_orders:",all_orders

		del request.session['request_item']
		del request.session['search_with_request_item']


	elif 'search_with_request_item_start' in request.session:
		# print "search item and startdate"
		first_startdate = str(request.session['startdate'])
		startdate = first_startdate.split('-')
		# print "startdate:",startdate
		all_orders = requestOrder.objects.filter(

				(Q(requestee__email__iexact=request.session['request_item']) |
				Q(ordernumber__iexact=request.session['request_item']) | 
				Q(requestee__first_name__icontains=request.session['request_item']) |
				Q(requestee__last_name__icontains=request.session['request_item'])),

				deleted=False,
				created_on_by__year=startdate[0],
				created_on_by__month=startdate[1],
				created_on_by__day=startdate[2]
				)

		# print "all_orders:",all_orders

		del request.session['request_item']
		del request.session['startdate']
		del request.session['search_with_request_item_start']


	elif 'search_with_request_item_end' in request.session:
		# print "item and enddate"
		first_enddate = str(request.session['enddate'])
		enddate = first_enddate.split('-')
		# print "enddate:",enddate
		all_orders = requestOrder.objects.filter(

				(Q(requestee__email__iexact=request.session['request_item']) |
				Q(ordernumber__iexact=request.session['request_item']) | 
				Q(requestee__first_name__icontains=request.session['request_item']) |
				Q(requestee__last_name__icontains=request.session['request_item'])),

				deleted=False,
				created_on_by__year=enddate[0],
				created_on_by__month=enddate[1],
				created_on_by__day=enddate[2]
				)

		# print "all_orders:",all_orders

		del request.session['request_item']
		del request.session['enddate']
		del request.session['search_with_request_item_end']


	elif 'search_with_start' in request.session:
		# print "startdate:",request.session['startdate']
		first_startdate = str(request.session['startdate'])
		startdate = first_startdate.split('-')
		# print "startdate:",startdate
		all_orders = requestOrder.objects.filter(
			created_on_by__year=startdate[0],
			created_on_by__month=startdate[1],
			created_on_by__day=startdate[2], 
			deleted=False)

		# print "all_orders:",all_orders
				
		del request.session['startdate']
		del request.session['search_with_start']


	elif 'search_with_end' in request.session:
		# print "enddate:",request.session['enddate']
		first_enddate = str(request.session['enddate'])
		enddate = first_enddate.split('-')
		# print "enddate:",enddate
		all_orders = requestOrder.objects.filter(
			created_on_by__year=enddate[0],
			created_on_by__month=enddate[1],
			created_on_by__day=enddate[2],
			deleted=False)

		# print "all_orders:",all_orders

		del request.session['enddate']
		del request.session['search_with_end']


	elif 'search_with_start_end' in request.session:
		# print "startdate and enddate"
		all_orders = requestOrder.objects.filter(created_on_by__range=[request.session['startdate'],request.session['enddate']],
			deleted=False)
		# print "all_orders:",all_orders

		del request.session['search_with_start_end']
		del request.session['enddate']
		del request.session['startdate']

	else:
		all_orders = requestOrder.objects.filter(deleted=False)
		# print "all_orders:",all_orders


	context['all_orders'] = all_orders
	return render(request, 'wfm_admin/adminPage.html',context)


@login_required
def orderTypeView(request,status):
	context = {}
	template_name = 'wfm_admin/order_type.html'
	order_type = requestOrder.objects.filter(status=status,deleted=False)
	context['order_type'] = order_type
	context['status'] = status.title() + " " + "Orders"
	return render(request,template_name,context)


@login_required
def search_for_order(request):
	context = {}
	template_name = ""
	rp = request.POST

	if rp.has_key('requested_item'):
		requested_item = str(rp.get('requested_item'))
		request.session['requested_item'] = requested_item
		return redirect('dashboard:inventory')

	else:
		request_item = str(rp.get('request_order'))
		startdate = str(rp.get('startdate'))
		enddate = str(rp.get('enddate'))

		if request_item != '' and startdate == '' and enddate == '':
			request.session['request_item'] = request_item
			request.session['search_with_request_item'] = 'search_with_request_item'
			return redirect("dashboard:admindashboard")

		elif request_item != '' and startdate != '' and enddate == '':
			request.session['request_item'] = request_item
			request.session['startdate'] = startdate
			request.session['search_with_request_item_start'] = 'search_with_request_item_start'
			return redirect("dashboard:admindashboard")

		elif request_item != '' and enddate != '' and startdate == '':
			request.session['request_item'] = request_item
			request.session['enddate'] = enddate
			request.session['search_with_request_item_end'] = 'search_with_request_item_end'
			return redirect("dashboard:admindashboard")

		elif startdate != '' and request_item == '' and enddate == '':
			request.session['startdate'] = startdate
			request.session['search_with_start'] = 'search_with_start'
			return redirect("dashboard:admindashboard")

		elif startdate != '' and enddate != '' and request_item == '':
			if (startdate >= enddate):
				# print True
				messages.warning(request,"The start date cannot be greater than or equal to the end date")
				return redirect(request.META['HTTP_REFERER'])
			else:
				request.session['startdate'] = startdate
				request.session['enddate'] = enddate
				request.session['search_with_start_end'] = 'search_with_start_end'
				return redirect("dashboard:admindashboard")

		elif enddate != '' and request_item == '' and startdate == '':
			request.session['enddate'] = enddate
			request.session['search_with_end'] = 'search_with_end'
			return redirect("dashboard:admindashboard")

		elif request_item != '' and startdate != '' and enddate != '':
			if (startdate >= enddate):
				# print True
				messages.warning(request,"The start date cannot be greater than or equal to the end date")
				return redirect(request.META['HTTP_REFERER'])

			else:
				request.session['request_item'] = request_item
				request.session['startdate'] = startdate
				request.session['search_with_all'] = 'search_with_all'
				request.session['enddate'] = enddate
				return redirect("dashboard:admindashboard")


@login_required
def inventory(request):
	context = {}
	if "requested_item" in request.session:
		# print "searched for:", request.session['requested_item']
		search_value = request.session['requested_item'].strip()
		all_items = item.objects.filter((
			Q(item_name__contains=search_value)|
			Q(item_category__icontains=search_value)|
			Q(item_num__icontains=search_value)
			),
			deleted = False)

		del request.session['requested_item']
	else:
		all_items = item.objects.filter(deleted=False)

	paginator = Paginator(all_items,5)
	page = request.GET.get('page')
	try:
	    items = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    items = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    items = paginator.page(paginator.num_pages)
	context['items'] = items
	return render(request,'wfm_admin/items_inventory.html',context)


@login_required
def viewitems(request,item_id):

	context = {}
	order_request_item = requestOrder.objects.filter(id=item_id)
	context['order_items'] = order_request_item
	return render(request,'wfm_admin/itemsinorder.html',context)

	# context = {}
	# rp = request.POST
	# print "rp:",rp
	# if rp:
	# 	order_public_key = str(rp.get('item_request'))
	# 	order_request_item = requestOrder.objects.filter(id=order_public_key)
	# 	print "order_item:",order_request_item
	# 	context['order_items'] = order_request_item
	# 	return render(request,'wfm_admin/itemsinorder.html',context)
	# else:
	# 	return redirect("dashboard:admindashboard")




@login_required
def delete_order(request,item_id):

	current_time = datetime.datetime.now()
	order_to_delete = requestOrder.objects.get(id=item_id)

	history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=order_to_delete.id,
			history_type='order',
			message="This order -" + order_to_delete.ordernumber + "was deleted by" + request.user.username + "on" + str(current_time))
	if created:
		order_to_delete.deleted = True
		order_to_delete.save()
		# print "was created"
	else:
		print "not created"

	return redirect(request.META['HTTP_REFERER'])



@login_required
def item_stock_delete(request,item_id):

	current_time = datetime.datetime.now()
	item_to_delete = item.objects.get(id=item_id)

	history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=item_to_delete.id,
			history_type='inventory',
			message="This item -" + item_to_delete.item_num + "was deleted by" + request.user + "on" + str(current_time))
	if created:
		item_to_delete.deleted = True
		item_to_delete.save()
		# print "was created"
	else:
		print "not created"

	return redirect(request.META['HTTP_REFERER'])



@login_required
def item_delete(request,item_id):

	current_time = datetime.datetime.now()
	item_to_delete = requestItem.objects.get(id=item_id)

	history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=item_to_delete.id,
			history_type='item',
			message="This order -" + item_to_delete + "was deleted by" + request.user + "on" + str(current_time))
	if created:
		item_to_delete.deleted = True
		item_to_delete.save()
		# print "was created"
	else:
		print "not created"


	return redirect(request.META['HTTP_REFERER'])



@login_required
def update_orders(request):
	context = {}
	rp = request.POST
	# print "rp:",rp
	status = str(rp.get('orders_status')).split(",")
	update_type = str(rp.get('order_update_type'))
	order_list_ids = str(rp.get('orders_ids')).split(",")
	# print "status:",status
	# print "update_type:",update_type
	# print "order_list:",order_list_ids
	# order = str(rp.get('item_to_delete'))
	# order_to_delete = requestOrder.objects.filter(id=order)
	# order_to_delete.delete()
	return redirect("dashboard:admindashboard")


@login_required
def update_bulk_items(request):

	context = {}

	rp = request.POST
	# print "rp:",rp

	current_time = datetime.datetime.now()
	order_request_number = str(rp.get('order_id'))
	status = str(rp.get('items_status')).split(",")
	update_type = str(rp.get('items_update_type'))
	items_list_ids = str(rp.get('items_ids')).split(",")
	items_list_qty = str(rp.get('items_qty')).split(",")
	items_list_num = str(rp.get('items_num')).split(",")
	combined_list = dict(zip(items_list_ids,zip(items_list_qty,items_list_num)))

	# print "status:",status
	# print "update_type:",update_type
	# print "items_list:",items_list_ids
	# print "items_list_qty:",items_list_qty
	# print "items_list_num:",items_list_num
	# print "combined_list:", combined_list
	# print "order_request_number:",order_request_number

	for key in combined_list:

		item_in_stock = item.objects.get(item_num=combined_list[key][1])
		# print "item_in_stock quantity:",item_in_stock.item_quantity

		if item_in_stock.item_quantity < int(combined_list[key][0]):
			item_in_stock.item_quantity = item_in_stock.item_quantity
			item_in_stock.save()

			itm_to_update = requestItem.objects.get(id=key)
			itm_to_update.status = "Pending"

			history_obj,created = History.objects.get_or_create(
					user=request.user,
					history_number=itm_to_update.id,
					history_type='item',
					message="This request item with S/No" + ":" + str(itm_to_update.number) + " could not be processed by " + str(request.user)+ "on" + str(current_time) + " due to insufficient quantity.")
	
			itm_to_update.save()

		else:
			itm_to_update = requestItem.objects.get(id=key)

			if itm_to_update.status == "approved":
				item_in_stock.item_quantity = item_in_stock.item_quantity
				item_in_stock.save()

			else:
				item_in_stock.item_quantity = item_in_stock.item_quantity - int(combined_list[key][0])

				history_obj,created = History.objects.get_or_create(
				user=request.user,
				history_number=item_in_stock.id,
				history_type='inventory',
				message="Outgoing stock " + str(current_time.replace(microsecond=0))  + " signed by " + str(request.user) + " to " + str(itm_to_update.user.first_name) + " " + str(itm_to_update.user.last_name) + " " + " Dept: " + str(itm_to_update.user.useraccount.department) + "-" + "(Current stock:" + str(item_in_stock.item_quantity) + ")")

				item_in_stock.save()

			itm_to_update.status = update_type

			history_obj,created = History.objects.get_or_create(
					user=request.user,
					history_number=itm_to_update.id,
					history_type='item',
					message="This request item with S/No" + ":" + str(itm_to_update.number) + " was approved by " + str(request.user) + " on " + str(current_time))
	
			itm_to_update.save()


	order_statuses = []
	approved = []
	processing = []

	order_in_view = requestOrder.objects.get(ordernumber=order_request_number)

	for order in order_in_view.requestitem_set.all():
		order_statuses.append(order.status)
		if order. status == "approved":
			approved.append(order.status)
		else:
			processing.append(order.status)

	# print "order_statuses:",order_statuses

	if all_same(order_statuses):
		messages.success(request,"All the items have been successfully approved")
		order_in_view.status = "approved"

		history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=order_in_view.id,
			history_type='order',
			message="All request items for this order have been approved by " + str(request.user) + " on " + str(current_time.replace(microsecond=0))
			) 

		order_in_view.save()

	else:
		order_in_view.status = "processing"

		history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=order_in_view.id,
			history_type='order',
			message= str(len(approved)) + " item(s) approved " + " and " + str(len(processing)) + " item(s) pending approval " + " as at " + str(current_time.replace(microsecond=0)) + " by " + str(request.user)
			)

		order_in_view.save()

	return redirect(request.META['HTTP_REFERER'])


@login_required
def edit_item_inventory(request):

	action_taker = request.user.email
	current_time = datetime.datetime.now()

	rp = request.POST
	# print "rP:", rp
		

	itemToEdit                   = item.objects.get(id=str(rp.get('item_id')))

	qty 						 = str(itemToEdit.item_quantity)

	itemToEdit.user              = request.user
	itemToEdit.item_name         = str(rp.get('item_name'))
	itemToEdit.item_category     = str(rp.get('item_category'))
	itemToEdit.item_quantity 	 = str(rp.get('item_quantity'))
	itemToEdit.item_num          = str(rp.get('item_num'))
	itemToEdit.item_edited_on    = current_time
	itemToEdit.edited_by    	 = action_taker

	item_num = str(itemToEdit.item_num)
	quantity = str(itemToEdit.item_quantity)
	first_name = str(request.user.first_name)
	last_name = str(request.user.last_name)
	request_user = first_name + " " + last_name


	history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=itemToEdit.id,
			history_type='inventory',
			message="Updated on " + str(current_time.replace(microsecond=0))  + " by " + request_user + " from " + qty + " to " + quantity + " " + "(Current stock:" + quantity + ")")

	if created:
		# print "update history was cretaed"
		itemToEdit.save()
	else:
		print "update history was not created"

	messages.info(request,"item was successfully edited")

	return redirect("dashboard:inventory")


@login_required
def create_item_inventory(request):

	action_taker = request.user.email
	current_time = datetime.datetime.now()

	rp = request.POST
	# print "rP:", rp

	if request.method == "POST":
	 	form = itemForm(request.POST, request.FILES)

	 	if form.is_valid():
	 		create_item_form = form.save(commit=False)
	 		create_item_form.item_edited_by = action_taker
	 		create_item_form.user= request.user
	  		create_item_form.item_name = str(rp.get('item_name'))
	  		create_item_form.item_category = str(rp.get('item_category'))
	  		create_item_form.item_num = getCatPrefix(str(rp.get('item_category')))
	  		create_item_form.item_quantity = str(rp.get('item_quantity'))
	  		create_item_form.item_desc = str(rp.get('item_desc'))

			messages.info(request,"item was successfully added")
  			create_item_form.save()
		
	  		return HttpResponseRedirect(reverse('dashboard:inventory'))

	  	else:
	  		# print form.errors
			messages.warning(request,"item was not successfully added")
	  		return HttpResponseRedirect(reverse('dashboard:inventory'))

	return redirect(request.META['HTTP_REFERER'])


@login_required
def edit_request_item(request):

	action_taker = request.user.email
	current_time = datetime.datetime.now()

	rp = request.POST
	# print "rP:", rp	

	itemToEdit              = requestItem.objects.get(id=str(rp.get('item_id')))
	qty                     = itemToEdit.quantity
	itemToEdit.name         = str(rp.get('item_name'))
	itemToEdit.category     = str(rp.get('item_category'))
	itemToEdit.quantity 	= str(rp.get('item_quantity'))
	itemToEdit.number       = str(rp.get('item_num'))
	itemToEdit.edited_on    = current_time
	itemToEdit.edited_by    = action_taker

	history_obj,created = History.objects.get_or_create(
		user=request.user,
		history_number=itemToEdit.id,
		history_type='item',
		message="Edited on " + str(current_time.replace(microsecond=0))  + " by " + str(request.user) + " from " + str(qty) + " to " + str(rp.get('item_quantity')))

	if created:
		# print "update history was cretaed"
		itemToEdit.save()
	else:
		print "update history was not created"

	messages.info(request,"item was successfully edited")

	return redirect(request.META['HTTP_REFERER'])


@login_required
def update_request_items(request):
	# print "got here"

	context = {}
	current_time = datetime.datetime.now()


	rp = request.POST
	# print "rp:",rp

	order_request_number = str(rp.get('order_num_id'))
	status = str(rp.get('item_status'))
	item_id = str(rp.get('item_id'))
	item_qty = str(rp.get('item_qty'))
	item_num = str(rp.get('item_num'))

	# print "status:",status
	# print "item_id",item_id
	# print "item_qty:",item_qty
	# print "item_num:",item_num
	# print "order_request_number:",order_request_number

	item_in_stock = item.objects.get(item_num=item_num)
	# print "item_in_stock quantity:",item_in_stock.item_quantity

	if item_in_stock.item_quantity < int(item_qty):
		messages.warning(request,"Oops this item cannot be aproved at the moment due to insufficient stock")
		return redirect(request.META['HTTP_REFERER'])

	else:
		item_in_stock.item_quantity = item_in_stock.item_quantity - int(item_qty)

		order_statuses = []

		itm_to_update = requestItem.objects.get(id=item_id)
		itm_to_update.status = status


		hist_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=item_in_stock.id,
			history_type='inventory',
			message="Outgoing stock " + str(current_time.replace(microsecond=0))  + " signed by " + str(request.user) + " to " + str(itm_to_update.user.email) + "-" + "(Current stock:" + str(item_in_stock.item_quantity) + ")")

		if created:
			# print "update history was cretaed"
			item_in_stock.save()
		else:
			print "update history was not created"

		history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=itm_to_update.id,
			history_type='item',
			message="This request item with S/No" + ":" + str(itm_to_update.number) + " was approved by " + str(request.user) + " on " + str(current_time))

		if created:
			# print "update history was cretaed"
			itm_to_update.save()
		else:
			print "update history was not created"

	order_statuses = []
	approved = []
	processing = []

	order_in_view = requestOrder.objects.get(ordernumber=order_request_number)

	for order in order_in_view.requestitem_set.all():
		order_statuses.append(order.status)
		if order.status == "approved":
			approved.append(order.status)
		else:
			processing.append(order.status)

	# print "order_statuses:",order_statuses

	if all_same(order_statuses):
		order_in_view.status = "approved"

		history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=order_in_view.id,
			history_type='item',
			message="All request items for this order have been approved by " + str(request.user) + " on " + str(current_time.replace(microsecond=0))
			)

		order_in_view.save()

	else:
		order_in_view.status = "processing"

		history_obj,created = History.objects.get_or_create(
			user=request.user,
			history_number=order_in_view.id,
			history_type='item',
			message= str(len(approved)) + " item(s) approved " + " and " + str(len(processing)) + " item(s) pending approval " + " as at " + str(current_time.replace(microsecond=0)) + " by " + str(request.user)
			)

		order_in_view.save()

	return redirect(request.META['HTTP_REFERER'])



@login_required
def print_order(request, item_id):
	order = get_object_or_404(requestOrder, id=item_id)
	items_assigned_to_order = requestItem.objects.filter(requestOrder = order)
	return render_to_response('wfm_admin_snippet/print_order.html',
                              {'order': order, #'shipments': shipments,
                               'items_assigned_to_order':[itm.request_item_info() for itm in items_assigned_to_order]},
                               context_instance=RequestContext(request))


@login_required
def history(request,item_id,history_type):
	# print "got here"
	context = {}

	if history_type == "inventory":
		item_in_view = item.objects.get(id=item_id)
		history_obj = History.objects.filter(history_number=item_in_view.id)
		# print "history:",history_obj
		context['item_in_view'] = item_in_view
		context['history_obj'] = history_obj
		context['inventory_req'] = 'inventory_req'

	elif history_type == "order":
		item_in_view = requestOrder.objects.get(id=item_id)
		history_obj = History.objects.filter(history_number=item_in_view.id)
		context['item_in_view'] = item_in_view
		context['history_obj'] = history_obj
		context['order_req'] = 'order_req'

	else:
		item_in_view = requestItem.objects.get(id=item_id)
		history_obj = History.objects.filter(history_number=item_in_view.id)
		context['item_in_view'] = item_in_view
		context['history_obj'] = history_obj
		context['item_req'] = 'item_req'

	return render(request,'wfm_admin/history.html',context)


@login_required
def manage_users(request):
	context = {}
	rp = request.POST
	# print "rp:",rp
	if request.method == "POST" and rp.has_key('search_value'):
		search_value = str(rp.get('search_value'))
		searched_user = User.objects.filter(
			Q(first_name__contains=search_value) |
			Q(last_name__contains=search_value) |
			Q(email__contains=search_value)
			)
		context['searched_user'] = searched_user
	else:	
		users = User.objects.all()
		context['users'] = users
	return render(request,'wfm_admin/manage_users.html',context)


@login_required
def create_supply(request):
	rp = request.POST
	# print 'rp: ',rp
	items_ids = str(rp.get('supply_items_ids')).split(',')
	items_qty = str(rp.get('supply_items_qty')).split(',')
	dict_of_ids_qty = dict(zip(items_ids,items_qty)) #convert two equal list into a dictionary
	# print "dict: ",dict_of_ids_qty

	if request.method == "POST":
		items_list = []
		cat_list = []
		new_list = []
		for key,value in dict_of_ids_qty.items():
			print "key,value: ",key,value
			item_obj = item.objects.filter(pk=key)[0]
			item_obj.item_quantity_required = value
			items_list.append(item_obj)
			cat_list.append(item_obj.item_category)
		for i in cat_list:
			if i in new_list:
				pass
			else:
				new_list.append(i)
		template_name = 'wfm_admin/supply_order.html'
		return render(request,template_name,{"item_obj":items_list, "items_cat_list":new_list})

	else:

		context = {}
		template_name = 'wfm_admin/create_supply.html'
		items_below_threshold = item.objects.filter(item_quantity__lt=F('threshold'))
		paginator = Paginator(items_below_threshold,10)
		page = request.GET.get('page')

		try:
		    items_below_threshold = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    items_below_threshold = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    items_below_threshold = paginator.page(paginator.num_pages)

		context['items_below_threshold'] = items_below_threshold
		return render(request,template_name,context)


@login_required
def users_access(request):
	# print "i got here"
	rp = request.POST
	# print rp
	users_list_ids = str(rp.get('users_access_ids')).split(",")
	status = str(rp.get('users_access_status'))
	# print "ids: ",users_list_ids
	# print "status: ",status
	if status == "Staff":
		for user_id in users_list_ids:
			user_obj = User.objects.get(id=user_id)
			user_obj.is_staff = True
			user_obj.save()
			# print model_to_dict(user_obj)

	else:
		for user_id in users_list_ids:
			user_obj = User.objects.get(id=user_id)
			user_obj.is_staff = False
			user_obj.save()
			# print model_to_dict(user_obj)

	messages.success(request,'Successful')
	return redirect(request.META['HTTP_REFERER'])







