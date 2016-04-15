from osmaxx.api_client import ConversionApiClient


def get_authenticated_api_client():
    """
    Helper method to get an authenticated ConversionApiClient instance.

    :return:
    """
    conversion_api_client = ConversionApiClient()
    return conversion_api_client
