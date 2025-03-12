.PHONY: all production test docs clean

COMPOSE = $(shell if docker compose version >/dev/null 2>&1; then echo " compose"; else echo "-compose"; fi)

all: production

production:
	@true

docs:
	tox -c tests/tox.ini -e docs

dev: $(LOCAL_CONFIG_DIR) $(LOGS_DIR) install-hooks

install-hooks:
	pre-commit install -f --install-hooks

test:
	tox -c tests/tox.ini

test-elasticsearch:
	tox -c tests/tox.ini -- --runelasticsearch

test-docker:
	$(shell echo docker$(COMPOSE)) -f tests/docker-compose.yml --project-name elastalert build tox
	$(shell echo docker$(COMPOSE)) -f tests/docker-compose.yml --project-name elastalert run --rm tox \
		tox -c tests/tox.ini -- $(filter-out $@,$(MAKECMDGOALS))

clean:
	make -C docs clean
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf virtualenv_run tests/.tox tests/.coverage *.egg-info docs/build

%:
	@:
