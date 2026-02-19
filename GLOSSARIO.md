# 📚 GLOSSÁRIO — Framework NL-Agent

> Glossário consolidado de termos técnicos, acrônimos, definições formais e referências conceituais do framework NL-Agent para interoperabilidade semântica multi-agente.

---

## A

### A2A — Agent-to-Agent Protocol
Protocolo de comunicação peer-to-peer entre agentes autônomos, desenvolvido pela Google. Estrutura interações via Agent Cards e ciclos de tarefas assíncronas (`submitted → working → completed/failed/canceled`). No framework NL-Agent, opera na camada de comunicação direta entre agentes de domínio.

### ABECI — Associação Brasileira de Educação em Ciência da Informação
Referência para alinhamento de competências no estágio de Ciência da Informação (UnDF-SEDF).

### ABP — Aprendizagem Baseada em Problemas
Metodologia pedagógica ativa adotada pela UnDF, onde o processo de aprendizagem é iniciado por problemas complexos extraídos de contextos reais.

### ACP — Agent Communication Protocol
Protocolo híbrido proposto pela IBM que subsume formatos MCP e A2A em modelo de mensagens unificado, com suporte a federação, ACNBP e ANS.

### ACNBP — Agent Capability Negotiation and Binding Protocol
Subprotocolo do ACP (Huang et al., 2025b) que define processo formal de 10 passos para negociar, verificar e comprometer-se com execução de capacidades de forma criptograficamente segura. Cria SLAs digitais entre agentes.

### Agent Card
Documento JSON Schema que representa a identidade declarativa de um agente A2A, incluindo nome, descrição, URL, capacidades, skills e modos de autenticação.

### Agent Description Document
Documento ANP que combina metadados técnicos com descrições em linguagem natural, viabilizando busca híbrida (estruturada + semântica).

### Alinhamento Ontológico
Processo de estabelecer correspondências `M = {⟨e₁, e₂, r, c⟩}` entre entidades de ontologias distintas, onde `r` é a relação semântica e `c` o grau de confiança.

### ANP — Agent Network Protocol
Protocolo descentralizado para descoberta e estabelecimento de confiança em redes abertas de agentes, usando DIDs e Verifiable Credentials.

### ANS — Agent Name Service
Infraestrutura análoga ao DNS para agentes, traduzindo identificadores legíveis em localizações de rede e metadados de capacidade, com PKI nativa integrada (Raskar et al., 2025).

### Autonomia Supervisionada
Paradigma sociotécnico onde o humano atua como "gerente de agentes" — define objetivos pedagógicos e logísticos, delega execução operacional, monitora indicadores em dashboards e intervém em pontos críticos de decisão (validação de exceções orçamentárias, arbitragem de rotas de transporte). Não é substituição nem controle manual total, mas simbiose deliberada entre agência humana e poder computacional.

---

## B

### Bridge Bidirecional
Padrão de integração do NL-Agent que traduz mensagens entre dois protocolos em ambas as direções, preservando semântica via consulta oracular.

### BioTIC — Parque Tecnológico de Brasília
Parque tecnológico parceiro da UnDF, materializando a tríplice hélice universidade-governo-indústria no Distrito Federal.

---

## C

### CacheService
Agente de infraestrutura MCP que implementa cache com chaves padronizadas e TTL configurável, equivalente funcional ao Redis/Memcached no ecossistema Google Apps Script.

### CLASP — Command Line Apps Script Projects
Ferramenta CLI para desenvolvimento local de Google Apps Script, permitindo versionamento Git e deploy automatizado via `clasp push`.

### COLUMN_SCHEMAS
Definições formais de estrutura de cada aba do Google Sheets — nomes de colunas, tipos e índices — funcionando como migrations de schema.

### Condições de Felicidade
Requisitos para que um ato de fala seja bem-sucedido: Conteúdo Proposicional, Preparatória, Sinceridade e Essencial.

### ConfigManager
Agente de infraestrutura MCP (Config Oracle) com 23 referências no codebase, responsável por configurações contextuais.

### Context Keeper
Agente teórico MCP responsável por manter o estado do contexto. Implementado como `SessionManager` em produção.

