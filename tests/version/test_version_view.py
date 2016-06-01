def test_version_view(client):
    from django.core.urlresolvers import reverse
    import subprocess
    response = client.get(reverse('version:version'))
    assert response.status_code == 200
    import osmaxx
    assert osmaxx.__version__ in str(response.content)
    assert subprocess.check_output(["git", "describe", "--dirty"]).strip().decode() in str(response.content)
