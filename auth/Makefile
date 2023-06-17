
PHONY: all
.DEFAULT_GOAL = help
.NOTPARALLEL: ; # Targets execute serially
.ONESHELL: ; # Recipes execute in the same shell


clean: ## Removes all build and test artifacts
	rm -f .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf reports
	rm -rf venv
	rm -f requirements.txt
	rm -rf $(SSAP_DIR)

dist-clean: clean ## Removes all build and test artifacts and virtual environment
	rm -rf .venv

build: ## Creates a virtual environment and installs development dependencies
	poetry install

test: ## Executes tests cases
	poetry run pytest

cover: ## Executes tests cases with coverage reports
	poetry run pytest

lint: ## Applies static analysis, checks and code formatting
	poetry run pre-commit run --all-files

ci-prebuild: ## Install build tools and prepare project directory for the CI pipeline
	pip install --disable-pip-version-check poetry
	cat /dev/null > requirements.txt

help: ## Show make target documentation
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)