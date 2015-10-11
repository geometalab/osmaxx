from osmaxx.excerptexport.models import Excerpt


def _get_active_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
            bounding_geometry_raw_reference__bboxboundinggeometry__isnull=False
        )


def own_private(user):
    return _get_active_excerpts().filter(is_public=False, owner=user)


def own_public(user):
    return _get_active_excerpts().filter(is_public=True, owner=user)


def other_public(user):
    return _get_active_excerpts().filter(is_public=True).exclude(owner=user)


def countries():
    return _get_active_excerpts().filter(
            bounding_geometry_raw_reference__osmosispolygonfilterboundinggeometry__isnull=False
        )


def get_existing_excerpt_choices_shortcut(user):
    return (
        ('Personal excerpts ({username})'.format(username=user.username),
            tuple(
                (excerpt.id, excerpt.name) for excerpt in own_private(user)
            )
        ),
        ('Personal public excerpts ({username})'.format(username=user.username),
            tuple(
                (excerpt.id, excerpt.name) for excerpt in own_public(user)
            )
        ),
        ('Other excerpts',
            tuple(
                (excerpt.id, excerpt.name) for excerpt in other_public(user)
            )
        ),
        ('Countries',
            tuple(
                (excerpt.id, excerpt.name) for excerpt in countries()
            )
        ),
    )
