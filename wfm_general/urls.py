from django.conf.urls import url
from wfm_general import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	url(r'^$', views.homePage, name='homePage'),
    url(r'^login/$', views.userLogin, name='userLogin'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.userRegister, name='userRegister'),
    url(r'^successful_registration/$', views.successful_registration, name='successful_registration'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)