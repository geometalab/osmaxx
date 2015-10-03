#!/usr/bin/env python
import sys
import os
from jinja_helpers.render import render_to_string

sys.path.append(os.path.join(__file__))


def input_text(question, default=None):
    answer = input(question).strip()
    if answer == '' and default:
        return default
    return str(answer)


def input_int(question, default=None):
    try:
        answer = int(input(question).strip())
    except ValueError:
        print('please enter a valid number.')
        input_int(question, default)
    if answer == '' and default:
        return default
    return str(answer)


class InputChoice:
    def __init__(self, choices=None, default=None):
        self.VALID_CHOICES = choices
        self.result = None
        self.default = default

    def ask(self, question):
        answer = input(question).strip()
        if answer == '':
            if self.default and self.VALID_CHOICES[self.default]:
                return self.VALID_CHOICES[self.default]
        try:
            self.result = self.VALID_CHOICES[answer]
        except KeyError:
            print('Invalid Choice. Please choose out of the following:')
            print(', '.join(self.VALID_CHOICES.keys()))
            self.ask(question)
        return self.result


def yes_no(question, default=None):
    return InputChoice({'Y': True, 'y': True, 'N': False, 'n': False}, default).ask(question)


class OsmaxxDeployer(object):
    def __init__(self):
        # these are the default settings from Django, which are not production ready!
        self.settings = {
            'DJANGO_LOG_LEVEL': 'INFO',
        }

    def _general_questions(self):
        self.settings['APP_HOST'] = input_text('Which IP should the application listen? (0.0.0.0)', default='0.0.0.0')
        self.settings['APP_PORT'] = input_int('Which port should the application run on? (8000)', default=8000)
        if yes_no('Would you like to configure Email sending?'):
            self.settings.update(dict(
                DJANGO_EMAIL_BACKEND=input_text('EMAIL_BACKEND (django.core.mail.backends.smtp.EmailBackend): ',
                                                default='django.core.mail.backends.smtp.EmailBackend'),
                DJANGO_EMAIL_HOST=input_text('EMAIL_HOST (localhost): ', default='localhost'),
                DJANGO_EMAIL_HOST_PASSWORD=input_text('EMAIL_HOST_PASSWORD (""): ', default=''),
                DJANGO_EMAIL_HOST_USER=input_text('EMAIL_HOST_USER (""): ', default=''),
                DJANGO_EMAIL_PORT=input_int('EMAIL_PORT (25): ', default=25),
                DJANGO_EMAIL_USE_TLS=str(yes_no('EMAIL_USE_TLS (false): ', default='false')),
                DJANGO_EMAIL_USE_SSL=str(yes_no('EMAIL_USE_SSL (false): ', default='false')),
                DJANGO_DEFAULT_FROM_EMAIL=input_text('DEFAULT_FROM_EMAIL (no-reply@localhost): ',
                                                     default='no-reply@localhost'),
                DJANGO_SERVER_EMAIL=input_text('SERVER_EMAIL (no-reply@localhost): ', default='no-reply@localhost'),
            ))

    def _production_specific_questions(self):
        self.settings['production'] = True
        self.settings['DJANGO_ALLOWED_HOSTS'] = input_text(
            'which host(s) is it running on? \n'
            'HINT: use "*" for all, subdomain wildcard is a leading dot '
            '(e.g. ".example.org"), multiple values can be comma separated: ')
        self.settings['DJANGO_DEBUG'] = 'False'
        self.settings['DJANGO_X_FRAME_OPTIONS'] = 'SAMEORIGIN'

        if yes_no('is it using ssl? [Y/n] ', 'Y'):
            self.settings['ssl'] = True
            self.settings['DJANGO_SECURE_HSTS_SECONDS'] = input_int('HSTS_SECONDS duration in seconds (60): ', default=60)
            self.settings['DJANGO_SECURE_SSL_HOST'] = input_text(
                'which is the secured host? (e.g. osmaxx.hsr.ch): ')
            self.settings['DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS'] = str(yes_no(
                'Should HSTS include subdomains? [Y/n]: ', True))
        else:
            self.settings['ssl'] = False

    def _development_specific_questions(self):
        self.settings['production'] = False

    def start_questions(self):
        self._general_questions()
        if yes_no('are you setting up production? [Y/n]: '):
            self._production_specific_questions()
        else:
            self._development_specific_questions()

        return render_to_string('docker-compose.yml-template.jj2', self.settings)


if __name__ == '__main__':
    print(OsmaxxDeployer().start_questions())
