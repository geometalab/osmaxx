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

.PHONY: local_dev_env
local_dev_env: compose-env/common.env compose-env/frontend.env compose-env/mediator.env compose-env/worker.env
	@echo
	@echo "\tIf you haven't already, you might want to "'`source activate_local_development`', now.

compose-env/common.env: compose-env-dist/common.env
	@mkdir -p $(@D)
	sed -e 's/^\(DJANGO_OSMAXX_CONVERSION_SERVICE_\(USERNAME\|PASSWORD\)=\)/\1dev/' < $< > $@

PUBLIC_LOCALHOST_IP := $(shell ip route get 1 | awk '{print $$NF;exit}')

compose-env/frontend.env: compose-env-dist/frontend.env
	@mkdir -p $(@D)
# We don't have to set DJANGO_SECRET_KEY here, as docker-compose-dev.yml sets it for local use.
	sed -e 's/^\(DJANGO_EMAIL_\)/# \1/' \
	    -e 's/^\(DJANGO_ALLOWED_HOSTS=\)/\1$(PUBLIC_LOCALHOST_IP)/' \
	    < $< \
	    > $@

compose-env/%.env: compose-env-dist/%.env
	@mkdir -p $(@D)
# We don't have to set DJANGO_SECRET_KEY here, as docker-compose-dev.yml sets it for local use.
	cp $< $@

.PHONY: tests-quick
tests-quick: up-redis up-pg
	./runtests.py $(PYTEST_ARGS)

.PHONY: tests-all
tests-all: up-redis up-pg up-pg_translit
	./runtests.py $(PYTEST_ARGS) --runslow

.PHONY: tox
tox: up-redis up-pg up-pg_translit
	tox -e py34-flake8
	tox -e py34-django1.8-drf3.2
	tox -e py34-django1.9-drf3.2
	tox -e py34-django1.8-drf3.3
	tox -e py34-django1.9-drf3.3
	tox -e py34-slow-tests

.PHONY: up-redis
up-redis:
	docker pull redis  > /dev/null
	docker create -p "127.0.0.1:6379:6379" --name redis-local redis > /dev/null 2>&1 || true
	docker start redis-local > /dev/null 2>&1 || true
	./docker_entrypoint/wait-for-it/wait-for-it.sh 127.0.0.1:6379 -t 20

.PHONY: down-redis
down-redis:
	docker stop redis-local > /dev/null 2>&1 && docker rm -vf redis-local > /dev/null 2>&1 || true

.PHONY: up-pg
up-pg:
	docker pull geometalab/postgis-with-translit > /dev/null
	docker create -p "127.0.0.1:54321:5432" -e POSTGRES_DB='postgres' --name pg_tests geometalab/postgis-with-translit > /dev/null 2>&1 || true
	docker start pg_tests
	./docker_entrypoint/wait-for-it/wait-for-it.sh 127.0.0.1:54321 -t 20

.PHONY: down-pg
down-pg:
	docker stop pg_tests > /dev/null 2>&1 && docker rm -vf pg_tests > /dev/null 2>&1 || true

.PHONY: up-pg_translit
up-pg_translit:
	docker pull geometalab/postgis-with-translit > /dev/null
	docker create -p "127.0.0.1:65432:5432" -e POSTGRES_DB='osmaxx_db' --name pg_translit geometalab/postgis-with-translit > /dev/null 2>&1  || true
	docker start pg_translit
	./docker_entrypoint/wait-for-it/wait-for-it.sh 127.0.0.1:65432 -t 20

.PHONY: down-pg_translit
down-pg_translit:
	docker stop pg_translit > /dev/null 2>&1 && docker rm -vf pg_translit > /dev/null 2>&1 || true

.PHONY: clean
clean: down-redis down-pg_translit down-pg
	find . -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -rf {} +
