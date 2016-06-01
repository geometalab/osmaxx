def test_version_view(client):
    from django.core.urlresolvers import reverse
    response = client.get(reverse('version:version'))
    assert response.status_code == 200
    import osmaxx
    assert osmaxx.__version__ in str(response.content)
