# Contribuindo para o NL-Agent Framework

Obrigado por considerar contribuir! Este guia descreve práticas e convenções do projeto.

---

## 📋 Pré-requisitos

| Ferramenta | Versão Mínima |
|------------|---------------|
| Python     | 3.10          |
| Node.js    | 18 LTS        |
| Git        | 2.30          |

## 🚀 Setup Inicial

```bash
# 1. Clone o repositório
git clone https://github.com/nlagent/fw.git
cd fw

# 2. Instale dependências
make install

# 3. Configure pre-commit hooks
pip install pre-commit
pre-commit install
```

## 🏗️ Estrutura do Projeto

```
framework_agentnl/
├── config/              # Configurações YAML (bridge, agentes)
├── src/
│   ├── core/            # Módulos Python + TypeScript centrais
│   └── apps_script/     # Módulos Google Apps Script (IIFE)
├── tests/               # Testes (pytest + vitest)
├── docs/                # Documentação complementar
├── pyproject.toml       # Config Python (deps, ruff, mypy, pytest)
├── package.json         # Config Node (deps, eslint, prettier, vitest)
└── tsconfig.json        # Config TypeScript
```

## ✅ Antes de Submeter um PR

Execute **todas** as verificações localmente:

```bash
# Verificação completa (recomendado)
make lint           # Ruff (Python) + ESLint (JS)
make test           # Pytest + Vitest
make audit          # Assertion Agent (robustez)
make format         # Auto-formatação

# Ou via pre-commit (roda tudo de uma vez)
pre-commit run --all-files
```

## 📝 Convenções de Código

### Python
- **Formatter**: Ruff (88 colunas)
- **Linter**: Ruff com regras `E, F, I, N, W, D, UP, B, SIM, RUF`
- **Types**: Inline type hints obrigatórios (PEP 484 / PEP 604)
- **Docstrings**: Google style, obrigatórias para classes e funções públicas
- **Imports**: Agrupados por stdlib → third-party → local (Ruff cuida disso)

### JavaScript (Google Apps Script)
- **Padrão**: IIFE (`const Módulo = (function() {...})()`)
- **Variáveis**: `var` no escopo IIFE (compatibilidade V8 do GAS)
- **JSDoc**: Obrigatório em todas as funções públicas
- **Nomes**: Português para API pública, inglês para internos

### TypeScript
- **Strict mode**: Ativado (`"strict": true`)
- **Exports**: Tipos via `export type`, funções via `export`
- **Interfaces**: Preferir `interface` sobre `type` para objetos

## 🔀 Convenções de Git

### Branches
```
feature/nome-descritivo
fix/descricao-do-bug
docs/o-que-mudou
refactor/modulo-alterado
```

### Commits (Conventional Commits)
```
feat: adicionar suporte a protocolo ANP
fix: corrigir perda semântica em tradução ACP→MCP
docs: atualizar diagrama de arquitetura
refactor: extrair NLReasoner para módulo independente
test: adicionar cobertura para oracle_query
chore: atualizar dependências de dev
```

## 🧪 Testes

- Cada módulo Python em `src/core/` deve ter um `test_<módulo>.py` correspondente em `tests/`
- Cobertura mínima recomendada: **80%**
- Use fixtures do pytest para dados compartilhados

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.
