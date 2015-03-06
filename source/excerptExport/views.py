from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from excerptExport.models import Excerpt
from django.contrib.auth.models import User


def index(request):
    return HttpResponse(loader.get_template('templates/excerptExport/index.html').render(RequestContext(request, {})))


class ListViewModel:
    def __init__(self):
        self.personal_excerpts = Excerpt.objects.filter(is_active=True, is_public=False) #.order_by('name')
        self.public_excerpts = Excerpt.objects.filter(is_active=True, is_public=True) #.order_by('name')

    def get_context(self):
        return self.__dict__


def list(request):
    view_model = ListViewModel()
    return render(request, 'templates/excerptExport/list.html', view_model.get_context())


def export(request):
    excerpt_name = request.POST['excerpt.name']
    excerpt = Excerpt()
    excerpt.is_active = True
    excerpt.name = excerpt_name
    excerpt.is_public = request.POST['excerpt.isPublic']

    return render(request, 'templates/excerptExport/export.html', { 'excerpt': excerpt })