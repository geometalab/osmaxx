.PHONY: all
all: help

.PHONY: help
help:
	@echo frequently used:
	@echo "\t"make tests-all"                                  "- run all test
	@echo "\t"make tests-quick"                                "- run only quick tests
	@echo Pass options to ./runtests.py or pytest by setting PYTEST_ARGS:
	@echo "\t"make tests-all PYTEST_ARGS=-ktest_label_water_l" "- run only a specific test
	@echo
	@echo available targets:
	@$(MAKE) --no-print-directory _list_targets_on_separate_lines | sed -e 's/^/\t/'

.PHONY: list
list:
	@$(MAKE) --no-print-directory _list_targets_on_separate_lines | xargs

.PHONY: _list_targets_on_separate_lines
_list_targets_on_separate_lines:
	# Adopted from http://stackoverflow.com/a/26339924/674064
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	    awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	    sort | \
	    egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

PIP_TOOLS_SOURCE_SPEC_FILES := requirements.in requirements-all.in
PIP_TOOLS_COMPILED_SPEC_FILES := $(PIP_TOOLS_SOURCE_SPEC_FILES:.in=.txt)

.PHONY: pip-upgrade
pip-upgrade: $(PIP_TOOLS_SOURCE_SPEC_FILES)
	PIP_COMPILE_FLAGS=--upgrade $(MAKE) --always-make $(PIP_TOOLS_COMPILED_SPEC_FILES)
	@echo
	@echo Updated compiled pip-tools spec files $<, but NOT INSTALLED, yet.
	@echo Consider running
	@echo "\t"make pip-sync-all
	@echo or
	@echo "\tpip-sync <compiled spec file> [<compiled spec file> ...]"
	@echo e.g.
	@echo "\t"pip-sync $(PIP_TOOLS_COMPILED_SPEC_FILES)
	@echo now.

.PHONY: pip-sync-all
pip-sync-all: requirements-all.txt
	pip-sync $?

%.txt: %.in
	pip-compile ${PIP_COMPILE_FLAGS} --output-file $@ $<

.PHONY: tests-quick
tests-quick: up-redis up-pg
	docker build --target worker -t worker:test -f Dockerfile .
	docker run --link pg_tests:postgres --link redis-local:redis -e DJANGO_DB_PORT=5432 -e DJANGO_DB_HOST=postgres -e DJANGO_SETTINGS_MODULE= -v "$$(pwd):/code" --rm worker:test bash -c 'cp -r /code /tmp/code && cd /tmp/code/ && ./runtests.py $(PYTEST_ARGS)'

.PHONY: tests-all
tests-all: up-redis up-pg up-pg_translit
	docker build --target worker -t worker:test -f Dockerfile .
	docker run --link pg_translit:translit --link pg_tests:postgres --link redis-local:redis  -e DJANGO_DB_PORT=5432 -e DJANGO_DB_HOST=postgres -e PG_TRANSLIT_PORT=5432 -e PG_TRANSLIT_HOST=translit -e DJANGO_SETTINGS_MODULE= -v "$$(pwd):/code" --rm worker:test bash -c 'cp -r /code /tmp/code && cd /tmp/code/ && ./runtests.py $(PYTEST_ARGS) --runslow'

.PHONY: tox
tox: up-redis up-pg up-pg_translit
	tox --skip-missing-interpreters

.PHONY: up-redis
up-redis:
	docker pull redis  > /dev/null
	docker create -p "127.0.0.1:6379:6379" --name redis-local redis > /dev/null 2>&1 || true
	docker start redis-local > /dev/null 2>&1 || true
	sleep 10

.PHONY: down-redis
down-redis:
	docker stop redis-local > /dev/null 2>&1 && docker rm -vf redis-local > /dev/null 2>&1 || true

.PHONY: up-pg
up-pg:
	docker pull geometalab/postgis-with-translit > /dev/null
	docker create -p "127.0.0.1:54321:5432" -e POSTGRES_DB='postgres' --name pg_tests geometalab/postgis-with-translit > /dev/null 2>&1 || true
	docker start pg_tests
	sleep 10

.PHONY: down-pg
down-pg:
	docker stop pg_tests > /dev/null 2>&1 && docker rm -vf pg_tests > /dev/null 2>&1 || true

.PHONY: up-pg_translit
up-pg_translit:
	docker pull geometalab/postgis-with-translit > /dev/null
	docker create -p "127.0.0.1:65432:5432" -e POSTGRES_DB='osmaxx_db' --name pg_translit geometalab/postgis-with-translit > /dev/null 2>&1  || true
	docker start pg_translit
	sleep 10

.PHONY: down-pg_translit
down-pg_translit:
	docker stop pg_translit > /dev/null 2>&1 && docker rm -vf pg_translit > /dev/null 2>&1 || true

.PHONY: clean
clean: down-redis down-pg_translit down-pg
	find . -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -rf {} +

LOCAL_RUN_ONCE_SERVICES := osmboundaries_importer osm-pbf-updater
LOCAL_DB_SERVICES := frontenddatabase mediatordatabase osmboundaries-database
LOCAL_APPLICATION_STACK := nginx frontend mediator worker worker-exclusive conversionserviceredis
LOCAL_DEPLOY_VERSION := latest
PUBLIC_LOCALHOST_IP := $(shell ip route get 1 | awk '{print $$NF;exit}')
COMPOSE := PUBLIC_LOCALHOST_IP=${PUBLIC_LOCALHOST_IP} DEPLOY_VERSION=${LOCAL_DEPLOY_VERSION} docker-compose

.PHONY: up_local_run_once
up_local_run_once: up_local_db
	${COMPOSE} up -d ${LOCAL_RUN_ONCE_SERVICES}

.PHONY: up_local_db
up_local_db:
	${COMPOSE} up -d ${LOCAL_DB_SERVICES}

.PHONY: up_local
up_local: up_local_db
	${COMPOSE} up -d ${LOCAL_APPLICATION_STACK}

.PHONY: up_local_all
up_local_all: build_local up_local_db up_local_run_once up_local

.PHONY: build_local
build_local:
	${COMPOSE} build --pull