### CoT — Chain-of-Thought
Técnica de raciocínio em cadeia utilizada por LRMs para garantir que respostas não sejam meramente probabilísticas, mas logicamente derivadas.

### CRE-PP — Coordenação Regional de Ensino do Plano Piloto
Unidade da gestão educacional onde os sistemas multi-agentes (SGTE/SGAE) foram validados empiricamente.

---

## D

### DIDs — Decentralized Identifiers
Identificadores descentralizados (W3C) que permitem identidade criptográfica única para cada agente, independente de servidor central de autenticação.

### Disclosure Mínimo
Princípio de que agentes provam atributos sem expor dados sensíveis, alinhado à LGPD. No contexto educacional, garantir que agentes possam verificar a elegibilidade de um aluno para transporte escolar sem revelar seus dados pessoais completos.

### Democratização Tecnológica
Princípio arquitetural de que sistemas multi-agentes robustos podem ser construídos sobre infraestrutura acessível (Google Sheets, Apps Script), eliminando barreiras de adoção para secretarias de educação com orçamentos limitados e tornando a solução replicável em qualquer rede de ensino.

---

## E

### EventBus
Implementação do padrão Pub/Sub para comunicação A2A desacoplada entre agentes no backend. Exemplo: quando o agente de transporte notifica um incidente, o evento é propagado para os agentes de frequência e alimentação sem acoplamento direto.

### Equidade Educacional
Princípio de design que garante que decisões algorítmicas sobre rotas de transporte, distribuição alimentar e alocação orçamentária não desfavoreçam sistematicamente populações vulneráveis. Implementado via auditabilidade no EventStore e mitigação de viés no TRiSM.

### EventStore
Mecanismo de persistência imutável e sequencial de eventos, permitindo auditoria forense e replay para recuperação de estado.

---

## F

### FIPA-ACL — Foundation for Intelligent Physical Agents - Agent Communication Language
Linguagem de comunicação de 2ª geração para agentes, predecessora dos protocolos atuais.

### FUNDEB — Fundo de Manutenção e Desenvolvimento da Educação Básica
Fundo público cujas regras orçamentárias (e.g., regra de 70%) são verificadas por Oráculos Raciocinadores no framework.

---

## G

### Gerente de Agentes
Novo papel do profissional na era da Autonomia Supervisionada: define objetivos, delega, monitora execuções e arbitra exceções.

### Glosa
Rejeição de despesas em prestações de contas públicas (FUNDEB/PDDE) por inconsistência ou irregularidade. Reduzida em 97% pelo framework.

---

## H

### Heurística de Roteamento
Mecanismo do Agente Orquestrador que classifica tarefas por complexidade e as direciona para LLMs (transformação, resumo — System 1) ou LRMs (planejamento, aritmética, compliance FUNDEB — System 2), evitando o anti-padrão do "Monolito de Modelo".

### Human-in-the-Loop
Modelo de supervisão humana contínua sobre sistemas de IA. Na parceria universidade-campo, o estagiário atua como "Human-in-the-Loop de Segunda Ordem", auditando traduções semânticas e evoluindo oráculos epistêmicos.

---

## I

### IIFE — Immediately Invoked Function Expression
Padrão JavaScript de execução imediata que encapsula estado privado e expõe interface pública. No framework, é a **unidade básica de agência MCP** — um isomorfismo funcional do isolamento contextual do protocolo.

### Infodemia
Proliferação excessiva de dados digitais que sobrecarrega a capacidade cognitiva humana (Zhang et al., 2024).

### Interoperabilidade Semântica
Capacidade de sistemas heterogêneos trocarem informações preservando significado, intenção e contexto. Taxa alcançada: 93,6%. No contexto educacional, garante que "aluno" no sistema de transporte, "beneficiário" no sistema de alimentação e "matrícula" no sistema de frequência refiram-se à mesma entidade.

### Inteligência Institucional
Capacidade de uma organização educacional de aprender, adaptar-se e decidir de forma integrada. Transcende a mera automação operacional, permitindo que gestores transformem dados brutos e fragmentados em conhecimento acionável para planejamento estratégico.

### IoA — Internet of Agents
Visão futura de uma rede global de agentes autônomos interoperáveis, análoga à Internet atual para humanos (Wang et al., 2025).

