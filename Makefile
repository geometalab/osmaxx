.PHONY: tests runtests-quick runtests-slow tox up-redis down-redis up-pg_translit down-pg_translit clean

tests: runtests-slow

runtests-quick: up-redis
	./runtests.py

runtests-slow: up-redis up-pg_translit
	./runtests.py --runslow

tox: up-redis
	tox -e py34-flake8
	tox -e py34-django1.8-drf3.2
	tox -e py34-django1.9-drf3.2
	tox -e py34-django1.8-drf3.3
	tox -e py34-django1.9-drf3.3

up-redis: down-redis
	docker pull redis
	docker run -d -p "127.0.0.1:6379:6379" --name redis-local redis

down-redis:
	docker stop redis-local && docker rm -vf redis-local || true

up-pg_translit: down-pg_translit
	docker pull geometalab/postgis-with-translit
	docker run -d -p "127.0.0.1:65432:5432" -e POSTGRES_DB='osmaxx_db' --name pg_translit geometalab/postgis-with-translit
	sleep 10

down-pg_translit:
	docker stop pg_translit && docker rm -vf pg_translit || true

clean: down-redis down-pg_translit
	find . -iname __pycache__ -exec rm -rf {} \;
	find . -iname "*.pyc" -exec rm -rf {} \;

