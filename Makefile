.PHONY: all help list _list_targets_on_separate_lines tests runtests-quick runtests-slow tox up-redis down-redis up-pg down-pg up-pg_translit down-pg_translit clean

all: help

help:
	@echo frequently used:
	@echo "\t"make tests"           "- run all tests
	@echo "\t"make runtests-quick"  "- run only quick tests
	@echo "\t"make runtests slow"   "- run only slow tests
	@echo
	@echo available targets:
	@$(MAKE) --no-print-directory _list_targets_on_separate_lines | sed -e 's/^/\t/'

list:
	@$(MAKE) --no-print-directory _list_targets_on_separate_lines | xargs

_list_targets_on_separate_lines:
    # Adopted from http://stackoverflow.com/a/26339924/674064
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	    awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	    sort | \
	    egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

tests: runtests-slow

runtests-quick: up-redis up-pg
	./runtests.py

runtests-slow: up-redis up-pg up-pg_translit
	./runtests.py --runslow

tox: up-redis up-pg up-pg_translit
	tox -e py34-flake8
	tox -e py34-django1.8-drf3.2
	tox -e py34-django1.9-drf3.2
	tox -e py34-django1.8-drf3.3
	tox -e py34-django1.9-drf3.3
	tox -e py34-slow-tests

up-redis:
	docker pull redis
	docker create -p "127.0.0.1:6379:6379" --name redis-local redis > /dev/null 2>&1 || true
	docker start redis-local > /dev/null 2>&1 || true

down-redis:
	docker stop redis-local > /dev/null 2>&1 && docker rm -vf redis-local > /dev/null 2>&1 || true

up-pg:
	docker pull geometalab/postgis-with-translit > /dev/null 2>&1
	docker run -d -p "127.0.0.1:54321:5432" -e POSTGRES_DB='postgres' --name pg_tests geometalab/postgis-with-translit > /dev/null 2>&1 \
	&& sleep 10 || docker start pg_tests > /dev/null 2>&1 && sleep 1

down-pg:
	docker stop pg_tests > /dev/null 2>&1 && docker rm -vf pg_tests > /dev/null 2>&1 || true

up-pg_translit:
	docker pull geometalab/postgis-with-translit > /dev/null 2>&1
	docker run -d -p "127.0.0.1:65432:5432" -e POSTGRES_DB='osmaxx_db' --name pg_translit geometalab/postgis-with-translit > /dev/null 2>&1\
	&& sleep 10 || docker start pg_translit > /dev/null 2>&1 && sleep 1

down-pg_translit:
	docker stop pg_translit > /dev/null 2>&1 && docker rm -vf pg_translit > /dev/null 2>&1 || true

clean: down-redis down-pg_translit down-pg
	find . -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -rf {} +
