# 📖 EXEGESE — Framework NL-Agent

> Exegese geral dos fundamentos teóricos, arquiteturais e empíricos que sustentam o framework NL-Agent para interoperabilidade semântica em sistemas multi-agentes.

---

## 1. Fundamento Epistemológico: A Lógica Natural

A **Lógica Natural (NL)** constitui o alicerce filosófico do framework. Diferentemente das lógicas formais clássicas, a NL enfatiza a **inferência intuitiva** e a **preservação de relações semânticas naturais**, operando sobre estruturas que refletem padrões de raciocínio humano.

### 1.1 Operadores Epistêmicos

O framework define o **Operador de Conhecimento** `K_a(φ)` — "O agente `a` conhece a proposição `φ`" — governado por três axiomas:

| Axioma | Nome                  | Formulação                           | Significado                                      |
|--------|-----------------------|--------------------------------------|--------------------------------------------------|
| K1     | Veracidade            | `K_a(φ) → φ`                        | Conhecimento implica verdade                     |
| K2     | Distribuição          | `K_a(φ→ψ) → (K_a(φ) → K_a(ψ))`    | Conhecimento se distribui sobre implicações      |
| K3     | Introspecção Positiva | `K_a(φ) → K_a(K_a(φ))`             | Saber que se sabe                                |

Estes axiomas distinguem **conhecimento** de mera **crença** pela exigência de veracidade — condição sine qua non para a atribuição de conhecimento a agentes artificiais.

### 1.2 Inferência Monotônica e Não-Monotônica

A NL reconhece dois modos de inferência:

- **Monotônica**: Novas premissas não invalidam conclusões anteriores.
  ```
  Γ ⊢ φ  ⇒  Γ ∪ {ψ} ⊢ φ
  ```

- **Não-Monotônica**: Novas informações podem revogar conclusões prévias, modelando o raciocínio *defeasível* de agentes em ambientes dinâmicos.

**Implicação prática**: No SGTE, uma rota ótima calculada (inferência monotônica) pode ser revista quando um incidente de trânsito é notificado (inferência não-monotônica), sem invalidar todo o modelo.

---

## 2. Ontologias e Representação de Conhecimento

### 2.1 Definição Formal

Uma **ontologia computacional** `O = ⟨C, R, I, A⟩` compreende:

- **C** — Conjunto de conceitos (classes)
- **R ⊆ C × C** — Relações entre conceitos
- **I** — Instâncias
- **A** — Axiomas restritivos

### 2.2 O Problema do Alinhamento na Educação Pública

No ecossistema educacional, o problema do alinhamento ontológico manifesta-se de forma concreta e consequente. Cada sistema define suas entidades segundo lógicas próprias, criando **silos de inteligência** que fragmentam a visão institucional:

| Sistema | Conceito de "Aluno" | Identificador | Consequência do Desalinhamento |
|---------|---------------------|---------------|--------------------------------|
| SGTE (Transporte) | Passageiro com escola-origem e escola-destino | Matrícula + código de rota | Aluno sem rota atribuída perde acesso ao transporte |
| SGAE (Alimentação) | Beneficiário com perfil nutricional e restrições alimentares | Código nutricional + turma | Restrição alimentar não propagada pode causar risco à saúde |
| Frequência | Presença diária vinculada a turma e disciplina | Registro diário + turno | Divergência com transporte: aluno "presente" sem rota registrada gera inconsistência FUNDEB |
| Matrícula | Vínculo legal com a rede de ensino | Número de matrícula oficial | Base cadastral desatualizada invalida dados de todos os outros sistemas |

O **alinhamento ontológico** formal resolve essas divergências:

```
M = {⟨e₁, e₂, r, c⟩}
```

Onde `e₁ ∈ O₁`, `e₂ ∈ O₂`, `r ∈ {≡, ⊑, ⊒, ⊥}` é a relação semântica e `c ∈ [0,1]` o grau de confiança.

O framework resolve este problema via **consultas oraculares**: o oráculo semântico (LLM) analisa descrições em linguagem natural de cada conceito e produz o alinhamento automaticamente, com taxa de acerto de 89,3% em casos ambíguos. No contexto educacional, essa mediação é crítica: quando o agente de transporte informa que "o aluno João foi transportado", o agente de alimentação precisa compreender que *esse mesmo* João é o beneficiário do cardápio especial — uma tradução que exige tanto precisão técnica quanto consciência das consequências humanas de uma falha.

