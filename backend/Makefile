# ---------- UTILS ---------
.PHONY: ssh
ssh:
	docker-compose exec backend bash

.PHONY: setup
setup:
	./scripts/setup.sh


.PHONY: install-dev
install-dev:
	poetry install --with dev


.PHONY: install-prod
install-prod:
	poetry install --with prod


.PHONY: pre-commit
pre-commit: poetry run pre-commit run --all-files


# ---------- DJANGO ----------
.PHONY: migrations
migrations:
	poetry run python app/manage.py makemigrations


.PHONY: migrate
migrate:
	poetry run python app/manage.py migrate


.PHONY: shell
shell:
	poetry run python app/manage.py shell


.PHONY: run-api
run-api:
	cd app && poetry run python manage.py runserver 0.0.0.0:8000


.PHONY: run-api-prod
run-api-prod:
	cd app && poetry run uvicorn core.asgi:application --host 0.0.0.0 --port 8000


# ---------- CELERY ----------
.PHONY: run-celery
run-celery:
	cd app && celery -A core worker -l INFO


# .PHONY: run-celery-beat
# run-celery-beat:
# 	cd app && celery -A core beat -l INFO


# .PHONY: run-celery-flower
# run-celery-flower:
# 	cd app && celery -A core flower --port=5555


# ---------- KAFKA ----------
.PHONY: run-asset-daily-kafka-consumer
run-asset-daily-kafka-consumer:
	cd app && poetry run python manage.py start_homebroker_kafka_consumer asset_daily


# ---------- QUALITY ----------
.PHONY: test
test:
	poetry run pytest app/


.PHONY: coverage
coverage:
	poetry run pytest app/ -v -n auto --html=test_report/test-report.html --cov=app/ --cov-report=html


.PHONY: lint
lint:
	poetry run ruff check


.PHONY: format
format:
	poetry run ruff format


.PHONY: format-check
format-check:
	poetry run ruff format --check


# ---------- CLEAN UP ----------
# Remove build artifacts
.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


# Remove Python file artifacts
.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


# Remove test and coverage artifacts
.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr test_report/


# Remove all build, test, coverage and Python artifacts
.PHONY: clean
clean: clean-build clean-pyc clean-test
