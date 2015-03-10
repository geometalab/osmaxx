from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from excerptexport.models import Excerpt
from excerptexport.models import BoundingGeometry
from django.contrib.auth.models import User
from pprint import pprint


def index(request):
    return HttpResponse(loader.get_template('templates/excerptexport/index.html').render(RequestContext(request, {})))


class NewExcerptExportViewModel:
    def __init__(self, user):
        self.user = user
        self.personal_excerpts = Excerpt.objects.filter(is_active=True, is_public=False, owner=user) #.order_by('name')
        self.public_excerpts = Excerpt.objects.filter(is_active=True, is_public=True) #.order_by('name')

        # TODO: move to settings or read from file
        self.administrative_areas = {
            'regions': {
                'eu': 'Europe', 'af': 'Africa'
            },
            'countries': {
                'ch': 'Switzerland', 'de': 'Germany', 'us': 'USA'
            }
        }

    def get_context(self):
        return self.__dict__


@login_required(login_url='/admin/')
def new_excerpt_export(request):
    view_model = NewExcerptExportViewModel(request.user)
    return render(request, 'templates/excerptexport/new_excerpt_export.html', view_model.get_context())


@login_required(login_url='/admin/')
def create_excerpt_export(request):
    excerpt = Excerpt(
        name = request.POST['excerpt.name'],
        is_active = True,
        is_public = request.POST['excerpt.isPublic'] if ('excerpt.isPublic' in request.POST) else False
    )
    excerpt.owner = request.user
    excerpt.save()

    bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(
        request.POST['excerpt.boundingBox.north'],
        request.POST['excerpt.boundingBox.east'],
        request.POST['excerpt.boundingBox.south'],
        request.POST['excerpt.boundingBox.west']
    )
    bounding_geometry.excerpt = excerpt
    bounding_geometry.save()

    return render(request, 'templates/excerptexport/create_excerpt_export.html', { 'excerpt': excerpt, 'bounding_geometry': bounding_geometry })