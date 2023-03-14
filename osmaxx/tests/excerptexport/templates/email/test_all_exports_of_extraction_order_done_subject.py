from django.template.loader import render_to_string


def test_some_success_some_failed(rf, extraction_order, exports):
    successful_exports = exports[::2]
    failed_exports = exports[1::2]

    view_context = dict(
        extraction_order=extraction_order,
        successful_exports=successful_exports,
        failed_exports=failed_exports,
        request=rf.get('/foo/bar'),
    )
    email_body = render_to_string(
        'excerptexport/email/all_exports_of_extraction_order_done_body.txt',
        context=view_context,
    ).strip()
    expected_body = '\n'.join(
        [
            'This is an automated email from testserver',
            '',
            'The extraction order #{order_id} "Neverland" has been processed and is available for download:',
            '- Esri Shapefile',
            '- SpatiaLite',
            '- OSM Protocolbuffer Binary Format',
            '',
            'Unfortunately, the following exports have failed:',
            '- GeoPackage',
            '- Garmin navigation &amp; map data',
            '',
            'Please order them anew if you need them. '
            'If there are repeated failures, '
            'please report them on https://github.com/geometalab/osmaxx/issues '
            'unless the problem is already known there.',
            '',
            'View the complete order at http://testserver/exports/ (login required)',
            '',
            'Thank you for using OSMaxx.',
            'The team at Geometa Lab HSR',
            'geometalab@hsr.ch',
        ]
    ).format(
        order_id=extraction_order.id,
    )
    assert email_body == expected_body


def test_some_success_1_failed(rf, extraction_order, exports):
    successful_exports = exports[:-1]
    failed_exports = exports[-1:]

    view_context = dict(
        extraction_order=extraction_order,
        successful_exports=successful_exports,
        failed_exports=failed_exports,
        request=rf.get('/foo/bar'),
    )
    email_body = render_to_string(
        'excerptexport/email/all_exports_of_extraction_order_done_body.txt',
        context=view_context,
    ).strip()
    expected_body = '\n'.join(
        [
            'This is an automated email from testserver',
            '',
            'The extraction order #{order_id} "Neverland" has been processed and is available for download:',
            '- Esri Shapefile',
            '- GeoPackage',
            '- SpatiaLite',
            '- Garmin navigation &amp; map data',
            '',
            'Unfortunately, the following export has failed:',
            '- OSM Protocolbuffer Binary Format',
            '',
            'Please order it anew if you need it. '
            'If there are repeated failures, '
            'please report them on https://github.com/geometalab/osmaxx/issues '
            'unless the problem is already known there.',
            '',
            'View the complete order at http://testserver/exports/ (login required)',
            '',
            'Thank you for using OSMaxx.',
            'The team at Geometa Lab HSR',
            'geometalab@hsr.ch',
        ]
    ).format(
        order_id=extraction_order.id,
    )
    assert email_body == expected_body


def test_no_success_1_failed(rf, extraction_order, exports):
    successful_exports = tuple()
    failed_exports = exports

    view_context = dict(
        extraction_order=extraction_order,
        successful_exports=successful_exports,
        failed_exports=failed_exports,
        request=rf.get('/foo/bar'),
    )
    email_body = render_to_string(
        'excerptexport/email/all_exports_of_extraction_order_done_body.txt',
        context=view_context,
    ).strip()
    expected_body = '\n'.join(
        [
            'This is an automated email from testserver',
            '',
            'The extraction order #{order_id} "Neverland" has been processed.',
            '',
            'Unfortunately, the following exports have failed:',
            '- Esri Shapefile',
            '- GeoPackage',
            '- SpatiaLite',
            '- Garmin navigation &amp; map data',
            '- OSM Protocolbuffer Binary Format',
            '',
            'Please order them anew if you need them. '
            'If there are repeated failures, '
            'please report them on https://github.com/geometalab/osmaxx/issues '
            'unless the problem is already known there.',
            '',
            'View the complete order at http://testserver/exports/ (login required)',
            '',
            'Thank you for using OSMaxx.',
            'The team at Geometa Lab HSR',
            'geometalab@hsr.ch',
        ]
    ).format(
        order_id=extraction_order.id,
    )
    assert email_body == expected_body
