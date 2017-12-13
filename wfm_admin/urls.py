from django.conf.urls import url
from wfm_admin import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    url(r'^admin_dashboard/$', views.admindashboard, name='admindashboard'),
    url(r'^order/search/$', views.search_for_order, name='order_search'),
    url(r'^item/inventory/$', views.inventory, name='inventory'),
    url(r'^order/type/(?P<status>\w+)/$', views.orderTypeView, name='order_type'),
    url(r'^order/items/(?P<item_id>.+)/$', views.viewitems, name="items"),
    url(r'^order/delete/(?P<item_id>.+)/$', views.delete_order, name="delete_order"),
    url(r'^order/update/$', views.update_orders, name="update_orders"),
    url(r'^item/update/$', views.update_bulk_items, name="update_items"),
    url(r'^stockitem/delete/(?P<item_id>.+)/$', views.item_stock_delete, name="delete_stock_item"),
    url(r'^item/edit/$', views.edit_item_inventory, name="edit_item"),
    url(r'^item/request/edit/$', views.edit_request_item, name="edit_request_item"),
    url(r'^item/update/request/$', views.update_request_items, name="update_request_items"),
    url(r'^item/create/$', views.create_item_inventory, name="create_item"),
    url(r'^item/delete/(?P<item_id>.+)/$', views.item_delete, name="delete_item"),
    url(r'^item/history/(?P<item_id>.+)/(?P<history_type>\w+)/$', views.history, name="history"),
    url(r'^order/manifest/(?P<item_id>.+)/$', views.print_order, name="print-order"),
    url(r'^supply/manager/$', views.create_supply, name="create_supply"),
    url(r'^user/manager/$', views.manage_users, name="usermanager"),
    url(r'^access/$', views.users_access, name="users_access"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)