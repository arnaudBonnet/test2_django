from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def djangorocks(request):
    template = loader.get_template('apptwo/index.html')
    return HttpResponse(template.render({}, request))

