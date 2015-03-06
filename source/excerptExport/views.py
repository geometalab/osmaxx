from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from excerptExport.models import Excerpt
from excerptExport.models import BoundingGeometry
from django.contrib.auth.models import User
from pprint import pprint


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
    excerpt = Excerpt(
        name = request.POST['excerpt.name'],
        is_active = True,
        is_public = request.POST['excerpt.isPublic']
    )
    
    # TODO: Replace by current user
    excerpt.owner = User.objects.filter(username="test", is_active=True)[0]
    excerpt.save()

    bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(
        request.POST['excerpt.boundingBox.north'],
        request.POST['excerpt.boundingBox.east'],
        request.POST['excerpt.boundingBox.south'],
        request.POST['excerpt.boundingBox.west']
    )
    bounding_geometry.excerpt = excerpt
    bounding_geometry.save()

    return render(request, 'templates/excerptExport/export.html', { 'excerpt': excerpt, 'bounding_geometry': bounding_geometry })