# 🏗️ ARQUITETURA — Framework NL-Agent

> Detalhamento arquitetural completo do framework NL-Agent: camadas, componentes, fluxos de dados, modelo de capacidades e padrões de integração.

---

## 1. Visão Geral da Arquitetura Multinível

O framework opera em **três camadas** verticais e **três níveis hierárquicos** horizontais, refletindo diretamente a estrutura organizacional do ecossistema educacional: a camada de inferência processa a lógica semântica que sustenta decisões; a camada de abstração traduz entre os domínios heterogêneos da gestão escolar (transporte, alimentação, frequência); e a camada de adaptadores conecta-se aos protocolos de comunicação que viabilizam a interoperabilidade em escala.

### 1.1 Camadas Verticais

```
┌──────────────────────────────────────────────────────────────┐
│              NL-AGENT FRAMEWORK                              │
├──────────────────────────────────────────────────────────────┤
│  CAMADA 1 — INFERÊNCIA NL                                    │
│  ┌───────────┐   ┌───────────┐   ┌─────────────┐            │
│  │  Reasoner │◄─►│  Unifier  │◄─►│  Validator   │           │
│  │(Inferência)│  │(Alinhamento│  │(Consistência)│            │
│  └───────────┘   └───────────┘   └─────────────┘            │
├──────────────────────────────────────────────────────────────┤
│  CAMADA 2 — ABSTRAÇÃO                                        │
│  ┌──────────────┐ ┌────────────────┐ ┌─────────────────┐    │
│  │ Cap. Mapper  │ │ Msg Translator │ │  Context Manager │    │
│  │(Mapeamento)  │ │ (Tradução)     │ │  (Contexto)      │    │
│  └──────────────┘ └────────────────┘ └─────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│  CAMADA 3 — ADAPTADORES                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │ Adapt MCP  │  │ Adapt A2A  │  │ Adapt ACP  │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Níveis Hierárquicos (Gestão Educacional)

| Nível        | Função                | Agentes                               | Protocolo  | Impacto Educacional |
|--------------|-----------------------|---------------------------------------|------------|---------------------|
| Estratégico  | Consolidação regional | Agente Orquestrador CRE               | A2A Tasks  | Visão integrada de 680 escolas para planejamento de políticas regionais |
| Tático       | Operações por domínio | Transporte, Alimentação, Frequência   | MCP Context| Gestão operacional que impacta diretamente 475.000 estudantes |
| Operacional  | Persistência          | SheetRepository, DriveService, Cache  | Acesso direto| Dados estruturados em infraestrutura acessível (Sheets-as-Database) |

---

## 2. Componentes da Camada de Inferência NL

### 2.1 Reasoner (Motor de Inferência)

Responsável por aplicar regras de inferência da Lógica Natural sobre mensagens em trânsito:

- **Inferência Monotônica**: Preserva conclusões ao adicionar informação
- **Inferência Não-Monotônica**: Permite revogação de conclusões com nova evidência
- **Classificação de complexidade**: Roteia consultas para LLM ou LRM

### 2.2 Unifier (Alinhamento Ontológico)

Produz correspondências entre ontologias de protocolos distintos:

```
M = {⟨e₁, e₂, r, c⟩}

r ∈ {≡, ⊑, ⊒, ⊥}    # equivalência, subsunção, superclasse, disjunção
c ∈ [0, 1]             # grau de confiança
```

Processo de alinhamento:
1. Extrai conceitos da ontologia de origem
2. Consulta oráculo semântico para candidatos
3. Avalia relação semântica via NLP
4. Atribui confiança com base em evidência

### 2.3 Validator (Validação de Consistência)

Verifica que mensagens traduzidas não violam invariantes lógicas:

- Ausência de contradições internas
- Preservação de precondições e poscondições
- Threshold de consistência configurável (padrão: 0.95)

---

## 3. Componentes da Camada de Abstração

### 3.1 Capability Mapper (Mapeamento de Capacidades)

Traduz capacidades entre taxonomias de protocolos usando o modelo `UnifiedCapability`:

```typescript
interface UnifiedCapability {
  // Identificação
  id: string;
  name: string;
  version: string;

  // Semântica
  description: string;
  semanticType: 'resource' | 'action' | 'template' | 'composite';
  ontologyMapping: OntologyReference[];

  // Interface
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;

