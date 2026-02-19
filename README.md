# 🧠 Framework NL-Agent

> **Interoperabilidade Semântica para Sistemas Multi-Agentes via Lógica Natural**
>
> Framework unificado que integra os protocolos **MCP** (Model Context Protocol), **A2A** (Agent-to-Agent), **ANP** (Agent Network Protocol) e **ACP** (Agent Communication Protocol) sob princípios de Lógica Natural (NL), mediados por oráculos epistêmicos baseados em LLMs/LRMs.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Protocolos Suportados](#protocolos-suportados)
- [Oráculos Epistêmicos](#oráculos-epistêmicos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Primeiros Passos](#primeiros-passos)
- [Métricas de Validação](#métricas-de-validação)
- [Casos de Uso](#casos-de-uso)
- [Heurísticas de Implementação](#heurísticas-de-implementação)
- [Anti-Padrões](#anti-padrões)
- [Referências Teóricas](#referências-teóricas)
- [Licença](#licença)

---

## Visão Geral

O **NL-Agent Framework** propõe uma camada de abstração semântica que unifica protocolos de comunicação entre agentes sob princípios fundamentais da **Lógica Natural (NL)**. Ele resolve o problema central da comunicação agêntica: como assegurar que intenções comunicadas permaneçam intactas perante diferenças ontológicas, incertezas contextuais e lacunas no conhecimento disponível.

### O Problema

A **infodemia** contemporânea sobrecarrega profissionais com dados fragmentados em "silos de inteligência". Na gestão educacional, isso se manifesta em:

- Sistemas isolados de matrícula, frequência e suprimentos
- Heterogeneidade ontológica (representações divergentes de conceitos)
- Ambiguidade contextual e incompletude epistêmica
- Ausência de padrões unificados para comunicação multi-agente

### A Solução

O framework implementa:

1. **Dualidade Cognitiva** — LLMs (System 1: rápido, intuitivo) + LRMs (System 2: lento, deliberativo)
2. **Mediação Oracular** — Oráculos epistêmicos baseados em LLMs para tradução semântica
3. **Tradução Semântica** — Algoritmo que preserva intenção original via transformações NL
4. **Isolamento Contextual** — Padrão IIFE como unidade básica de agência MCP

### Resultados Comprovados

| Métrica                         | Antes       | Depois        | Melhoria |
|---------------------------------|-------------|---------------|----------|
| Tempo de consolidação de dados  | 4–8 horas   | 15–30 minutos | **94%**  |
| Taxa de erro em prestação contas| 12%         | 0,3%          | **97%**  |
| Interoperabilidade semântica    | 42%         | 93,6%         | **123%** |
| Preservação semântica média     | 0,72        | 0,923         | **28%**  |

---

## Arquitetura

O framework organiza-se em **três camadas** interoperáveis:

```
┌──────────────────────────────────────────────────────────┐
│                   NL-AGENT FRAMEWORK                     │
├──────────────────────────────────────────────────────────┤
│  1. CAMADA DE INFERÊNCIA NL                              │
│     [ Reasoner ]  <->  [ Unifier ]  <->  [ Validator ]   │
│     (Inferência)      (Alinhamento)    (Consistência)    │
├──────────────────────────────────────────────────────────┤
│  2. CAMADA DE ABSTRAÇÃO                                  │
│     [ Cap. Mapper ]  [ Msg Translator ]  [ Context Mgr ] │
├──────────────────────────────────────────────────────────┤
│  3. CAMADA DE ADAPTADORES                                │
│     [ Adapt MCP ]    [ Adapt A2A ]      [ Adapt ACP ]    │
└──────────────────────────────────────────────────────────┘
```

### Fluxo de Processamento

```
Mensagem de entrada
  → Adaptador do protocolo origem
    → Camada de Abstração (tradução)
      → Camada de Inferência NL (validação)
        → Adaptador do protocolo destino
          → Mensagem de saída
```

---

## Protocolos Suportados

### MCP — Model Context Protocol

- **Topologia**: Cliente-Servidor
- **Viés**: Contexto & Tools
- **Primitivos**: Resources, Tools, Prompts
- **Transporte**: JSON-RPC 2.0
- **Implementação SEDF**: Padrão IIFE_MODULE_PATTERN (100% de adesão)

### A2A — Agent-to-Agent Protocol

- **Topologia**: Peer-to-Peer
- **Viés**: Tarefas & Skills
- **Artefatos**: Agent Cards (JSON Schema)
- **Estados de Tarefa**: `submitted → working → completed | failed | canceled`
- **Design**: Agentic, Capability-first, Modality-agnostic, Opaque execution, Enterprise-ready

### ANP — Agent Network Protocol

- **Topologia**: Descentralizada
- **Viés**: Identidade & Rede
- **Infraestrutura**: DIDs (W3C) + Verifiable Credentials
- **Descoberta**: Agent Description Documents (busca híbrida semântica)

### ACP — Agent Communication Protocol

- **Topologia**: Híbrida
- **Viés**: Mensageria & Assincronia
- **Subprotocolo**: ACNBP (Agent Capability Negotiation and Binding)
- **Infraestrutura**: ANS (Agent Name Service)

### Comparação Rápida

| Aspecto     | MCP             | A2A              | ANP                | ACP        |
|-------------|-----------------|------------------|--------------------|------------|
| Topologia   | Cliente-Servidor| Peer-to-Peer     | Descentralizada    | Híbrida    |
| Descoberta  | Estática        | Dinâmica (Cards) | Semântica (DIDs)   | Federada   |
| Viés        | Contexto & Tools| Tarefas & Skills | Identidade & Rede  | Mensageria |

---

## Oráculos Epistêmicos

O framework distingue dois tipos de oráculos, alinhados à dualidade cognitiva LLM/LRM:

### Oráculo Semântico (LLM — System 1)

- **Modelos**: GPT-4o, Gemini Flash
- **Função**: Mediação de tradução e interoperabilidade sintática
- **Latência**: < 1s
- **Métrica de Sucesso**: Fluidez e preservação de intenção

### Oráculo Raciocinador (LRM — System 2)

- **Modelos**: o1 (OpenAI), R1 (DeepSeek), Gemini 1.5 Pro (thinking)
- **Função**: Garantia de validade epistêmica e lógica
- **Latência**: 10s–60s
- **Métrica de Sucesso**: Correção lógica com tolerância a erro ≈ 0

### Taxonomia Hierárquica

| Ordem     | Escopo                         | Exemplo                                             |
|-----------|--------------------------------|------------------------------------------------------|
| 1ª Ordem  | Consultas factuais diretas     | "Qual o status do protocolo A2A?"                    |
| 2ª Ordem  | Conhecimento de outros agentes | "O Agente B conhece a especificação MCP?"            |
| Superior  | Meta-epistêmico                | "É possível determinar se existe agente para X?"     |

### Camada de Mediação Oracular

```
┌─────────────────────────────────────────────────────┐
│           CAMADA DE MEDIAÇÃO ORACULAR                │
│  ┌──────────────┐ ┌────────────────┐ ┌────────────┐ │
│  │Orác. Semântico│ │Orác. Ontológico│ │Orác. Pragma│ │
│  │ (Significado) │◄│  (Conceitos)   │►│ (Contexto) │ │
│  └───────┬───────┘ └───────┬────────┘ └──────┬─────┘ │
└──────────┼─────────────────┼─────────────────┼───────┘
     ┌─────┴─────┐     ┌────┴─────┐     ┌─────┴─────┐
     │  Agt MCP  │     │ Agt A2A  │     │  Agt ACP  │
     └───────────┘     └──────────┘     └───────────┘
```

---

## Estrutura do Projeto

```
framework_agentnl/
├── README.md                        # Este arquivo
├── LICENSE                          # Licença MIT
├── EXEGESE.md                       # Exegese geral do framework
├── GLOSSARIO.md                     # Glossário de termos e acrônimos
├── ARQUITETURA.md                   # Detalhamento arquitetural completo
├── config/
│   └── bridge-config.yaml           # Configuração do bridge MCP↔A2A
├── src/
│   ├── core/
│   │   ├── semantic_translator.py   # Algoritmo de tradução semântica
│   │   ├── oracle_query.py          # Padrões de consulta oracular
│   │   ├── nl_reasoner.py           # Motor de inferência NL
│   │   └── unified_capability.ts    # Modelo de capacidades unificado (TypeScript)
│   └── apps_script/
│       ├── session_manager.js       # Context Keeper (MCP)
│       ├── job_queue.js             # Orquestrador de tarefas A2A
│       ├── event_bus.js             # Comunicação Pub/Sub
│       └── sheet_repository.js      # Abstração CRUD sobre Google Sheets
└── docs/
    └── tabelas_resumo.md            # Consolidação das 27 tabelas do framework
```

---

## Primeiros Passos

### 1. Compreender a Base Teórica

Leia o arquivo [`EXEGESE.md`](./EXEGESE.md) para uma visão exegética dos fundamentos:

- Lógica Natural (NL) e operadores epistêmicos
- Ontologias computacionais e alinhamento
- Teoria dos Atos de Fala em sistemas multi-agente
- Paradigma da Autonomia Supervisionada

### 2. Explorar a Arquitetura

Consulte [`ARQUITETURA.md`](./ARQUITETURA.md) para entender:

- Camadas de inferência, abstração e adaptação
- Modelo de capacidades unificado (`UnifiedCapability`)
- Algoritmo de tradução semântica (5 etapas)
- Padrões de integração (Bridge Bidirecional)

### 3. Consultar o Glossário

O [`GLOSSARIO.md`](./GLOSSARIO.md) reúne todos os termos técnicos, acrônimos e definições formais utilizados no framework.

### 4. Configurar o Bridge Semântico

```yaml
# config/bridge-config.yaml
bridge:
  name: "MCP-A2A Semantic Bridge"
  endpoints:
    mcp:
      host: "localhost"
      port: 3000
      transport: "stdio"
    a2a:
      host: "agent.example.com"
      port: 443
      transport: "https"
  translation:
    strategy: "semantic_preserve"
    oracle:
      type: "llm"
      model: "claude-4-opus"
      temperature: 0.1
  validation:
    enabled: true
    consistency_threshold: 0.95
```

### 5. Implementar um Agente (Padrão IIFE/MCP)

```javascript
const MeuAgente = (function() {
  // Contexto privado — isolado do escopo global
  const _estadoInterno = {};
  const _configuracoes = {};

  // Interface pública — contrato de comunicação
  return {
    inicializar: function(contexto) { /* ... */ },
    obterEstado: function() { return {..._estadoInterno}; },
    processarRequisicao: function(req) { /* ... */ }
  };
})();
```

---

## Métricas de Validação

### Desempenho do Framework (12.500 mensagens)

| Métrica                   | Valor   | IC 95%           |
|---------------------------|---------|------------------|
| Latência P50 (ms)         | 145     | [138, 152]       |
| Latência P99 (ms)         | 890     | [845, 935]       |
| Throughput (msg/s)        | 1.240   | [1.180, 1.300]   |
| Taxa de Sucesso           | 96,8%   | [95,9%, 97,7%]   |
| Preservação Semântica     | 0,923   | [0,908, 0,938]   |

### Preservação Semântica por Tradução

| Tradução   | Preservação | Classificação |
|------------|-------------|---------------|
| MCP → A2A  | 92,4%       | Alta          |
| A2A → MCP  | 91,7%       | Alta          |
| MCP → ACP  | 94,1%       | Muito Alta    |
| ACP → MCP  | 93,2%       | Alta          |
| A2A → ACP  | 95,3%       | Muito Alta    |
| ACP → A2A  | 94,8%       | Muito Alta    |
| **Média**  | **93,6%**   | **Alta**      |

### NASA-TLX Adaptado (Workflows)

| Dimensão      | Enxame Autônomo | Híbrido (NL) | Manual   |
|---------------|-----------------|--------------|----------|
| Carga Mental  | 6.0 (±0.8)      | 5.4 (±0.6)   | 2.8      |
| Frustração    | 5.1 (±1.2)      | 4.6 (±0.9)   | 1.8      |
| Transparência | 2.4 (±0.7)      | 5.4 (±0.5)   | N/A      |
| Confiança     | 4.2 (±0.9)      | 4.0 (±0.7)   | 3.8      |

---

## Casos de Uso

### 1. Assistente de Pesquisa Multi-Modal

Integra agentes MCP (busca em bases acadêmicas), A2A (análise com modelos de raciocínio) e ACP (síntese com templates de escrita) para pesquisa acadêmica automatizada. Melhoria: **76,5%** de redução em retrabalho, **19,2%** na latência e **20,9%** na taxa de sucesso.

### 2. Orquestração de Pipeline de Dados

Coordenação multi-protocolo em 4 estágios: `ingest (MCP)` → `transform (A2A)` → `analyze (ACP)` → `report (MCP)`, com estados unificados gerenciados pelo Coordenador Semântico.

### 3. Negociação Multi-Agente

Protocolos formais de negociação semântica (`propose → counter → accept/reject`) com três propriedades desejáveis: (N1) **Terminação** em tempo finito, (N2) **Racionalidade** — aceitação somente se melhora a utilidade, (N3) **Eficiência de Pareto** — resultado ótimo sem prejudicar outros agentes.

### 4. Gestão Educacional SEDF (Validação Empírica)

- **SGTE** — Transporte Escolar: 9.000 alunos, 300+ linhas, ~1.200 viagens/dia
- **SGAE** — Alimentação Escolar: 680 escolas, 350 mil refeições/dia
- **Codebase**: ~215.000 linhas combinadas, 70 módulos MCP, 100% adesão IIFE
- **Processamento diário**: 18.000 registros de presença, 600+ cálculos de rota
- **Impacto**: 475.000 estudantes atendidos no Distrito Federal

---

## Infraestrutura de Runtime

### Google Apps Script como Orquestrador Serverless

O ecossistema SEDF opera sobre duas plataformas complementares:

- **script.google.com** — Contêiner de execução gerenciado com autenticação OAuth2 transparente, gerenciamento de cotas e deploy atômico
- **Google Colab** — Laboratório Python para análise preditiva, prototipagem de oráculos e validação em larga escala via pandas/numpy

### `google.script.run` como Barramento RPC Assíncrono

A comunicação frontend-backend utiliza o protocolo proprietário `google.script.run`, que atua como barramento RPC assíncrono alinhado ao ciclo A2A:

```javascript
google.script.run
  .withSuccessHandler(onSuccess) // A2A Result
  .withFailureHandler(onFailure) // A2A Exception
  .funcaoDoBackend(parametros);  // Invocação do Agente Remoto
```

**Detecção de Ambiente**: `if (typeof google === 'undefined' || !google.script)` permite alternância entre modo Produção (RPC real) e Desenvolvimento Local (mocks).

### Pipeline DevOps

| Etapa          | Ferramenta                      | Ambiente           |
|----------------|---------------------------------|--------------------|
| Desenvolvimento| script.google.com / VS Code     | Local / Web        |
| Versionamento  | Git + GitHub                    | GitHub             |
| Validação      | GitHub Actions / testes internos| CI                 |
| Deploy         | CLASP push / Editor Web         | script.google.com  |
| Análise        | Google Colab (Python)           | colab.google.com   |
| Monitoramento  | AppLogger + aba Telemetry       | Google Sheets      |

---

## Heurísticas de Implementação

### Heurística 1 — Um Agente por Responsabilidade FUNDEB

Cada categoria de despesa (transporte, alimentação, material didático) deve ser gerenciada por um agente distinto e especializado, facilitando a prestação de contas precisa e auditoria eficiente.

### Heurística 2 — Contexto Escolar, Impacto Regional

Agentes no nível escolar publicam eventos padronizados consumidos assincronamente por agentes regionais (CRE), evitando acoplamento direto e promovendo escalabilidade.

### Heurística 3 — Validação como Cidadão de Primeira Classe

Em sistemas onde dados impactam financiamento público (FUNDEB, PDDE), a validação deve ser implementada como **agente autônomo** — nunca como código embutido. Isso permite que o Agente de Validação intercepte preventivamente transações que violem regras orçamentárias dinâmicas, atuando como auditor em tempo real.

---

## Anti-Padrões

| Anti-Padrão              | Consequência                                   | Solução                             |
|--------------------------|-------------------------------------------------|-------------------------------------|
| Monolito Administrativo  | Indisponibilidade total; atualização impossível | Decomposição em agentes por domínio |
| Validação Tardia         | Glosas de recursos; erros tardios               | Agentes de validação em tempo real  |
| Silos de Dados           | Divergências cadastrais                         | Agente centralizador de identidade  |
| Integração por Arquivo   | Latência; perda de dados                        | Comunicação A2A via eventos         |
| Monolito de Modelo       | Tratar toda IA como igual                       | Matriz LLM vs. LRM por tarefa      |

---

## Paradigma da Autonomia Supervisionada

O caminho mais promissor para sistemas multi-agente não reside nos extremos de ferramentas passivas ou agentes totalmente autônomos, mas no paradigma de **Autonomia Supervisionada**:

> *"Não é um mero compromisso ou uma fase de transição para a autonomia total, mas um modelo de design sociotécnico deliberado que busca uma simbiose produtiva e sustentável entre a agência humana e o poder computacional da máquina."*

O usuário torna-se um **"gerente de agentes"**: define objetivos, delega, monitora e intervém em pontos críticos de decisão.

### Framework TRiSM para Oráculos

O **TRiSM** (Trust, Risk and Security Management), adaptado para oráculos epistêmicos, mitiga riscos de:

- Propagação de alucinações em cadeias de agentes
- Viés algorítmico em decisões que impactam populações vulneráveis
- Perda de responsabilidade em delegações multi-nível

---

## Parceria UnDF-SEDF

O framework é validado empiricamente pela parceria estratégica entre a **Universidade do Distrito Federal (UnDF)** e a **Secretaria de Estado de Educação do DF (SEDF)**, configurada como:

- **Tríplice Hélice**: UnDF (academia) + GDF/FAPDF (governo) + BioTIC (indústria)
- **Campo de Estágio**: Estagiários atuam como *"Human-in-the-Loop de Segunda Ordem"*, auditando traduções oraculares
- **Cursos Alinhados**: Ciência da Computação (SBC), Engenharia de Software (SWEBOK), Ciência da Informação (ABECI)
- **Escala Real**: 475.000 estudantes, 680 escolas, 215.000 LOC, conformidade FUNDEB/PDDE

---

## Referências Teóricas

### Formalizações do Framework

- **Definição 1**: Operador de Conhecimento — `K_a(φ)` com axiomas de Veracidade, Distribuição e Introspecção
- **Definição 2**: Ontologia Computacional — `O = ⟨C, R, I, A⟩`
- **Definição 3**: Alinhamento Ontológico — `M = {⟨e₁, e₂, r, c⟩}`
- **Definição 4**: Oráculo Epistêmico — `O = ⟨D, Q, R, φ⟩`
- **Definição 5**: Negociação Semântica — `N = ⟨m₁, m₂, ..., mₙ⟩`
- **Teorema 1**: Aproximação Oracular (LLM → Oráculo ideal)
- **Teorema 2**: Preservação Semântica (`|S(m) − S(T(m))| ≤ ε`)
- **Teorema 3**: Completude do Mapeamento entre protocolos
- **Proposição**: Complexidade de Tradução — `O(n × log(|O|) + n × T_oracle)`

### Equação de Confiança

```
T = λ₁·E_x + λ₂·S_e + λ₃·P_v + λ₄·I_v
```

Onde: T = Confiança total | E_x = Explicabilidade | S_e = Segurança | P_v = Previsibilidade | I_v = Identidade verificável

### Autores e Frameworks Citados

- Castioni, Cerqueira e Cardoso (2021) — Capacidades Institucionais e Entidades Executoras
- Santos et al. (2025) — Fragmentação de Sistemas em Gestão Educacional
- Shen e Yang (2025) — "Da Mente à Mão" (Mind-to-Hand)
- Gulli et al. (2025) — Modelo Tripartite (Modelo, Ferramentas, Orquestração)
- Raza et al. (2025) — TRiSM (Trust, Risk, Security Management)
- Huang et al. (2025) — ACNBP e DIDs/VCs
- Raskar et al. (2025) — ANS (Agent Name Service)
- Randevik e Petersson (2025) — Paradoxo do Poder vs. Controle
- Gabison e Xi (2025) — Teoria do Principal-Agente aplicada a IA
- Aksu et al. (2025) — NASA-TLX e Inter-relações de Carga Mental
- Rangel (2025) — Manual de Oslo e Inovação no SNI
- Etzkowitz (1997) — Universidade Empreendedora e Terceira Missão

### Trabalhos Futuros

1. **Aprendizado de mapeamentos ontológicos** — Alinhamentos via ML a partir de corpora de comunicação
2. **Oráculos distribuídos** — Escalabilidade horizontal com consenso semântico
3. **Verificação formal** — Prova automática de invariantes semânticas
4. **Extensão ANP** — Descoberta descentralizada com DIDs e credenciais verificáveis

---

## Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [`LICENSE`](./LICENSE) para detalhes.

Este framework é parte do produto técnico-tecnológico da dissertação de Mestrado Profissional em Políticas Públicas e Gestão da Educação (UnB/UnDF).

---

> *"A convergência dos protocolos MCP, A2A e ACP não é meramente técnica — representa uma transformação paradigmática na forma como concebemos a comunicação entre entidades artificiais. Assim como a linguagem natural evoluiu para permitir a cooperação humana complexa, estes protocolos estabelecem as fundações para uma nova era de colaboração entre agentes artificiais, onde a compreensão mútua transcende diferenças sintáticas e ontológicas."*
>
> — Framework NL-Agent, 2026
