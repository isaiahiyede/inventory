from django.contrib import admin
from wfm_client.models import item, requestOrder, requestItem, History



# Register your models here.


class itemAdmin(admin.ModelAdmin):
	list_display = ('item_name','item_category','item_num','item_desc','item_quantity','item_created_on','threshold')
	search_fields = ('item_name',)


class requestOrderAdmin(admin.ModelAdmin):
	list_display = ('ordernumber','requestee','status','created_on_by',)
	search_fields = ('ordernumber',)


class requestItemAdmin(admin.ModelAdmin):
	list_display = ('user','name','quantity','category','status','created_on',)
	search_fields = ('name',)


class HistoryAdmin(admin.ModelAdmin):
	list_display = ('user','message','created_on',)


admin.site.register(History, HistoryAdmin)
admin.site.register(item, itemAdmin)
admin.site.register(requestOrder, requestOrderAdmin)
admin.site.register(requestItem, requestItemAdmin)