---

## 3. Atos de Fala e Performativos

A comunicação entre agentes é analisada pela lente da **Teoria dos Atos de Fala** (Austin, 1962; Searle, 1969), adaptada ao contexto computacional:

| Categoria    | Performativos                     | Efeito Pretendido             |
|--------------|-----------------------------------|-------------------------------|
| Assertivos   | `inform`, `confirm`, `disconfirm` | Transmitir informação         |
| Diretivos    | `request`, `query`, `subscribe`   | Solicitar ação/informação     |
| Comissivos   | `promise`, `accept`, `reject`     | Comprometer-se com ação       |
| Declarativos | `define`, `cancel`, `register`    | Alterar estado do mundo       |

As **condições de felicidade** (conteúdo proposicional, preparatória, sinceridade, essencial) garantem a validade pragmática das interações — um modal de confirmação de exclusão, por exemplo, satisfaz a condição preparatória ao verificar permissões antes de executar.

---

## 4. A Dualidade LLM/LRM: System 1 e System 2

O framework implementa uma **arquitetura cognitiva híbrida** que distingue:

### System 1 — LLMs (Large Language Models)

- **Analogia**: Pensamento rápido, intuitivo, associativo
- **Exemplos**: GPT-4o, Gemini Flash
- **Uso**: Interface com usuário, tradução sintática, geração de descrições
- **Latência**: < 1s
- **Risco**: Alucinação em tarefas de precisão

### System 2 — LRMs (Large Reasoning Models)

- **Analogia**: Pensamento lento, analítico, lógico
- **Exemplos**: o1 (OpenAI), R1 (DeepSeek), Gemini 1.5 Pro (thinking)
- **Uso**: Cálculos orçamentários, otimização de rotas, compliance legal
- **Latência**: 10–60s
- **Mecanismo**: Chain-of-Thought (CoT) forçada

**Anti-padrão identificado**: O "Monolito de Modelo" — tratar toda IA como igual. O framework implementa uma **Heurística de Roteamento** onde um classificador direciona tarefas para o tipo de oráculo adequado.

---

## 5. O MCP como Materialização Sintática das Fronteiras Epistêmicas

O **Model Context Protocol** não é apenas uma especificação de transporte JSON-RPC. Ele **materializa as fronteiras epistêmicas** da Lógica Natural, forçando que o contexto (o "mundo" do agente) seja explicitado e contido.

### 5.1 O Padrão IIFE como Microcosmo Fractal da Agência

A análise de 215.000 linhas de código da SEDF revelou que o padrão IIFE (Immediately Invoked Function Expression) do JavaScript é um **isomorfismo funcional** do MCP:

```javascript
const ModuloTransporte = (function() {
  // Contexto privado — isolado do escopo global (= Context do MCP)
  const _estadoInterno = {};
  const _configuracoes = {};

  // Interface pública — contrato de comunicação (= Tools/Resources do MCP)
  return {
    inicializar: function(contexto) { /* ... */ },
    obterEstado: function() { return {..._estadoInterno}; },
    processarRequisicao: function(req) { /* ... */ }
  };
})();
```

**Descoberta fundamental**: Desenvolvedores da SEDF, sem treinamento formal em protocolos agênticos, convergiram *organicamente* para soluções IIFE que prepararam estruturalmente o terreno para o MCP. Isso demonstra que o MCP é uma **formalização de práticas emergentes**, não uma abstração teórica distante.

### 5.2 Agentes de Infraestrutura (Context Keepers)

| Agente Teórico     | Implementação Real         | Função                           |
|--------------------|----------------------------|----------------------------------|
| Context Keeper     | `SessionManager`           | Estado da sessão do servidor     |
| State Propagator   | `CacheService`             | Propagação entre requisições     |
| Config Oracle      | `ConfigManager`/`PropertiesManager` | Configurações contextuais |

---

## 6. O A2A como Protocolo de Comunicação Peer-to-Peer

### 6.1 Agent Cards e Descoberta de Capacidades

Cada agente publica um **Agent Card** — documento JSON Schema que declara sua identidade, capacidades, skills e modos de interação. A descoberta de agentes compatíveis é mediada pela **negociação ANP** (Agent Network Protocol).

