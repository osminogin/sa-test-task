# Test task for SpeechAnalytics

[![](https://travis-ci.org/osminogin/sa-test-task.svg?branch=master)](https://travis-ci.org/osminogin/sa-test-task)

Test task.

Initially generated from [cookiecutter aiohttp uvloop](https://github.com/osminogin/cookiecutter-aiohttp-uvloop) project template.

Publicly available: [sa-test-task.herokuapp.com](https://sa-test-task.herokuapp.com/)

## Features

- Python 3.6, 3.7 support.
- Asyncio & aiohttp used.
- Gunicorn with UVloop event loop ([read why](http://magic.io/blog/uvloop-blazing-fast-python-networking/)).
- Pipenv for Python dependency management.
- Yandex.Disk async lib used.
- JSON schemas for input validation.
- JWT tokens used for auth.
- Heroku deployment support.
- Travis CI autobuilds.

## Getting started

Firstly set required environment variable:

```bash
export YADISK_TOKEN=...
```

Run production ready gunicorn server with uvloop:

```bash
make daemon
```

Or alternatively run devserver:

```bash
make dev
```

## Settings

This environment variables available:

SECRET_KEY - секретный ключ авторизации (по дефолту равен токену я.диска).
YADISK_TOKEN - единственный __обязательный параметр__.
YADISK_CALLDATA = путь до метаданных звонков на файловой системе я.диска,
    по дефолту равен '/speechanalytics-connect/meta/calls-info.csv')
WHITELIST_IPS = список разрешенных для доступа IP (используется в firewall middleware).
WHITELIST_URLS = список URL без авторизации (изначально /ping, /health).
FIREWALL_ENABLED = включение ограничения доступа по WHITELIST_IPS и WHITELIST_URLS
    (остальные запросы получают 403).

## License

See [LICENSE.md](https://github.com/osminogin/cookiecutter-aiohttp-helm/blob/master/LICENSE.md).
