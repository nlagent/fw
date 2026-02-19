# ============================================================================
# Makefile — NL-Agent Framework
# Automação de tarefas: install, lint, format, test, audit, CI local.
# ============================================================================

.PHONY: help install audit test lint format clean ci typecheck hooks

# ─── Default ─────────────────────────────────────────────────────────────

help:  ## Mostra esta ajuda
	@echo ""
	@echo "🧠 NL-Agent Framework — Comandos Disponíveis"
	@echo "═══════════════════════════════════════════════"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ─── Setup ───────────────────────────────────────────────────────────────

install:  ## Instala dependências (Python + JS)
	pip install -e ".[dev]"
	npm install

hooks:  ## Instala pre-commit hooks
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks instalados."

# ─── Qualidade de Código ────────────────────────────────────────────────

lint:  ## Verifica qualidade (Ruff + ESLint)
	ruff check src/ tests/
	npm run lint

format:  ## Auto-formata código (Ruff + Prettier)
	ruff format src/ tests/
	ruff check --fix src/ tests/
	npm run format

typecheck:  ## Verificação de tipos (mypy + tsc)
	mypy src/core/ --config-file pyproject.toml
	npm run check-types

# ─── Testes ──────────────────────────────────────────────────────────────

test:  ## Executa todos os testes (Pytest + Vitest)
	pytest tests/ -v --tb=short
	npm test

test-cov:  ## Testes com relatório de cobertura
	pytest tests/ -v --tb=short --cov=src --cov-report=term-missing --cov-report=html
	@echo "📊 Relatório HTML em: htmlcov/index.html"

# ─── Auditoria ──────────────────────────────────────────────────────────

audit:  ## Executa Assertion Agent (robustez)
	python src/core/assertion_agent.py

# ─── CI Local ────────────────────────────────────────────────────────────

ci: lint typecheck test audit  ## Pipeline CI completo (lint → types → test → audit)
	@echo ""
	@echo "✅ Pipeline CI local concluído com sucesso."

# ─── Limpeza ─────────────────────────────────────────────────────────────

clean:  ## Remove artefatos temporários
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
	rm -rf htmlcov .coverage coverage.xml
	rm -rf node_modules dist *.egg-info build
	rm -f robustness_report.json
	@echo "🧹 Artefatos removidos."
