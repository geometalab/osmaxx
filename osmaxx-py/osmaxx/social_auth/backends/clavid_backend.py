from urllib import parse as urlparse
from social.backends.open_id import OpenIdAuth
from social.exceptions import AuthMissingParameter


class ClavidComOpenId(OpenIdAuth):
    """clavid.com OpenID authentication backend"""
    name = 'clavid.com'

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super().get_user_details(response)
        values['username'] = values.get('username') or \
            urlparse.urlsplit(response.identity_url).netloc.split('.', 1)[0]
        return values

    def openid_url(self):
        """Returns clavid.com authentication URL"""
        if not self.data.get('openid_user'):
            raise AuthMissingParameter(self, 'openid_user')
        return 'http://%s.clavid.com' % self.data['openid_user']


class ClavidChOpenId(OpenIdAuth):
    """clavid.ch OpenID authentication backend"""
    name = 'clavid.ch'

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super().get_user_details(response)
        values['username'] = values.get('username') or \
            urlparse.urlsplit(response.identity_url).netloc.split('.', 1)[0]
        return values

    def openid_url(self):
        """Returns clavid.ch authentication URL"""
        if not self.data.get('openid_user'):
            raise AuthMissingParameter(self, 'openid_user')
        return 'http://%s.clavid.ch' % self.data['openid_user']
