import os

SECRET_KEY = os.getenv('SECRET_KEY', 'aeghu0an0Ben9zai5Etae1eid2xoh,Ge')
WHITELIST_IP = (
    '127.0.0.1',
    '188.227.75.70',
    '188.227.75.56',
    '5.200.35.203',
    '78.140.220.147',
    '95.213.131.210',
)

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
