from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from excerptexport.models import ExtractionOrder
from excerptexport.models import Excerpt
from excerptexport.models import BoundingGeometry
from excerptexport import settings


def index(request):
    return HttpResponse(loader.get_template('excerptexport/templates/index.html').render(RequestContext(request, {})))


class NewExcerptExportViewModel:
    def __init__(self, user):
        self.user = user
        self.personal_excerpts = Excerpt.objects.filter(is_active=True, is_public=False, owner=user) #.order_by('name')
        self.public_excerpts = Excerpt.objects.filter(is_active=True, is_public=True) #.order_by('name')

        self.administrative_areas = settings.ADMINISTRATIVE_AREAS
        self.export_options = settings.EXPORT_OPTIONS

    def get_context(self):
        return self.__dict__


@login_required(login_url='/admin/')
def new_excerpt_export(request):
    view_model = NewExcerptExportViewModel(request.user)
    return render(request, 'excerptexport/templates/new_excerpt_export.html', view_model.get_context())


@login_required(login_url='/admin/')
def create_excerpt_export(request):
    if request.POST['form-mode'] == 'existing_excerpt':
        existingExcerptID = request.POST['existing_excerpt.id']
        viewContext = { 'excerpt': existingExcerptID }
        ExtractionOrder.objects.create(
            excerpt_id = existingExcerptID,
            orderer = request.user
        )

    if request.POST['form-mode'] == 'create_new_excerpt':
        excerpt = Excerpt(
            name = request.POST['new_excerpt.name'],
            is_active = True,
            is_public = request.POST['new_excerpt.is_public'] if ('new_excerpt.is_public' in request.POST) else False
        )
        excerpt.owner = request.user
        excerpt.save()

        bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(
            request.POST['new_excerpt.boundingBox.north'],
            request.POST['new_excerpt.boundingBox.east'],
            request.POST['new_excerpt.boundingBox.south'],
            request.POST['new_excerpt.boundingBox.west']
        )
        bounding_geometry.excerpt = excerpt
        bounding_geometry.save()

        viewContext = { 'excerpt': excerpt, 'bounding_geometry': bounding_geometry }
        ExtractionOrder.objects.create(
            excerpt = excerpt,
            orderer = request.user
        )

    viewContext['use_existing'] = 'existingExcerptID' in vars() # TODO: The view should not have to know
    viewContext['options'] = get_export_options(request.POST, settings.EXPORT_OPTIONS)
    return render(request, 'excerptexport/templates/create_excerpt_export.html', viewContext)


def get_export_options(requestPostValues, optionConfig):
    # post values naming schema:
    # formats: "export_options.{{ export_option_key }}.formats"
    # options: "'export_options.{{ export_option_key }}.options.{{ export_option_config_key }}"
    export_options = {}
    for export_option_key, export_option in optionConfig.items():
        export_options[export_option_key] = {}
        export_options[export_option_key]['formats'] = requestPostValues.getlist('export_options.'+export_option_key+'.formats')

        for export_option_config_key, export_option_config in export_option['options'].items():
            export_options[export_option_key][export_option_config_key] = requestPostValues.getlist('export_options.'+export_option_key+'.options.'+export_option_config_key)

    return export_options
