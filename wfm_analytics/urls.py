from django.conf.urls import url
from wfm_analytics import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^analysis/(?P<startdate>\w+)/(?P<enddate>\w+)/(?P<chart_type>\w+)/(?P<depts_list>\w+)/$', views.analytics_page, name='analysispage'),
    url(r'^departmentalanalysis/$', views.departmentalanalysis, name='departmentalanalysis'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)