### 6.2 Ciclo de Vida de Tarefas

```
submitted → working → completed
                    → failed
                    → canceled
```

Na SEDF, este ciclo é implementado pelo `JobQueue` (orquestrador de tarefas) e `EventBus` (comunicação pub/sub):

- **JobQueue**: Fila priorizada (`crítica > alta > normal > baixa`) com retry automático
- **EventBus**: Padrão pub/sub para comunicação desacoplada entre agentes

### 6.3 O `google.script.run` como RPC Assíncrono A2A

A comunicação frontend-backend nos sistemas SEDF ocorre via `google.script.run`, que atua como **barramento RPC assíncrono** com callbacks encadeados — alinhando-se perfeitamente ao ciclo de vida de tarefas A2A:

```javascript
google.script.run
  .withSuccessHandler(onSuccess) // Callback de sucesso (A2A Result)
  .withFailureHandler(onFailure) // Callback de erro (A2A Exception)
  .funcaoDoBackend(parametros);  // Invocação do Agente Remoto
```

Características arquiteturais identificadas:

1. **Assincronicidade Obrigatória** — Padrão não-bloqueante via callbacks, isomorfo ao ciclo `submitted → completed | failed`
2. **Detecção de Ambiente e Mocking** — `if (typeof google === 'undefined' || !google.script)` permite alternância entre Produção (RPC real) e Desenvolvimento Local (mocks), desacoplando agentes da infraestrutura Google
3. **Serialização Transparente** — Marshalling automático de objetos complexos, eliminando parsing manual de JSON

### 6.4 Infraestrutura de Runtime

O ecossistema SEDF opera sobre duas plataformas complementares:

- **script.google.com** — Orquestrador Serverless de Alta Disponibilidade (contêiner de execução gerenciado, OAuth2 transparente, cotas de execução, deploy atômico)
- **Google Colab** — Laboratório de dados para análise preditiva de demanda, prototipagem de oráculos via Gemini API e validação em larga escala via pandas/numpy

Para projetos de grande escala como o SGTE (~63 mil linhas) e SGAE (~135 mil linhas), a ferramenta **CLASP** (Command Line Apps Script Projects) viabiliza desenvolvimento local com VS Code, versionamento Git e CI/CD via GitHub Actions.

---

## 7. O ACP como Síntese Unificadora

O **Agent Communication Protocol** da IBM subsume os formatos MCP e A2A em um modelo de mensagens unificado, adicionando:

- **ACNBP** — Negociação e vínculo de capacidades com compromisso contratual (SLA digital)
- **ANS** — Agent Name Service, análogo ao DNS para agentes
- **Federação** — Governança distribuída entre domínios

---

## 8. O Algoritmo de Tradução Semântica

O núcleo do NL-Agent é um **algoritmo de tradução em 5 etapas**:

1. **EXTRAIR** — Análise semântica da mensagem de origem
2. **IDENTIFICAR** — Consulta oracular para correspondências ontológicas
3. **TRANSFORMAR** — Mapeamento direto, composto ou aproximação com aviso
4. **VALIDAR** — Verificação de consistência via inferência NL
5. **RETORNAR** — Mensagem traduzida com metadados de confiança

**Propriedade formal**: Para toda mensagem `m`, a tradução `T(m)` satisfaz `|S(m) − S(T(m))| ≤ ε`, onde `ε → 0` quando as ontologias são isomórficas.

---

## 9. Camada de Persistência: Sheets-as-Database

O Google Sheets funciona como **banco de dados relacional simplificado** na SEDF:

| Componente         | Equivalente Tradicional  | Protocolo |
|--------------------|--------------------------|-----------|
| `SpreadsheetApp`   | Driver de banco de dados | —         |
| `SheetRepository`  | ORM / DAO                | MCP       |
| `PropertiesManager`| Variáveis de ambiente    | MCP       |
| `CacheService`     | Redis / Memcached        | MCP       |
| `COLUMN_SCHEMAS`   | Migrations de schema     | ACP       |
| Abas (Sheets)      | Tabelas de banco         | —         |

---

## 10. O Paradoxo do Poder versus Controle na Gestão Educacional

