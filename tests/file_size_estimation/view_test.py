from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class SizeEstimationViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('estimate_size_in_bytes-list')

    def test_size_estimation_returns_value(self):
        data = {"west": 1.0, "south": 2.0, "east": 3.0, "north": 4.0}
        expected_result = data.copy()
        expected_result.update({"estimated_file_size_in_bytes": 1166})

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)

    def test_size_estimation_returns_400_and_error_if_invalid_data_is_passed(self):
        data = {"west": 1.0, "south": 2.0, "east": 3.0, "north": -1.0}
        response = self.client.post(self.url, data, format='json')
        expected_result = {
            "non_field_errors": [
                "north must be greater than south"
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_result)
