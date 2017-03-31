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
            '- Esri File Geodatabase',
            '- GeoPackage',
            '- Garmin navigation &amp; map data',
            '',
            'Unfortunately, the following exports have failed:',
            '- Esri Shapefile',
            '- SpatiaLite',
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