A implementação prática revela o **Paradoxo do Poder vs. Controle**: gestores educacionais reconhecem a capacidade superior dos workflows autônomos para processar milhares de registros, mas relatam simultaneamente uma sensação de **perda de agência pessoal** sobre decisões que afetam diretamente estudantes e comunidades.

No ambiente escolar, esse paradoxo é amplificado por três fatores:

1. **Responsabilidade legal**: O gestor é pessoalmente responsável pela execução orçamentária — uma decisão algorítmica incorreta sobre o FUNDEB pode gerar glosas que comprometem o financiamento de toda uma escola
2. **Impacto social direto**: Otimizações de rotas de transporte afetam crianças reais em comunidades vulneráveis — a eficiência não pode prevalecer sobre a equidade
3. **Confiança institucional**: A credibilidade do sistema educacional perante pais, professores e órgãos de controle depende da percepção de que decisões são tomadas com discernimento humano, não delegadas cegamente a algoritmos

A solução proposta é o paradigma da **Autonomia Supervisionada**:

> "Não é um compromisso transitório, mas um modelo sociotécnico deliberado que busca simbiose produtiva e sustentável entre agência humana e poder computacional. O gestor torna-se um orquestrador, não um subordinado da máquina."

O profissional de educação torna-se um **"gerente de agentes"**: define objetivos pedagógicos e logísticos, delega execução operacional a agentes especializados, monitora indicadores em dashboards transparentes e intervém em pontos críticos — como a validação de exceções orçamentárias, a arbitragem de conflitos entre rotas e a aprovação de cardápios nutricionais.

### Equação de Confiança

```
T = λ₁·E_x + λ₂·S_e + λ₃·P_v + λ₄·I_v
```

| Variável | Significado             | Exemplo Educacional |
|----------|-------------------------|---------------------|
| T        | Confiança total         | Disposição do gestor em delegar decisões ao sistema |
| E_x      | Explicabilidade         | Dashboard que mostra *por que* uma rota foi escolhida, não apenas *qual* |
| S_e      | Segurança               | Garantia de que dados de menores de idade estão protegidos (LGPD) |
| P_v      | Previsibilidade         | Comportamento consistente do sistema frente a cenários similares |
| I_v      | Identidade verificável  | Certificação de que o agente que processou dados é autorizado |

---

## 11. Validação Empírica na SEDF

### 11.1 Escala Operacional

| Categoria                  | Métrica                | Valor    |
|----------------------------|------------------------|----------|
| Volume de Dados            | Alunos cadastrados     | 9.000+   |
|                            | Linhas de transporte   | 300+     |
|                            | Escolas atendidas      | 680+     |
|                            | Viagens diárias        | ~1.200   |
| Processamento Assíncrono   | Registros presença/dia | ~18.000  |
|                            | Cálculos de rota/dia   | ~600     |
|                            | Relatórios gerados/dia | ~50      |
| Latência                   | Jobs críticos          | < 5s     |
|                            | Jobs normais           | < 30s    |
|                            | Relatórios complexos   | 2–5 min  |

### 11.2 Quatro Pilares do Impacto Institucional

1. **Fortalecimento das Capacidades Institucionais** — Dados processados em silos seguros via IIFE, mas integrados semanticamente; risco de glosas FUNDEB reduzido em 97%. Unidades escolares ganham autonomia na geração de relatórios, reduzindo dependência da Coordenação Regional e fortalecendo a gestão democrática
2. **Interoperabilidade como Governança** — Agentes A2A com ciclos assíncronos substituem monolitos centralizadores; resposta a auditorias de dias para horas. A fragmentação entre transporte, alimentação e frequência dá lugar a um ecossistema integrado onde o "aluno" é uma entidade unificada semanticamente
3. **Automação de Pesquisa Operacional** — Ciclo completo (coleta via agentes especializados → validação oracular → análise de padrões → síntese em dashboards) populando informações estratégicas em tempo real, transformando dados brutos e fragmentados em conhecimento acionável para gestores
4. **Equidade e Inclusão** — A auditabilidade algorítmica garante que otimizações de rotas, alocações alimentares e distribuição de recursos não desfavoreçam sistematicamente populações vulneráveis; cada decisão é rastreável e pode ser reconstituída para análise de impacto social

---

## 12. Considerações Éticas na Educação Pública

