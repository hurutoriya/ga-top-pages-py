# Target source file
SOURCE_FILES=src

.PHONY: install
install: ## Install dependency
	rye sync

.PHONY: lint
lint: ## Run linter
	rye run ruff $(SOURCE_FILES)

.PHONY: fmt
fmt: ## Run formatter
	rye run black $(SOURCE_FILES)
	rye run ruff check ${SOURCE_FILES} --fix-only --exit-zero

# ref: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Generate this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'