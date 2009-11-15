from datetime import datetime
import json
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.gis.feeds import Feed
from django.views.decorators.cache import cache_page
from django.template.defaultfilters import slugify
from ingestion.models import *
from ingestion.forms import *
from django.db.models import Count


def render_to_json(modelname, qs):
    interesting = {
        'layer' : ['id','status','size'],
        'layer' : ['name','provider','file_format']
        }
    j = {modelname:[]}
    for item in qs:
        d = {}
        for k in interesting[modelname]:
            d[k] = getattr(item,k)
            if modelname == 'layer':
                d['series_name'] = item.series.name
                d['series_id'] = item.series.id
        j[modelname].append(d)
    return HttpResponse(json.dumps(j), mimetype = "text/html")
    


def static(request, template):
    return render_to_response(template ,RequestContext(request,{}))


def upload_file(request):
    if request.method == 'POST':
        form = LayerAddForm(request.POST, request.FILES)
        print 'mp', form.is_multipart()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
    else:
        form = LayerAddForm()
    return render_to_response('upload.html', {'form': form})


def layer_edit(request, id):
    if request.method == 'POST':
        if id:
            op = layer.objects.get(pk=id)
            form = LayerAddForm(request.POST, instance=op)
        else:
            form = LayerAddForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        if id:
            op = layer.objects.get(pk=id)
            form = LayerAddForm(instance=op)
        else:
            form = LayerAddForm()
    return render_to_response("layer_create.html", RequestContext(request,{
        "form": form,
    }))    

    
def layer_create_or_edit(request, layer_id=''):
    if request.method == 'POST':
        if layer_id:
            op = get_object_or_404(Layer, pk=layer_id)
            form = LayerAddForm(request.POST, instance=op)
        else:
            form = LayerAddForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.date_uploaded_utc = datetime.utcnow()
            p.uploader = request.user
            p.save()
            return HttpResponseRedirect('./create/success/')

    else:
        if layer_id: 
            op = get_object_or_404(Layer, pk=layer_id)
            #pass this to template so it gets highlighted
            form = LayerAddForm(instance=op)
        else:
            form = LayerAddForm()
    return render_to_response("layer_create.html", RequestContext(request,{
        "form": form,
    }))
    
def list_view(request, model, id=''):
    modelname = model._meta.module_name
    ds = model.objects.all()
    format = request.GET.get('format','')
    if format == 'json':
        return render_to_json(modelname, ds)
    return render_to_response('%s_list.html' % modelname, RequestContext(request,{
        'object_list' : ds}))

def detail_view(request, model, id=''):
    modelname = model._meta.module_name
    ds = model.objects.get(pk=id)
    return render_to_response('%s_detail.html' % modelname, RequestContext(request,{
        'obj' : ds}))