  // Proveniência
  provenance: {
    sourceProtocol: 'MCP' | 'A2A' | 'ACP';
    originalDefinition: any;
    transformationLog: TransformationEntry[];
  };

  // Restrições
  constraints: {
    preconditions: LogicalExpression[];
    postconditions: LogicalExpression[];
    invariants: LogicalExpression[];
  };
}
```

**Mapeamentos fundamentais**:

| Origem (MCP)     | Destino (A2A)       | Tipo          |
|------------------|---------------------|---------------|
| `tool.name`      | `skill.id`          | Direto        |
| `tool.description`| `skill.description`| Direto        |
| `tool.inputSchema`| `skill.inputSchema`| Direto        |
| *(sem equivalente)*| `skill.tags`      | Deriv. via NLP|
| *(sem equivalente)*| `skill.examples`  | Sintético     |

### 3.2 Message Translator (Tradução de Mensagens)

Implementa o **Algoritmo 5.1: Tradução Semântica** em 5 etapas:

```
Entrada: M_origem (mensagem), P_destino (protocolo alvo)
Saída:   M_destino (mensagem traduzida + metadados)

1. EXTRAIR  → S ← AnalisarSemântica(M_origem)
2. IDENTIFICAR → C ← ConsultarOráculo(S.conceitos, P_destino.ontologia)
3. TRANSFORMAR → Para cada conceito c ∈ S.conceitos:
   SE mapeamento direto → aplicar transformação direta
   SENÃO SE composto   → decompor e traduzir componentes
   SENÃO              → gerar aproximação + aviso de perda
4. VALIDAR → SE Inconsistente(M_destino): aplicar correções NL
5. RETORNAR → M_destino com metadados de tradução
```

### 3.3 Context Manager (Gerenciamento de Contexto)

Mantém o estado compartilhado entre protocolos durante traduções em sessão:

- **Session context**: Dados do usuário/agente corrente
- **Translation context**: Histórico de traduções na sessão
- **Cache context**: Traduções frequentes para reutilização

---

## 4. Camada de Adaptadores

### 4.1 Adaptador MCP

Converte entre formato interno do NL-Agent e JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "semantic_search",
    "arguments": { "query": "..." }
  },
  "id": 1
}
```

**Primitivos suportados**:
- `Resources` → FonteDeDados → consulta
- `Tools` → CapacidadeExecutável → invocação
- `Prompts` → TemplateReutilizável → instanciação

### 4.2 Adaptador A2A

Converte entre formato interno e estrutura A2A com Agent Cards:

```json
{
  "role": "agent",
  "parts": [
    { "type": "text", "text": "Análise concluída." },
    { "type": "data", "data": { "key": "value" } },
    { "type": "file", "file": { "name": "report.pdf", "mimeType": "application/pdf" } }
  ]
}
```

**Modalidades**: Text, Data, File (multimodal)

### 4.3 Adaptador ACP

Converte entre formato interno e modelo unificado ACP:

```json
{
  "acp_version": "1.0",
  "message_type": "request",
  "correlation_id": "uuid-v4",
  "sender": { "agent_id": "alpha", "capabilities": ["reasoning"] },
  "receiver": { "agent_id": "beta", "required_capabilities": ["data-analysis"] },
  "payload": { "intent": "analyze_dataset", "parameters": {}, "context": {} },
  "metadata": { "priority": "high", "timeout_ms": 30000, "retry_policy": {} }
}
```

---

## 5. Camada de Mediação Oracular

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

### 5.1 Fluxo de Mediação

1. Agente origem → consulta **Oráculo Ontológico** (tradução de conceitos)
2. Oráculo Ontológico → delega a **Oráculo Semântico** (preservação de significado)
3. Oráculo Semântico → ajusta via **Oráculo Pragmático** (adaptação contextual)
4. Resposta → retorna ao agente origem

### 5.2 Protocolo de Consulta Oracular

```json
{
  "oracle_query": {
    "type": "semantic_alignment",
    "source": {
      "protocol": "MCP",
      "concept": "tool",
      "definition": "An executable capability exposed by a server"
    },
    "target": {
      "protocol": "A2A",
      "concept": "skill"
    },
    "context": {
      "use_case": "protocol_bridge",
      "constraints": ["preserve_semantics", "maintain_composability"]
    }
  }
}
```

### 5.3 Heurística de Roteamento LLM/LRM

