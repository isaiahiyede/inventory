from django.conf.urls import url
from wfm_client import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^client_page/$', views.client_page, name='client_page'),
    url(r'^request_order_list_view/$', views.request_order_list_view, name='request_order_list_view'),
    url(r'^client_requestViewPage/$', views.client_requestViewPage, name='client_requestViewPage'),
    url(r'^confirmRequest/$', views.confirmRequest, name='confirmRequest'),
    url(r'^request_form/$', views.request_form, name='request_form'),
    url(r'^deleteItem/(?P<item_id>[-\w]+)/(?P<action>\w+)/$', views.deleteItem, name="deleteItem"),
    url(r'^editItem/$', views.editItem, name="editItem"),
    url(r'^history/(?P<item_id>[-\w]+)/$', views.show_item_history, name="item_history"),
    url(r'^getCategory/$', views.getCategory, name="getCategory"),        

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)