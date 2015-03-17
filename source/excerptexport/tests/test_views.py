from django.test import TestCase

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class ExcerptExportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')

    def test_new_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 302)

    def test_new(self):
        """
        When logged in, we get the excerpt choice form.
        """
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new excerpt')
