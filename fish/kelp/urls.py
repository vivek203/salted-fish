from django.conf.urls import url
from . import views


urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^populatewt/$', views.populate_water_temperature, name='populate_wt'),
]