backend_dir = backend
frontend_dir = frontend

.PHONY: lint front-lint

backend-lint:
	uv run --directory $(backend_dir) --active ruff check --fix

mypy:
	uv run --directory $(backend_dir) --active mypy .

front-lint:
	npm run --prefix $(frontend_dir) lint:eslint && npm run --prefix $(frontend_dir) lint:stylelint && npm run --prefix $(frontend_dir) lint:prettier

all-done:
	@echo "ALL DONE!"

lint: backend-lint mypy front-lint all-done
