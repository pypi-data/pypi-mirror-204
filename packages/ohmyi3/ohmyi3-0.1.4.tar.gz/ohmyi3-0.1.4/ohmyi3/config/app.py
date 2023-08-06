from uvicore.configuration import env
from uvicore.typing import OrderedDict

# Running application configuration.
# This config only applies if this package is running as the main application.
# Accessible at config('app')

config = {
    'name': 'Ohmyi3 Configuration Manager',
    'main': 'ohmyi3',
    'debug': False,
    'packages': OrderedDict({
        'ohmyi3': {
            'provider': 'ohmyi3.services.ohmyi3.Ohmyi3',
        },
    }),
    'logger': {
        'console': {
            'enabled': True,
            'level': 'INFO',
            'colors': True,
        },
    },
}
