from urllib import parse as urlparse
from social.backends.open_id import OpenIdAuth
from social.exceptions import AuthMissingParameter


class ClavidAbstractBaseOpenId(OpenIdAuth):
    openID_url = None

    def __init__(self, *args, **kwargs):
        assert type(self) is not ClavidAbstractBaseOpenId
        assert self.openID_url is not None
        super().__init__(*args, **kwargs)

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super().get_user_details(response)
        values['username'] = values.get('username') or \
            urlparse.urlsplit(response.identity_url).netloc.split('.', 1)[0]
        return values

    def openid_url(self):
        """Returns clavid authentication URL"""
        if not self.data.get('openid_user'):
            raise AuthMissingParameter(self, 'openid_user')
        return 'http://%s.%s' % (self.data['openid_user'], self.openID_url)


class ClavidComOpenId(ClavidAbstractBaseOpenId):
    """clavid.com OpenID authentication backend"""
    name = 'clavid.com'
    openID_url = 'clavid.com'


class ClavidChOpenId(ClavidAbstractBaseOpenId):
    """clavid.ch OpenID authentication backend"""
    name = 'clavid.ch'
    openID_url = 'clavid.ch'
