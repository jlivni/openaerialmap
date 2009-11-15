from django.conf.urls.defaults import *
from django.views.generic import list_detail
from ingestion.views import *
from ingestion.models import *



urlpatterns = patterns('',
    (r'^$', static, {'template':'index.html'}),
    
    (r'^layers/create/$', layer_create_or_edit),
    (r'^layers/create/success/$', static, {'template':'layer_create_success'}),
    (r'^layers/$', list_view, {'model' : Layer}),
    (r'^layers/status/(?P<status>[-\w]+)/$', list_view, {'model' : Layer}),
    (r'^layers/(?P<id>\d+)/edit/$', layer_create_or_edit),
    (r'^layers/(?P<id>\d+)/$', detail_view, {'model' : Layer}),

)
    
