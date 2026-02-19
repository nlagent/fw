/**
 * unified_capability.ts — Modelo de Capacidades Unificado (NL-Agent Framework)
 *
 * Interface agnóstica a protocolo para representar capacidades de agentes,
 * permitindo tradução bidirecional entre MCP Tools, A2A Skills e ACP Actions.
 *
 * Referência: seção 5.1 da dissertação.
 * Autor: Framework NL-Agent, 2026
 */

// ---------------------------------------------------------------------------
// Tipos Base
// ---------------------------------------------------------------------------

/** Protocolos suportados pelo framework */
type SupportedProtocol = "MCP" | "A2A" | "ACP";

/** Tipos semânticos de capacidades */
type SemanticType = "resource" | "action" | "template" | "composite";

/** Relações semânticas entre entidades ontológicas */
type SemanticRelation = "≡" | "⊑" | "⊒" | "⊥";

/** JSON Schema simplificado */
interface JSONSchema {
  type: string;
  properties?: Record<string, JSONSchema>;
  required?: string[];
  description?: string;
  items?: JSONSchema;
  enum?: string[];
}

// ---------------------------------------------------------------------------
// Modelo de Capacidades Unificado
// ---------------------------------------------------------------------------

/** Referência a ontologia externa */
interface OntologyReference {
  ontologyId: string;
  conceptId: string;
  relation: SemanticRelation;
  confidence: number; // 0.0 a 1.0
}

/** Registro de transformação aplicada */
interface TransformationEntry {
  timestamp: string;
  sourceProtocol: SupportedProtocol;
  targetProtocol: SupportedProtocol;
  transformationType: "direct" | "composite" | "approximate";
  semanticLoss: number; // 0.0 = sem perda
  description: string;
}

/** Expressão lógica para pré/pós-condições e invariantes */
interface LogicalExpression {
  expression: string;
  language: "nl" | "javascript" | "json-logic";
  description: string;
}

/**
 * UnifiedCapability — Modelo agnóstico de capacidades.
 *
 * Mapeia para:
 *   MCP: Tool (name, description, inputSchema)
 *   A2A: Skill (id, description, tags, examples)
 *   ACP: Action (id, description, parameters)
 */
interface UnifiedCapability {
  // --- Identificação ---
  id: string;
  name: string;
  version: string;

  // --- Semântica ---
  description: string;
  semanticType: SemanticType;
  ontologyMapping: OntologyReference[];

  // --- Interface ---
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;

  // --- Proveniência ---
  provenance: {
    sourceProtocol: SupportedProtocol;
    originalDefinition: unknown;
    transformationLog: TransformationEntry[];
  };

  // --- Restrições ---
  constraints: {
    preconditions: LogicalExpression[];
    postconditions: LogicalExpression[];
    invariants: LogicalExpression[];
  };
}

// ---------------------------------------------------------------------------
// Conversores de Protocolo
// ---------------------------------------------------------------------------

/** Representação de uma Tool MCP */
interface MCPTool {
  name: string;
  description: string;
  inputSchema: JSONSchema;
}

/** Representação de uma Skill A2A */
interface A2ASkill {
  id: string;
  description: string;
  tags: string[];
  examples: string[];
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;
}

/** Representação de uma Action ACP */
interface ACPAction {
  id: string;
  description: string;
  parameters: JSONSchema;
  resultSchema: JSONSchema;
  sla?: { maxLatencyMs: number; guaranteedAvailability: number };
}

/**
 * Converte MCP Tool → UnifiedCapability
 */
function fromMCPTool(tool: MCPTool): UnifiedCapability {
  return {
    id: tool.name,
    name: tool.name,
    version: "1.0.0",
    description: tool.description,
    semanticType: "action",
    ontologyMapping: [],
    inputSchema: tool.inputSchema,
    outputSchema: { type: "object", description: "MCP tool result" },
    provenance: {
      sourceProtocol: "MCP",
      originalDefinition: tool,
      transformationLog: [],
    },
    constraints: {
      preconditions: [],
      postconditions: [],
      invariants: [],
    },
  };
}

/**
 * Converte UnifiedCapability → A2A Skill
 */
function toA2ASkill(cap: UnifiedCapability): A2ASkill {
  return {
    id: cap.id,
    description: cap.description,
    tags: cap.ontologyMapping.map((m) => m.conceptId),
    examples: [],
    inputSchema: cap.inputSchema,
    outputSchema: cap.outputSchema,
  };
}

/**
 * Converte UnifiedCapability → ACP Action
 */
function toACPAction(cap: UnifiedCapability): ACPAction {
  return {
    id: cap.id,
    description: cap.description,
    parameters: cap.inputSchema,
    resultSchema: cap.outputSchema,
  };
}

/**
 * Converte UnifiedCapability → MCP Tool
 */
function toMCPTool(cap: UnifiedCapability): MCPTool {
  return {
    name: cap.id,
    description: cap.description,
    inputSchema: cap.inputSchema,
  };
}

// ---------------------------------------------------------------------------
// Exemplo de Uso
// ---------------------------------------------------------------------------

const exampleTool: MCPTool = {
  name: "semantic_search",
  description: "Busca semântica em documentos do domínio educacional",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string", description: "Termo de busca" },
      limit: { type: "string", description: "Máximo de resultados" },
    },
    required: ["query"],
  },
};

// MCP → Unified → A2A
const unified = fromMCPTool(exampleTool);
const skill = toA2ASkill(unified);
const action = toACPAction(unified);

export type {
  UnifiedCapability,
  MCPTool,
  A2ASkill,
  ACPAction,
  SupportedProtocol,
  SemanticType,
  SemanticRelation,
  OntologyReference,
  TransformationEntry,
  LogicalExpression,
  JSONSchema,
};

export { fromMCPTool, toA2ASkill, toACPAction, toMCPTool };
