.PHONY: help

help:
	@grep -B1 -E "^[a-zA-Z0-9_-]+\:([^\=]|$$)" Makefile \
	| grep -v -- -- \
	| sed 'N;s/\n/###/' \
	| sed -n 's/^#: \(.*\)###\(.*\):.*/\2###\1/p' \
	| column -t -s '###'

#: Install poetry and fetch dependencies
install:
	pip install poetry and poetry env use 3.10; poetry install

#: Install dependencies
fetch-dependencies:
	poetry env use 3.10; poetry install

#: Lock dependencies
lock-dependencies:
	poetry env use 3.10; poetry lock

#: Start the API on port 8000
run:
	poetry env use 3.10; poetry run python topic_recommendations/api/main.py

#: Start test docker compose
start-docker:
	docker compose -f test_config/docker-compose-tests.yaml up -d

#: Stop test docker compose
stop-docker:
	docker compose -f test_config/docker-compose-tests.yaml down

#: Run all tests
tests:
	poetry env use 3.10; poetry run pytest

#: Show coverage
coverage:
	poetry env use 3.10; poetry run pytest --cov=topic_recommendations
