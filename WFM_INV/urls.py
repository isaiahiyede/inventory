"""WFM_INV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import TemplateView
from django.shortcuts import render

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^client/', include('wfm_client.urls', namespace='client')),
    url(r'^dashboard/', include('wfm_admin.urls', namespace='dashboard')),
    url(r'^analytics/', include('wfm_analytics.urls', namespace='analytics')),
    url(r'^', include('wfm_general.urls', namespace='general')),

    # Password reset urls
    url(r'^reset/form/$', TemplateView.as_view(template_name = 'registration/password_reset_email.html')),
    url(r'^resetpassword/passwordsent/$', password_reset_done, name="password_reset_done"),
    url(r'^reset/password/$', password_reset, name="password_reset"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name="password_reset_confirm"),
    url(r'^reset/done/$', password_reset_complete, name="password_reset_complete"),


]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
                
urlpatterns += staticfiles_urlpatterns()