---

## J

### JobQueue
Implementação do Message Broker A2A na SEDF. Fila priorizada com estados de tarefa, retry automático e máximo de 3 tentativas por padrão.

### JSON-RPC 2.0
Protocolo de transporte utilizado pelo MCP para comunicação bidirecional entre clientes e servidores.

---

## K

### KQML — Knowledge Query and Manipulation Language
Linguagem de comunicação de 1ª geração para agentes, predecessora da FIPA-ACL.

---

## L

### LGPD — Lei Geral de Proteção de Dados (Lei nº 13.709/2018)
Legislação brasileira de proteção de dados pessoais, relevante para agentes que processam informações de 475.000 estudantes.

### LLM — Large Language Model
Modelo de linguagem de grande escala que opera como "System 1" (rápido, intuitivo). Exemplos: GPT-4o, Gemini Flash.

### LRM — Large Reasoning Model
Modelo de raciocínio de grande escala que opera como "System 2" (lento, deliberativo). Exemplos: o1, R1, Gemini 1.5 Pro com thinking.

### Lógica Natural (NL)
Epistemologia que fundamenta o framework, enfatizando inferência intuitiva e preservação de relações semânticas naturais, incluindo inferências monotônicas e não-monotônicas.

---

## M

### MCP — Model Context Protocol
Protocolo cliente-servidor para integração de modelos de linguagem com fontes externas. Topologia: Host → Clientes → Servidores. Primitivos: Resources, Tools, Prompts.

### Monolito Administrativo
Anti-padrão onde um sistema único concentra todas as funções de gestão educacional, gerando indisponibilidade total quando falha e impossibilidade de atualização parcial. Solução: decomposição em agentes por domínio (transporte, alimentação, frequência).

### Monolito de Modelo
Anti-padrão que trata toda IA como igual, ignorando a dualidade LLM/LRM e suas implicações de latência, custo e precisão. No contexto educacional, leva a usar LLMs para cálculos FUNDEB (risco de alucinação) ou LRMs para gerar resumos de reuniões (custo proibitivo e latência desnecessária).

---

## N

### NASA-TLX — NASA Task Load Index
Instrumento de avaliação de carga cognitiva, adaptado no framework para comparar workflows autônomos, híbridos e manuais em gestão educacional.

### NL-Agent
Nome do framework proposto nesta dissertação para interoperabilidade semântica entre protocolos MCP, A2A, ANP e ACP via Lógica Natural.

---

## O

### Ontologia Computacional
Tupla formal `O = ⟨C, R, I, A⟩` que captura conceitos, relações, instâncias e axiomas de um domínio de conhecimento.

### Oráculo Epistêmico
Tupla `O = ⟨D, Q, R, φ⟩` que responde consultas sobre domínios específicos sem revelar seu mecanismo interno. Propriedades: Consistência, Completude Parcial, Opacidade.

### Oráculo Ontológico
Tipo de oráculo que traduz conceitos entre ontologias distintas.

### Oráculo Pragmático
Tipo de oráculo que adapta mensagens ao contexto específico do receptor.

### Oráculo Semântico
Tipo de oráculo que preserva significado durante traduções entre protocolos.

---

## P

### PDDE — Programa Dinheiro Direto na Escola
Programa federal de repasse financeiro direto às escolas, cujas prestações de contas são automatizadas pelo framework.

### PNAE — Programa Nacional de Alimentação Escolar
Programa que exige que cardápios atendam 30% das necessidades nutricionais dos alunos — verificação feita pelo Agente Nutricional (LRM).

### Preservação Semântica
Propriedade formal onde `|S(m) − S(T(m))| ≤ ε`. Taxa média alcançada: 93,6% (Tabela 25).

### PropertiesManager
Agente MCP que utiliza `PropertiesService` do Apps Script como repositório de configurações, equivalente a variáveis de ambiente.

---

## S

### SBC — Sociedade Brasileira de Computação
Referência para matrizes de competência no estágio de Ciência da Computação (UnDF-SEDF).

### SEDF — Secretaria de Estado de Educação do Distrito Federal
Campo empírico de validação do framework. Gestora de 680 escolas e 475.000 estudantes no DF.

