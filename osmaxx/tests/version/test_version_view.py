def test_version_view(client):
    from django.urls import reverse

    response = client.get(reverse("osmaxx.version:version"))
    assert response.status_code == 200
    import osmaxx

    assert osmaxx.__version__ in str(response.content)
    assert 'actual_version' not in str(response.content)
    assert 'osmaxx' in str(response.content)
    assert '5' in str(response.content)
