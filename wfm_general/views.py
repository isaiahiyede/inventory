from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from wfm_general.models import *
from wfm_general.forms import UserForm, UserAccountForm, LoginForm
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
from django.core.urlresolvers import reverse
import json
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage


# Create your views here.


def homePage(request):
	context = {}
	return render(request, 'wfm_general/indexPage.html',context)	


def successful_registration(request):
    context = {}    
    return render(request, 'wfm_general/successfulReg.html', context)


def userLogin(request):
	context = {}
	username  = ""
	context['login_form'] = LoginForm()

	if request.method == "POST":
	    form = LoginForm(data = request.POST)

	    if form.is_valid:
	        email    = request.POST.get('email').strip().lower()
	        password = request.POST.get('password').strip()
	        
	        user_account =  User.objects.filter(email = email)

	        if user_account.exists():
	            username = user_account[0].username
	        auth_user = authenticate(username = username, password = password)

	        if auth_user is not None:
	            user = auth_user

	            if user.is_active:
	                login(request, user)                    

	                if user.is_staff:
	                    response =  redirect(reverse('dashboard:admindashboard'))
	                    return response
	                   
	                else:
	                    response = redirect(reverse("client:client_page"))
	                    return response
	        else:
	            print "No details found for %s" %(email)
	            context['no_record_found'] = True
	        return render(request, 'wfm_general/login.html', context )
	else:
		return render(request, 'wfm_general/login.html',context)





def userRegister(request):
	print "Got here"
	context = {}	
	context['user_form']           =     UserForm()
	context['user_account_form']   =     UserAccountForm()
	if  request.method            ==     "POST":
	    rp                         =     request.POST
	    print "rp:",rp
	    if not request.POST.has_key('created_by_admin'):
	        
	        userform                   =     UserForm(data =  request.POST)
	        user_account_form          =     UserAccountForm(data = request.POST)

	        if User.objects.filter(username = rp['username']).exists():                
	            return render(request, 'wfm_general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'username_is_taken':True})
	        if User.objects.filter(email = rp['email']).exists():                
	            return render(request, 'wfm_general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'email_is_taken':True})
	        if UserAccount.objects.filter(phone_number = rp.get('phone_number')).exists():
	            return render(request, 'wfm_general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'phone_is_taken':True})
	        else:
	            if userform.is_valid and user_account_form.is_valid:
	                password1   = rp['password']
	                password2   = rp['password2']
	                if password1 != password2:
	                    return render(request, 'wfm_general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_mismatch':True})
	                if len(password1) < 6:
	                    return render(request, 'wfm_general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_too_short':True})
	                user = User.objects.create(username = rp['username'], email = rp['email'].lower(),
	                    first_name = rp['first_name'], last_name = rp['last_name'])
	                user.set_password(rp['password']) 
	                user.save()
	                new_user_account = UserAccount.objects.create(user = user,title= rp['title'], 
                        phone_number = rp.get('phone_number'),department = rp.get('department'), 
                        created_on = datetime.datetime.now())
	                context['user_is_created']  =    True
	                context['email']            =    rp['email']
	                print "user creation for %s successful" %(user)
	                return redirect(reverse('general:successful_registration'))
	            else:
	                print "here4"                    
	                return render(request, 'wfm_general/register.html', context)
	    else:
	        password = generate_pw()
	        print "new password ", password
	        if User.objects.filter(email = rp['email']).exists() and User.objects.filter(username = rp['username']).exists():
	            messages.info(request, "Sorry! the username and email address you entered is taken.")
	            return redirect(request.META['HTTP_REFERER'])
	        if User.objects.filter(username = rp['username']).exists():
	            messages.info(request, "Sorry! that username is taken.")
	            return redirect(request.META['HTTP_REFERER'])
	        if UserAccount.objects.filter(phone_number = rp['phone_number']).exists():
	            messages.info(request, "Sorry! that phone number is taken.")
	            return redirect(request.META['HTTP_REFERER'])
	        if User.objects.filter(email = rp['email']).exists():
	            messages.info(request, "Sorry! that email is taken.")
	            return redirect(request.META['HTTP_REFERER'])

	        user = User.objects.create(username= rp['username'], email = rp['email'].lower(),first_name = rp['first_name'], last_name = rp['last_name'])
	        user.set_password(password) 
	        user.save()
	        new_user_account = UserAccount.objects.create(user = user, phone_number = rp['phone_number'], created_by_admin = True)
	        login_link = DOMAIN_NAME + "/login"
	        print login_link

	        if new_user_account:
	            messages.success(request, "Customer account has been created for " + rp['first_name'].title())
	            # send mail to customer

	        subject = "[James Spence Authentication] Your account has been created successfully"
	        email_context = {'customer':rp['first_name'], 'email':rp['email'], 'password':password, 'login_link':login_link}

	        send_user_mail(subject, DEFAULT_FROM_EMAIL, rp['email'],'wfm_general/admin_user_registration_mail_template.html', email_context)


	        return redirect(request.META['HTTP_REFERER'])            
	return render(request, 'wfm_general/register.html',context)


def user_logout(request):
	response = redirect(reverse('general:homePage'))
	logout(request)
	return response
