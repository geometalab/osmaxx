import json

import pytest
from hamcrest import assert_that, contains_inanyorder as contains_in_any_order


@pytest.fixture
def extraction_configuration_with_formats():
    return {'gis_formats': ['txt', 'foobar'], 'gis_options': {'detail_level': 'standard'}}


@pytest.mark.django_db
def test_0019_forward(migrate, user, extraction_configuration_with_formats):
    old_apps = migrate('excerptexport', '0017_auto_20160310_1102')
    ExtractionOrder = old_apps.get_model('excerptexport', 'ExtractionOrder')  # noqa
    extraction_order = ExtractionOrder.objects.create(orderer_id=user.id)
    extraction_order._extraction_configuration = json.dumps(extraction_configuration_with_formats)
    extraction_order.save()
    extraction_order_id = extraction_order.id

    new_apps = migrate('excerptexport', '0019_one_export_per_file_format')
    ExtractionOrder = new_apps.get_model('excerptexport', 'ExtractionOrder')  # noqa
    extraction_order_after_migration = ExtractionOrder.objects.get(id=extraction_order_id)
    assert_that(
        extraction_order_after_migration.exports.values_list('file_format', flat=True), contains_in_any_order(
            'txt',
            'foobar',
        )
    )


@pytest.mark.django_db
def test_0019_backward(migrate, user, extraction_configuration_with_formats):
    old_apps = migrate('excerptexport', '0019_one_export_per_file_format')
    ExtractionOrder = old_apps.get_model('excerptexport', 'ExtractionOrder')  # noqa
    extraction_order = ExtractionOrder.objects.create(orderer_id=user.id)
    extraction_order._extraction_configuration = json.dumps({'gis_options': {'detail_level': 'standard'}})
    extraction_order.exports.create(file_format='txt')
    extraction_order.exports.create(file_format='foobar')
    extraction_order.save()
    extraction_order_id = extraction_order.id

    new_apps = migrate('excerptexport', '0017_auto_20160310_1102')
    ExtractionOrder = new_apps.get_model('excerptexport', 'ExtractionOrder')  # noqa
    extraction_order_after_migration = ExtractionOrder.objects.get(id=extraction_order_id)
    assert json.loads(extraction_order_after_migration._extraction_configuration) == extraction_configuration_with_formats
