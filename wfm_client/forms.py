from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime
from wfm_client.models import item, requestOrder, requestItem


CATEGORY = (
 	
 	('', 'Select a Category'),
 	('CIT', 'Cleaning Items'),
 	('BVG', 'Beverages'),
 	('STA', 'Stationaries'),

	)



class itemForm(forms.ModelForm):
	item_name         =    forms.CharField(max_length = 50, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Name', 'required':'required','class': 'form-group form-control'}))
	item_category     =    forms.CharField(max_length = 50, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Category', 'required':'required','class':'form-group form-control myStyle'}))
	item_desc         =    forms.CharField(max_length = 50, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Description', 'required':'required','class':'form-group form-control myStyle'}))
	item_quantity     =    forms.IntegerField(help_text = "",widget=forms.NumberInput(attrs={'placeholder': 'Quantity', 'required':'required','class': 'form-group form-control'}))
	item_image        =    forms.ImageField(help_text = "Upload Image", widget=forms.FileInput(attrs={'class': 'form-group form-control'}))



	class Meta:
		model  = item
		fields =  ('item_name','item_category','item_quantity','item_image','item_desc',)



class requestOrderForm(forms.ModelForm):

	class Meta:
		model  = requestOrder
		fields =  '__all__'



class requestItemForm(forms.ModelForm):
	name            =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Name', 'required':'required','class': 'form-group form-control'}))
	category        =    forms.CharField(max_length = 100, help_text = "",widget=forms.TextInput(attrs={'placeholder': 'Name', 'required':'required','class': 'form-group form-control'}))
	quantity        =    forms.IntegerField(help_text = "",widget=forms.NumberInput(attrs={'placeholder': 'Quantity', 'required':'required','class': 'form-group form-control'}))

	class Meta:
		model  = requestItem
		fields =  ('name','category','quantity',)