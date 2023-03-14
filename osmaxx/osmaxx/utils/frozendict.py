from types import MappingProxyType as dictproxy  # noqa


__all__ = [
    'frozendict',
]


# Using the recipe from https://pypi.python.org/pypi/dictproxyhack/1.1#usage
# We do this directly with MappingProxyType instead of using dictproxyhack, as we don't support Python < 3.3, anyway.
def frozendict(*args, **kwargs):
    return dictproxy(dict(*args, **kwargs))