| Tipo de Tarefa            | Oráculo     | Latência | Custo   |
|---------------------------|-------------|----------|---------|
| Tradução sintática        | LLM (Flash) | < 1s     | Baixo   |
| Resumo e descrições       | LLM (4o)    | 1–3s     | Médio   |
| Cálculos orçamentários    | LRM (o1)    | 10–30s   | Alto    |
| Verificação legal/FUNDEB  | LRM (R1)    | 20–60s   | Alto    |
| Otimização de rotas       | LRM (o1)    | 15–45s   | Alto    |

---

## 6. Handshake MCP

Sequência de estabelecimento de conexão:

| Passo | Emissor  | Receptor | Mensagem              | Conteúdo                          |
|-------|----------|----------|-----------------------|-----------------------------------|
| 1     | Cliente  | Servidor | `initialize`          | `protocolVersion`, `capabilities` |
| 2     | Servidor | Cliente  | `initialize` (resp.)  | `protocolVersion`, `capabilities` |
| 3     | Cliente  | Servidor | `initialized`         | Notificação de confirmação        |
| 4     | —        | —        | Conexão Estabelecida  | Comunicação bidirecional ativa    |

---

## 7. Taxonomia de Módulos (SEDF — 70 módulos)

| Camada               | Componentes                                                          | Função                          |
|----------------------|----------------------------------------------------------------------|---------------------------------|
| Contexto             | SessionManager (12), CacheService (8), PropertiesManager (15), ConfigManager (23) | Isolamento e propagação         |
| Serviços Especializados | TransporteService, AlimentacaoService, ValidationService, ReportService | Regras de negócio por domínio   |
| Integração           | APIGateway, trackedUrlFetch, GoogleMapsService                       | Sistemas externos               |
| Persistência         | SheetRepository, DriveService, CacheService                         | Armazenamento e recuperação     |

### Métricas Estruturais

| Métrica              | Valor  |
|----------------------|--------|
| Total de Módulos     | 70     |
| Padrão IIFE          | 100%   |
| Funções Expostas     | 485+   |
| Referências Cruzadas | 234    |
| Serviços de Contexto | 4      |

---

## 8. Taxonomia de Agentes Educacionais

| Categoria              | Função                       | Exemplos                                  | Protocolo | Aplicação Educacional |
|------------------------|------------------------------|-------------------------------------------|-----------|-----------------------|
| Agentes de Contexto    | Estado e configurações       | SessionManager, ConfigManager             | MCP       | Preservam contexto do gestor entre interações, garantindo continuidade de sessão |
| Agentes de Domínio     | Regras de negócio            | TransporteService, AlimentacaoService     | A2A       | Processam regras específicas de cada área: otimização de rotas, cálculo nutricional |
| Agentes de Validação   | Integridade de dados         | ValidationService, SchemaValidator        | ACP       | Verificam conformidade FUNDEB/PDDE em tempo real, evitando glosas |
| Agentes de Integração  | Sistemas externos            | GoogleMapsService, DriveService           | MCP       | Conectam dados escolares a serviços geográficos e de armazenamento |
| Agentes de Apresentação| Renderização de interfaces   | RenderDashboard, RenderRelatorios         | ANP       | Transformam dados brutos em dashboards acionáveis para gestores |

Cada agente opera sob o princípio da **Heurística 1** (Um Agente por Responsabilidade FUNDEB): categorias de despesa distintas são geridas por agentes especializados, facilitando prestação de contas precisa e auditoria eficiente. A **Heurística 3** (Validação como Cidadão de Primeira Classe) garante que o Agente de Validação intercepte preventivamente transações que violem regras orçamentárias dinâmicas, atuando como auditor em tempo real.

---

## 9. Processamento Assíncrono (Backend A2A)

### 9.1 JobQueue — Orquestrador de Tarefas

```javascript
const JobQueue = (function() {
  const _fila = [];
  const _emProcessamento = new Map();

  return {
    enfileirar: function(tarefa) {
      const job = {
        id: Utilities.getUuid(),
        tipo: tarefa.tipo,
        dados: tarefa.dados,
        prioridade: tarefa.prioridade || 'normal',
        estado: 'submitted',
        tentativas: 0,
        maxTentativas: tarefa.maxRetries || 3
      };
      _fila.push(job);
      return job.id;
    },

    dequeue: function() {
      _fila.sort((a, b) => this._compararPrioridade(a, b));
      const job = _fila.shift();
      if (job) {
        job.estado = 'working';
        _emProcessamento.set(job.id, job);
      }
      return job;
    },

    _compararPrioridade: function(a, b) {
      const ordem = { critica: 0, alta: 1, normal: 2, baixa: 3 };
      return ordem[a.prioridade] - ordem[b.prioridade];
    }
  };
})();
```

