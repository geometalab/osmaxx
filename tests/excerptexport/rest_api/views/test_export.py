import os

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

PERMISSION_DENIED = 403
NOT_FOUND = 404
DELETED_SUCCESS = 204


def test_existing_file_is_kept_when_not_authenticated(output_file_with_file):
    client = APIClient()
    request_url = reverse(
        "excerptexport_api:export-detail",
        kwargs={"pk": output_file_with_file.export.id},
    )
    file_path = output_file_with_file.file.path
    assert os.path.exists(file_path)
    response = client.delete(request_url, format="json")
    assert response.status_code == PERMISSION_DENIED
    assert os.path.exists(file_path)


def test_existing_file_is_deleted_when_authenticated(
    output_file_with_file, frontend_accessible_authenticated_api_client
):
    request_url = reverse(
        "excerptexport_api:export-detail",
        kwargs={"pk": output_file_with_file.export.id},
    )
    file_path = output_file_with_file.file.path
    assert os.path.exists(file_path)
    response = frontend_accessible_authenticated_api_client.delete(
        request_url, format="json"
    )
    assert response.status_code == DELETED_SUCCESS
    assert not os.path.exists(file_path)


def test_existing_file_is_kept_when_access_is_denied(
    output_file_with_file, authenticated_api_client
):
    request_url = reverse(
        "excerptexport_api:export-detail",
        kwargs={"pk": output_file_with_file.export.id},
    )
    file_path = output_file_with_file.file.path
    assert os.path.exists(file_path)
    response = authenticated_api_client.delete(request_url, format="json")
    assert response.status_code == PERMISSION_DENIED
    assert os.path.exists(file_path)


def test_export_is_deleted_without_attached_output_file(
    export, frontend_accessible_authenticated_api_client
):
    assert not hasattr(export, "output_file")
    request_url = reverse("excerptexport_api:export-detail", kwargs={"pk": export.id})
    response = frontend_accessible_authenticated_api_client.delete(
        request_url, format="json"
    )
    assert response.status_code == DELETED_SUCCESS