| Princípio         | Aplicação no Framework                                                          | Impacto Educacional |
|-------------------|----------------------------------------------------------------------------------|---------------------|
| Transparência     | Notificação explícita (`⊥`) quando tradução introduz incerteza                  | Gestores sabem *quando* e *por que* uma decisão algorítmica é incerta, podendo intervir |
| Responsabilidade  | Autonomia Supervisionada como modelo de atribuição                               | Cadeia de decisão sempre rastreável de volta a um responsável humano, protegendo gestores juridicamente |
| Privacidade       | Isolamento MCP + minimização de dados conforme LGPD (475 mil estudantes)         | Dados de menores de idade transitam entre agentes em silos seguros, com acesso controlado |
| Viés              | Mitigação via TRiSM, especialmente em rotas e alocação alimentar                | Populações vulneráveis protegidas de exclusão algorítmica sistemática |
| Equidade          | Auditoria de impacto social integrada ao EventStore imutável                      | Decisões sobre transporte e alimentação são verificáveis quanto à distribuição equitativa |

No contexto educacional, a ética não é um apêndice — é um **requisito de design**. A proteção de dados de 475 mil estudantes que transitam entre agentes de diferentes domínios exige que o isolamento contextual via IIFEs inclua mecanismos de **minimização de dados** e **anonimização**. Viéses na otimização de rotas de transporte escolar ou na alocação de recursos alimentares podem ter consequências reais sobre a **equidade no acesso à educação pública**: uma otimização que priorize custos pode sistematicamente desfavorecer alunos de zonas rurais ou comunidades de difícil acesso.

A cadeia de responsabilidade em sistemas multi-agente complexos — onde um agente orquestrador delega tarefas a agentes especializados que, por sua vez, utilizam oráculos LLM para tradução semântica — torna-se especialmente relevante quando decisões algorítmicas impactam **populações tuteladas** (menores de idade). O framework de Autonomia Supervisionada proposto oferece uma abordagem pragmática, mantendo o humano como árbitro final em decisões com consequências sociais.

---

## 13. Implicações Teóricas e Práticas

### 13.1 Contribuições Teóricas

1. **Formalização do Oráculo Epistêmico** — LLMs como agentes epistêmicos que resolvem ambiguidades ontológicas em tempo real, ampliando o arcabouço clássico de Sistemas Multiagentes (Wooldridge, 2009)
2. **Camada de Abstração baseada em NL** — Espaço semântico compartilhado que permite tradução dinâmica entre esquemas de protocolos heterogêneos
3. **Taxonomia de capacidades agnóstica** — Modelo unificado que permite integrar novos protocolos sem reengenharia dos mapeamentos existentes

### 13.2 Diretrizes Práticas

- **Adoção progressiva de protocolos** — Começar pelo MCP para isolamento contextual via IIFE, evoluir para A2A na coordenação entre domínios
- **Investimento em infraestrutura semântica** — Ontologias bem definidas facilitam a integração; na SEDF, modelagem de Transporte, Alimentação e Frequência reduziu erros para < 0,3%
- **LLMs como oráculos sob governança rigorosa** — Usar framework TRiSM para mitigar alucinações e assegurar supervisão humana em decisões críticas
- **IIFE como unidade de encapsulamento agêntico** — Isolamento contextual, interface pública controlada e substituibilidade sem impacto sistêmico

---

## 14. Trabalhos Futuros

1. **Aprendizado de mapeamentos ontológicos** — Uso de técnicas de ML para derivar alinhamentos automaticamente, reduzindo o custo de configuração para novos domínios
2. **Oráculos distribuídos** — Distribuição da carga entre múltiplos LLMs potencialmente heterogêneos, com consenso semântico para escalabilidade horizontal
3. **Verificação formal** — Ferramentas que certifiquem *a priori* que traduções entre protocolos preservam invariantes semânticas críticas
4. **Extensão ANP** — Descoberta descentralizada de agentes via DIDs (Decentralized Identifiers) e credenciais verificáveis

---

## 15. Parceria UnDF-SEDF: Validação no Ecossistema de Inovação Educacional

A **Universidade do Distrito Federal (UnDF)** atua como parceira estratégica na validação empírica, configurando-se como **Universidade Empreendedora** fundamentada na tríplice missão: ensino, pesquisa e Terceira Missão (transferência tecnológica e engajamento social). A parceria transcende a tradicional oferta de mão de obra de estágio, representando um **protocolo de governança** onde a inteligência humana supervisiona e refina a inteligência artificial.

