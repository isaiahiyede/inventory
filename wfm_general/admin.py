from django.contrib import admin
from wfm_general.models import *

# Register your models here.


class UserAccountAdmin(admin.ModelAdmin):
	list_display = ('user','phone_number','created_on')
	search_fields = ('user__email',)

	exclude = ['password2']



admin.site.register(UserAccount, UserAccountAdmin)