### 9.2 EventBus — Pub/Sub entre Agentes

```javascript
const EventBus = (function() {
  const _assinantes = new Map();

  return {
    inscrever: function(evento, callback, agente) {
      if (!_assinantes.has(evento)) {
        _assinantes.set(evento, []);
      }
      _assinantes.get(evento).push({ callback, agente });
    },

    publicar: function(evento, dados) {
      const ouvintes = _assinantes.get(evento) || [];
      for (const ouvinte of ouvintes) {
        ouvinte.callback(dados);
      }
    }
  };
})();
```

### 9.3 API Gateway Pattern (doGet/doPost)

As funcoes `doGet()` e `doPost()` do Google Apps Script funcionam como **Gateways de Entrada** para o sistema multi-agente:

```javascript
function doGet(e) {
  const action = e.parameter.action;
  const router = {
    'listarAlunos': function() { return TransporteService.listarAlunos(); },
    'obterRota':    function() { return TransporteService.obterRota(e.parameter.id); },
    'dashboard':    function() { return RenderDashboard.gerar(); }
  };
  return ContentService
    .createTextOutput(JSON.stringify(router[action]()))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### 9.4 Barramento RPC Assincrono (`google.script.run`)

A comunicacao frontend-backend nos sistemas SEDF ocorre via `google.script.run`, que atua como **barramento RPC assincrono** alinhado ao ciclo de vida A2A:

```javascript
google.script.run
  .withSuccessHandler(onSuccess) // Callback: A2A Result (completed)
  .withFailureHandler(onFailure) // Callback: A2A Exception (failed)
  .funcaoDoBackend(parametros);  // Invocacao do Agente Remoto (submitted)
```

**Deteccao de Ambiente e Mocking**:

```javascript
if (typeof google === 'undefined' || !google.script) {
  // Modo Desenvolvimento: usar mocks e dados simulados
} else {
  // Modo Producao: RPC real via google.script.run
}
```

Esta capacidade demonstra maturidade de engenharia que permite desenvolvimento desacoplado da infraestrutura Google, facilitando testes sem consumir cotas de execucao reais.

---

## 10. Padrão Bridge Bidirecional

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
    mappings:
      - source: "mcp.tool"
        target: "a2a.skill"
        bidirectional: true
      - source: "mcp.resource"
        target: "a2a.task.input"
        bidirectional: false
  validation:
    enabled: true
    nl_reasoner: "default"
    consistency_threshold: 0.95
```

---

## 11. Estratégia de Descontinuação (Absorção Semântica)

> *"Um protocolo legado P_old só deve ser descontinuado quando todo o seu espaço de capacidades semânticas S(P_old) puder ser mapeado isomorficamente para P_new."*

### Procedimento de Migração

1. **Auditoria de Capacidades** — Identificar funcionalidades exclusivas nos protocolos a descontinuar
2. **Mapeamento para Unified Schema** — Traduzir para `UnifiedCapability`
3. **Redirecionamento de Tráfego** — Adaptadores interceptam chamadas ao protocolo antigo
4. **Arquivamento Seguro** — Remover artefatos de origem após validação de cobertura 100%

---

## 12. Pipeline DevOps (Google Apps Script)

| Etapa          | Ferramenta                      | Função                          | Ambiente           |
|----------------|---------------------------------|---------------------------------|--------------------|
| Desenvolvimento| script.google.com / VS Code     | Edição e testes                 | Local / Web        |
| Versionamento  | Git + GitHub                    | Controle de versões             | GitHub             |
| Validação      | GitHub Actions / testes internos| Linting + testes pré-deploy     | CI                 |
| Deploy         | CLASP push / Editor Web         | Deploy atômico                  | script.google.com  |
| Análise        | Google Colab (Python)           | Análise de dados e ML           | colab.google.com   |
| Monitoramento  | AppLogger + aba Telemetry       | Logs e metricas de saude        | Google Sheets      |

