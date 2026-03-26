# Colors for help system
BLUE := \033[36m
YELLOW := \033[33m
GREEN := \033[32m
RESET := \033[0m

.DEFAULT_GOAL := help

##@ General
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\n$(BLUE)Usage:$(RESET)\n  make $(YELLOW)<target>$(RESET)\n"} \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2 } \
		/^##@/ { printf "\n$(GREEN)%s$(RESET)\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.PHONY: test-cov
test-cov: ## Run UNIT tests with strict coverage (Fail under 80%, excludes UI tests)
	@echo "$(GREEN)Running Unit Tests with Coverage Check...$(RESET)"
	uv run pytest -m "not integration" \
		--ignore=tests/test_sprint3_feed_ui.py \
		--cov=school_hub \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-fail-under=80

.PHONY: test-cov-simple
test-cov-simple: ## Run UNIT tests with simple console coverage report (shows missing lines)
	@echo "$(GREEN)Running Unit Tests with Simple Coverage Report...$(RESET)"
	uv run pytest -m "not integration" \
		--ignore=tests/test_sprint3_feed_ui.py \
		--cov=school_hub \
		--cov-report=term-missing \
		--cov-fail-under=0
