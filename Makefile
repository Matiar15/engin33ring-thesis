backend_dir = backend
frontend_dir = frontend

.PHONY: lint front-lint

backend-lint:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) ruff format

mypy:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) mypy .

tests:
	PYTHONPATH=$(shell pwd) uv run --directory $(backend_dir) pytest -v

front-lint:
	npm run --prefix $(frontend_dir) lint:eslint && npm run --prefix $(frontend_dir) lint:stylelint && npm run --prefix $(frontend_dir) lint:prettier

all-done:
	@echo "ALL DONE!"

lint: backend-lint mypy front-lint all-done
