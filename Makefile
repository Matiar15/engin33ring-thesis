backend_dir = backend
frontend_dir = frontend

.PHONY: lint front-lint

backend-lint:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) ruff format

mypy:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) mypy .

backend-test:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) pytest -v

front-lint:
	npm run --prefix $(frontend_dir) lint

frontend-test:
	npm run --prefix $(frontend_dir) test

frontend-install:
	npm i --prefix $(frontend_dir)

all-done:
	@echo "ALL DONE!"

lint: backend-lint mypy front-lint all-done

test: backend-test frontend-test all-done