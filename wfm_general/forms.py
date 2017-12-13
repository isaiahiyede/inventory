from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime
from wfm_general.models import *


TITLE = (
  
    ('', 'Select Title'),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms.', 'Ms.'),
    ('Dr', 'Dr'),
    ('Engr', 'Engr'),

    )

DEPARTMENTS = (
    
    ('', 'Select Department'),
    ('HR', 'Human Resources'),
    ('IT','IT'),
    ('Accounts','Accounts'),
    ('Logistics','Logistics'),
    ('Security','Security'),
    ('Cleaning','Cleaning'),

    )



class LoginForm(forms.ModelForm):
    email      =    forms.EmailField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Email','required':'required','class': 'form-group form-control'}))
    password   =    forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder':'Password','required':'required','class': 'form-group form-control'}))

    class Meta:
       # Associate form with a model
       	model = User
        fields = ('email','password',)




class UserForm(forms.ModelForm):
	username        =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Username', 'required':'required','class': 'form-group form-control'}))
	email           =    forms.EmailField(max_length = 128, help_text = "",widget=forms.EmailInput(attrs={'placeholder': 'Email','required':'required','class': 'form-group form-control'}))
	password        =    forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder':'Password','required':'required','class': 'form-group form-control'}))
	first_name      =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'First Name', 'required':'required','class': 'form-group form-control'}))
	last_name       =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'required':'required','class': 'form-group form-control'}))

	class Meta:
		model = User
		fields =  ('username','email','password','first_name','last_name',)




class UserAccountForm(forms.ModelForm):
    password2            =    forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','required':'required','class': 'form-group form-control'}))
    phone_number         =    forms.CharField(help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'required':'required', 'class': 'form-group form-control' }))
    department           =    forms.ChoiceField(widget=forms.Select(attrs={'class': 'myStyle form-group form-control select_outer two scrolled','required':'required'}), choices = DEPARTMENTS)
    title                =    forms.ChoiceField(widget=forms.Select(attrs={'class': 'myStyle form-group form-control select_outer two scrolled','required':'required'}), choices = TITLE)



    class Meta:
        model = UserAccount
        fields = ('phone_number','title', 'department',)