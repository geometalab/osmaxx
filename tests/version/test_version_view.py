def test_version_view(client):
    from django.urls import reverse

    response = client.get(reverse("osmaxx.version:version"))
    assert response.status_code == 200
    import osmaxx

    assert osmaxx.__version__ in str(response.content)
    # removed: we don't include git in the docker images anymore.
    # TODO: find another solution to provide more accurate version information
    assert 'actual_version' not in str(response.content)
