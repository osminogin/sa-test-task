import os

SECRET_KEY = os.getenv('SECRET_KEY', 'aeghu0an0Ben9zai5Etae1eid2xoh,Ge')
YADISK_TOKEN = os.getenv('YADISK_TOKEN')    # Required
YADISK_CALLDATA = os.getenv('YADISK_CALLDATA',
                            '/speechanalytics-connect/meta/calls-info.csv')
WHITELIST_IPS = os.getenv('WHITELIST_IPS', '').split(',') or (
    '127.0.0.1',
    '188.227.75.70',
    '188.227.75.56',
    '5.200.35.203',
    '78.140.220.147',
    '95.213.131.210',
)
WHITELIST_URLS = (r'/ping', r'/health',)
FIREWALL_ENABLED = os.getenv('FIREWALL_ENABLED', False)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s:%(lineno)d - %(message)s'  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'asyncio': {
            'level': 'WARNING',
            'propagate': True,
        },
        'asyncio_redis': {
            'level': 'WARNING',
            'propagate': True,
        },
    }
}
