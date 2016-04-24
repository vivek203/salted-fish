from django.conf.urls import url
from . import views


urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^populatedb/$', views.populate_db, name='populate_db'),
]