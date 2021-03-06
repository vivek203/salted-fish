from django.conf.urls import url
from . import views


urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^populatewt/$', views.populate_full_water_temperature, name='populate_wt'),
     url(r'^populatewtc/$', views.populate_curr_water_temperature, name='populate_wtc'),
     url(r'^populatedch/$', views.populate_full_discharge, name='populate_dch'),
     url(r'^populatedc/$', views.populate_discharge, name='populate_dc'),
     url(r'^populatedgdd/$', views.populate_gdd_full, name='populate_gdd'),
     url(r'^calc_gdd/$', views.calc_gdd, name='calc_gdd'),
]