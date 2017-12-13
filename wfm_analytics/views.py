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
import collections
import string

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from wfm_general.models import *
from wfm_client.models import *
from wfm_client.forms import itemForm, requestOrderForm, requestItemForm
from WFM_INV.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
from chartit import DataPool, Chart, PivotDataPool, PivotChart
from datetime import timedelta




# Create your views here.

def jsondump(response_list):
	return json.dumps(list(response_list), cls=DjangoJSONEncoder)

def all_depts_in_db():
	all_depts  = requestItem.objects.values_list('department', flat = True)
	unique_depts = []
	for x in all_depts:
		if x not in unique_depts:
			unique_depts.append(str(x))
		else:
			pass
	return jsondump(unique_depts)

def get_percentage(value,total):
	return (value * 100) / total

@login_required
def analytics_page(request,startdate,enddate,chart_type,depts_list):

	current_date = datetime.datetime.today()
	new_current_date = str(current_date).split('-')
 
	context = {}

	dept = []
	colors = ['FFFF10','FF0000','00FF00','0000FF','BBBB00','BB0000','008800','880000','000088','888800']
	
	if startdate and enddate and depts_list:
		if (startdate >= enddate):
			messages.warning(request,"The start date cannot be greater than or equal to the end date")
			return redirect(request.META['HTTP_REFERER'])
		else:
			enddate = datetime.datetime.strptime(enddate,'%Y-%m-%d') + datetime.timedelta(days=1)
			print "enddate:",enddate
			for item_request in requestItem.objects.filter(Q(department__in=depts_list),Q(created_on__range=[startdate,enddate])):
				dept.append(str(item_request.department))		

	elif startdate and enddate and not depts_list:
		if (startdate >= enddate):
			messages.warning(request,"The start date cannot be greater than or equal to the end date")
			return redirect(request.META['HTTP_REFERER'])
		else:
			enddate = datetime.datetime.strptime(enddate,'%Y-%m-%d') + datetime.timedelta(days=1)
			print "enddate:",enddate
			for item_request in requestItem.objects.filter(created_on__range=[startdate,enddate]):
				dept.append(str(item_request.department))
			
	elif startdate and not enddate and not depts_list:
		start_date = startdate.split("-")
		for item_request in requestItem.objects.filter(
			created_on__year=start_date[0],
			created_on__month=start_date[1],
			created_on__day=start_date[2]):
			dept.append(str(item_request.department))
			
	elif startdate and not enddate and depts_list:
		start_date = startdate.split("-")
		for item_request in requestItem.objects.filter(
			Q(department__in=depts_list),
			Q(created_on__year=start_date[0],
			 created_on__month=start_date[1],
			 created_on__day=start_date[2])):
			dept.append(str(item_request.department))
			
	elif enddate and not startdate and not depts_list:
		end_date = enddate.split("-")
		for item_request in requestItem.objects.filter(
			created_on__year=end_date[0],
			created_on__month=end_date[1],
			created_on__day=end_date[2]):
			dept.append(str(item_request.department))
			
	elif enddate and depts_list and not startdate:
		end_date = enddate.split("-")
		for item_request in requestItem.objects.filter(Q(department__in=depts_list),
			Q(created_on__year=end_date[0],
			 created_on__month=end_date[1],
			 created_on__day=end_date[2])):
			dept.append(str(item_request.department))
			
	elif not startdate and not enddate and depts_list:
		for item_request in requestItem.objects.filter(
			Q(department__in=depts_list),
			Q(created_on__month=new_current_date[1])
			):
			dept.append(str(item_request.department))			
	
	else:
		for item_request in requestItem.objects.filter(created_on__month=new_current_date[1]):
			dept.append(str(item_request.department))
			
	depts = []
	req_items = []
	labels = []
	chart_color = []

	dict_of_items = {x:dept.count(x) for x in dept}

	for key in dict_of_items:
		depts.append(key)
		req_items.append(dict_of_items[key])
		if not chart_type == 'bar_chart':
			labels.append(str(key) + "-" + str(get_percentage(dict_of_items[key],len(dept))) + '%')
		else:
			labels.append(str(key) + "-" + str(dict_of_items[key]))

	for clr in range(len(depts)):
		chart_color.append(colors[clr])

	context['depts'] = depts
	context['req_items'] = req_items
	context['colors'] = colors
	context['labels'] = labels
	context['month'] = current_date.strftime('%B')
	context['dept'] = dept

	if chart_type == "bar_chart":
		return render(request, 'bar-chart.html',context)
	else:
		return render(request, 'pie-chart.html',context)

@login_required
def departmentalanalysis(request):
	context = {}
	rp = request.POST

	startdate = str(rp.get('start_date'))
	enddate = str(rp.get('end_date'))
	chart_type = str(rp.get('optradio'))
	dpts = str(rp.get('depts')).replace(" ","").split(',')
	depts_list = []

	for dpt in dpts:
		if dpt in depts_list or dpt == "":
			pass
		else:
			depts_list.append(dpt)

	if chart_type == "bar_chart":
		return analytics_page(request,startdate,enddate,chart_type,depts_list)

	elif chart_type == "pie_chart":
		return analytics_page(request,startdate,enddate,chart_type,depts_list)

	else:
		all_depts = UserAccount.objects.all()
		new_list = []
		for i in all_depts:
			if i.department in new_list:
				pass
			else:
				new_list.append(str(i.department))
		test_list = ','.join(new_list)
		context['test_list'] = test_list
		context["all_depts"] = all_depts_in_db()

	return render(request, 'analysispage.html',context)


