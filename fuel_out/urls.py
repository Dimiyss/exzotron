from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.main, name='report.html'),
    url(r'^day/(?P<pk>)$',views.day_report,name='day_report'),

]