### SemanticTranslator
Classe de referência do algoritmo de tradução semântica em Python, com 5 etapas: extração → consulta oracular → transformação → validação NL → retorno com metadados.

### SessionManager
Implementação do Context Keeper (MCP) na SEDF. 12 referências no codebase. Preserva e propaga contexto do servidor público entre interações.

### SGAE — Sistema de Gestão da Alimentação Escolar
Sistema multi-agente para gestão de cardápios e estoques em 680 escolas (~135.000 LOC).

### SGTE — Sistema de Gestão do Transporte Escolar
Sistema multi-agente para gestão de rotas e incidentes (~63.000 LOC, 9.000+ alunos, 300+ linhas).

### SheetRepository
Abstração CRUD sobre `SpreadsheetApp` do Google Apps Script. Equivalente funcional a um ORM/DAO no ecossistema MCP.

### Sheets-as-Database
Abordagem arquitetural onde Google Sheets funciona como banco de dados relacional simplificado, com cada aba correspondendo a uma entidade de domínio.

### SNI — Sistema Nacional de Inovação
Paradigma que define a inovação como propriedade emergente de um sistema complexo de relações entre instituições públicas e privadas.

### SWEBOK — Software Engineering Body of Knowledge
Corpo de conhecimento em engenharia de software usado como referência para competências profissionais.

### Silos de Inteligência
Sistemas isolados (matrícula, frequência, transporte, alimentação) que não compartilham contexto semântico. Um "aluno" é representado de formas divergentes em cada sistema, gerando inconsistências que podem resultar em glosas no FUNDEB. O framework elimina esses silos via interoperabilidade semântica.

---

## T

### TPA — Teoria do Principal-Agente
Framework econômico aplicado à relação humano-IA, onde assimetrias de informação e risco moral emergem quando tarefas são delegadas a agentes autônomos.

### TRiSM — Trust, Risk, and Security Management
Framework de governança para sistemas de IA proposto por Raza et al. (2025), adaptado para oráculos epistêmicos no NL-Agent.

### Tríplice Hélice
Modelo de inovação baseado na interação universidade-governo-indústria, materializado na parceria UnDF-BioTIC-SEDF.

---

## U

### UnDF — Universidade do Distrito Federal
Universidade empreendedora parceira da SEDF, projetada como paradigma de inovação com ABP e tríplice hélice.

### UnifiedCapability
Interface TypeScript do framework que define modelo de capacidades agnóstico a protocolo, com identificação, semântica, interface, proveniência e restrições.

---

## V

### ValidationService
Agente de validação autônomo que verifica integridade de dados em tempo real, atuando como "cidadão de primeira classe" no ecossistema. Implementa a Heurística 3: intercepta preventivamente transações que violem regras orçamentárias do FUNDEB/PDDE, atuando como auditor em tempo real que blinda gestores contra glosas.

### VCs — Verifiable Credentials
Credenciais verificáveis que permitem a agentes provarem atributos sem expor dados sensíveis, complementando a identidade DID.

---

## Definições Formais (Resumo)

| #  | Nome                     | Formulação                                      |
|----|--------------------------|--------------------------------------------------|
| D1 | Operador de Conhecimento | `K_a(φ) ≡ "agente a conhece φ"`                 |
| D2 | Ontologia Computacional  | `O = ⟨C, R, I, A⟩`                              |
| D3 | Alinhamento Ontológico   | `M = {⟨e₁, e₂, r, c⟩}`                         |
| D4 | Oráculo Epistêmico       | `O = ⟨D, Q, R, φ⟩`                              |
| D5 | Negociação Semântica     | `N = ⟨m₁, m₂, ..., mₙ⟩`                        |
| T1 | Aproximação Oracular     | `lim P(L(q) = O(q)) = 1 − ε`                    |
| T2 | Preservação Semântica    | `\|S(m) − S(T(m))\| ≤ ε`                        |
| T3 | Completude do Mapeamento | `∀c ∈ Cap(P₁), ∃c' ∈ Cap(P₂): M(c) = c' ∨ ⊥`  |
| P1 | Complexidade de Tradução | `O(n × log(\|O\|) + n × T_oracle)`              |