### Modelo de Estagiário como Human-in-the-Loop

Na arquitetura proposta, o discente da UnDF ocupa o papel funcional de **"Human-in-the-Loop de Segunda Ordem"**:

- Enquanto agentes MCP/A2A processam a sintaxe e pragmática das operações em escala (18.000 registros/dia)
- O estagiário realiza **auditoria ontológica** — verifica que "aluno" no SGTE e "beneficiário" no SGAE referem-se à mesma entidade
- Conduz a **evolução dos oráculos epistêmicos** — ajusta prompts, refina heurísticas de roteamento LLM/LRM, valida novas correspondências ontológicas
- Fecha o ciclo de retroalimentação necessário para evitar degradação semântica do sistema em larga escala

Esse modelo forma profissionais que transcendem o perfil de desenvolvedor, emergindo como **"gerentes de agentes"** — aptos para auditoria de oráculos epistêmicos, validação FUNDEB/PDDE e orquestração de workflows híbridos humano-IA.

### Alinhamento com a Aprendizagem Baseada em Problemas (ABP)

A escolha pedagógica da ABP não é acidental: ao enfrentar problemas reais de orquestração multi-agente em sistemas que atendem 475.000 estudantes, o estagiário desenvolve competências que a instrução convencional não oferece — pensamento sistêmico, governança algorítmica, literacia de dados e a capacidade de questionar criticamente decisões automatizadas que afetam populações vulneráveis.

### Tríplice Hélice em Território

| Hélice      | Parceiros                               | Interação                                      |
|-------------|------------------------------------------|--------------------------------------------------|
| Universidade| UnDF, UnB                                | Geração de conhecimento, formação de RH, P&D    |
| Governo     | GDF, FAPDF, RNP, SERPRO                  | Financiamento (R$ 56M FAPDF), infraestrutura     |
| Indústria   | BioTIC, Sebrae, Cotidiano Aceleradora    | Demanda por inovação, transferência tecnológica   |

---

## 16. Síntese da Exegese

O framework NL-Agent não é meramente um produto de software — é uma **tese epistêmica materializada em código**, orientada fundamentalmente pela necessidade de transformar a gestão educacional pública:

1. A **Lógica Natural** fundamenta a inferência e preservação semântica — garantindo que a comunicação entre agentes respeite as relações de significado que sustentam decisões educacionais
2. Os **protocolos (MCP, A2A, ANP, ACP)** são manifestações complementares de um paradigma de interoperabilidade — eliminando os silos de inteligência que fragmentam a gestão escolar
3. Os **oráculos epistêmicos** (LLMs/LRMs) são mediadores semânticos que superam limitações formais — com a dualidade cognitiva refletindo a necessidade real de velocidade na interface e rigor no orçamento
4. A **Autonomia Supervisionada** equilibra poder computacional e agência humana — elevando o gestor a orquestrador, não subordinando-o à máquina
5. A **validação empírica** na SEDF (215.000 LOC, 12.500 interações, 93,6% preservação) comprova a viabilidade prática em escala real
6. A **parceria UnDF-SEDF** materializa a Terceira Missão universitária via Human-in-the-Loop de Segunda Ordem, formando uma nova geração de gestores-orquestradores
7. A **equidade educacional** é um princípio de design: auditabilidade, rastreabilidade e mitigação de viés são integradas ao nível protocolar, protegendo 475.000 estudantes
8. A **democratização tecnológica** — via infraestrutura acessível (Sheets-as-Database, Apps Script) — garante que a sofisticação arquitetural não exija sofisticação financeira, tornando a solução replicável em qualquer rede de ensino

> *"A convergência dos protocolos MCP, A2A e ACP não é meramente técnica — representa uma transformação paradigmática na forma como concebemos a comunicação entre entidades artificiais. Assim como a linguagem natural evoluiu para permitir a cooperação humana complexa, estes protocolos estabelecem as fundações para uma nova era de colaboração entre agentes artificiais, onde a compreensão mútua transcende diferenças sintáticas e ontológicas."*
>
> *"Padrões de código legados, analisados sob a lente epistemológica de protocolos como MCP, A2A e ACP, revelam-se como microcosmos fractais de agência que otimizam intuições desenvolvimentais práticas."*