Para projetos de maior escala como o SGTE (~63 mil linhas) e o SGAE (~135 mil linhas), a ferramenta **CLASP** (Command Line Apps Script Projects) permite desenvolvimento local com VS Code, versionamento via Git e deploy automatizado via `clasp push`. Praticas de CI/CD sao implementadas via GitHub Actions com verificacoes de linting, testes unitarios e deploy condicionado.

---

## 13. Fluxo A2A Completo: Interface -> Backend

```
+--------------------------------------------------------+
|         FLUXO A2A: INTERFACE -> BACKEND                 |
+--------------------------------------------------------+
|  [Agente Humano]                                       |
|       |  (1) Clique "Registrar Incidente"              |
|       v                                                |
|  [Modal ANP] <---- (2) Negociacao de Intencao          |
|       |  (3) Confirmacao + Dados                       |
|       v                                                |
|  [APIGateway] <-- (4) Serializacao ACP                 |
|       |  (5) doPost()                                  |
|       v                                                |
|  [ValidationService] <-- (6) Validacao Backend         |
|       |  (7) Persistencia                              |
|       v                                                |
|  [SheetRepository] <-- (8) Google Sheets               |
|       |                                                |
|       v                                                |
|  [Agente Humano] <-- (9) Confirmacao Visual            |
+--------------------------------------------------------+
```

---

## 14. Complexidade Computacional

A traducao de `n` conceitos entre protocolos tem complexidade:

```
O(n x log(|O|) + n x T_oracle)
```

- **Primeiro termo** `n x log(|O|)`: Busca na ontologia compartilhada
- **Segundo termo** `n x T_oracle`: Custo de consultas ao modelo, onde `T_oracle` varia:
  - LLM: < 1s (traducao, resumo)
  - LRM: ~30s (planejamento, compliance)

**Otimizacoes implementadas**:
- Cache de traducoes frequentes em CacheService (TTL configuravel)
- Processamento em lote para multiplas consultas (reduz latencia em 76,5%)
- Throughput resultante: 1.240 msg/s (IC 95%: 1.180-1.300)

### Analise de Perdas Semanticas

As perdas semanticas residuais concentram-se em tres categorias:

| Categoria                 | % das Perdas | Exemplo                                                      |
|---------------------------|--------------|--------------------------------------------------------------|
| Conceitos idiossincraticos| 28%          | `Prompt` (MCP) sem equivalente exato em `Tasks` (A2A)        |
| Nuances contextuais       | 45%          | Informacoes implicitas no contexto de uso                    |
| Estruturas compostas      | 27%          | Combinacoes que nao preservam composicionalidade             |

**Achado relevante**: A consulta oracular resolve 89,3% dos casos ambiguos, com tempo medio de 180ms (P50: 145ms, P99: 890ms, em 12.500 interacoes).

**Assimetria observada**: Traducoes *para* ACP (94,1%-95,3%) superam consistentemente traducoes *de* ACP (93,2%-94,8%), sugerindo que o ACP serve como **protocolo intermediario eficiente** para gateways de traducao.

---

## 15. Estratégia de Resiliência e Recuperação

A arquitetura adota a **falha progressiva** (graceful degradation) para assegurar que a indisponibilidade de agentes periféricos não comprometa o núcleo operacional. No contexto educacional, isso significa que a falha de um agente de integração geográfica não impede o processamento de presença escolar, e a indisponibilidade de um oráculo LRM não bloqueia o registro de incidentes de transporte:

- **EventStore**: Registro imutável e sequencial de transações para auditoria forense e replay automático — essencial para reconstituir decisões algorítmicas em auditorias do FUNDEB
- **Notificações estruturadas**: Falhas de mapeamento geram eventos no EventBus com estratégias de recuperação (decomposição recursiva, delegação dinâmica, oráculos epistêmicos)
- **Completude do Mapeamento (Teorema 3)**: Para todo `c` em Cap(P1), existe `c'` em Cap(P2) tal que M(c) = c' ou M(c) = bottom -- a notação bottom garante notificação explícita quando não há correspondência
- **Auditabilidade como princípio**: Cada decisão algorítmica é rastreável, permitindo que gestores, auditores e órgãos de controle verifiquem a cadeia completa de raciocínio que levou a uma ação sobre dados de estudantes
