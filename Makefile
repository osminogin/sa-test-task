PYTHON := $(shell /usr/bin/env pipenv --py)
DOCKER ?= $(shell /usr/bin/env docker 2> /dev/null)
APP := speechanalytics_api
VERSION ?= $(strip $(shell cat VERSION))
COMMIT = $(strip $(shell git rev-parse --short HEAD))
BUILD_DATE = $(strip $(shell date -u +"%Y-%m-%dT%H:%M:%SZ"))
TAG ?= latest
IMAGE ?= $(APP):$(TAG)

default: dev

daemon:
	@echo "Running async daemon on 0.0.0.0:8000 ..."
	@pipenv run gunicorn speechanalytics_api:app --bind 0.0.0.0:8000 \
		--worker-class aiohttp.worker.GunicornUVLoopWebWorker \
		--workers=2 \
		--worker-tmp-dir /dev/shm \
		--log-file=-

dev:
	@$(PYTHON) -m aiohttp.web -H localhost -P 8081 speechanalytics_api:build_app

tests:
	@$(PYTHON) -m pytest

analysis:
	@echo "Starting static analysis ..."
	@cd $(APP)
	@-pipenv run flake8
	@-pipenv run pylint --rcfile setup.cfg .
	@-pipenv run isort --check

build:
	@echo Building container ...
	@docker build --tag $(IMAGE) \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		--build-arg VCS_REF=$(COMMIT) \
		--build-arg VERSION=$(VERSION)\
		.

token:
	@echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.19X7kKD-m0ImEdCIeDzitU10IQLQIhTkGA55FOaLUhs"

deps:
	@docker-compose up postgres redis	# pgadmin4

.PHONY: default daemon tests build analysis dev token
