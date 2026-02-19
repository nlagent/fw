# Política de Segurança — NL-Agent Framework

## 🔒 Versões Suportadas

| Versão | Suporte         |
|--------|-----------------|
| 1.x    | ✅ Ativo         |
| < 1.0  | ❌ Sem suporte   |

## 🐛 Reportando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, **NÃO** abra uma issue pública.

Em vez disso, envie um e-mail para: **contato@nlagent.ai**

Inclua:
1. Descrição da vulnerabilidade
2. Passos para reproduzir
3. Impacto potencial
4. Sugestão de correção (se houver)

**Prazo de resposta**: Até 48 horas úteis para confirmação de recebimento.

## 🛡️ Práticas de Segurança do Projeto

- Credenciais e chaves **nunca** são commitadas (ver `.gitignore`)
- Variáveis sensíveis devem usar `.env` (excluído do repositório)
- Dependências são auditadas periodicamente (`pip audit`, `npm audit`)
- Pre-commit hooks incluem `detect-private-key`
