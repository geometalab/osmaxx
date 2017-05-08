"""
Interface between OSMaxx frontend (Django-based web client) and the OSMaxx conversion service (mediator and worker).

This package holds shared code. All OSMaxx components (frontend & conversion service) may depend on it.
No code in this package may depend on other OSMaxx Django apps, especially not the component-specific ones.

The OSMaxx conversion service implementation (provided by the mediator) is located in Django app `conversion`,
not here in the package `conversion_api`.
"""
