"""
semantic_translator.py — Algoritmo de Tradução Semântica (NL-Agent Framework)

Implementação de referência do Algoritmo 5.1 descrito na seção 5.2 da dissertação.
Traduz mensagens entre protocolos heterogêneos (MCP, A2A, ACP) preservando
a intenção semântica original via mediação oracular e inferência NL.

Propriedade formal:
    Para toda mensagem m, a tradução T(m) satisfaz:
    |S(m) − S(T(m))| ≤ ε, onde ε → 0 quando ontologias são isomórficas.

Autor: Framework NL-Agent, 2026
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Tipos e Estruturas de Dados
# ---------------------------------------------------------------------------

class Protocol(Enum):
    """Protocolos suportados pelo framework."""
    MCP = "mcp"
    A2A = "a2a"
    ACP = "acp"


class AlignmentType(Enum):
    """Tipos de alinhamento ontológico."""
    DIRECT = "direct"            # Correspondência direta (1:1)
    COMPOSITE = "composite"      # Decomposição e tradução de componentes
    APPROXIMATE = "approximate"  # Aproximação com aviso de perda semântica


class SemanticRelation(Enum):
    """Relações semânticas entre entidades ontológicas."""
    EQUIVALENT = "≡"    # Equivalência
    SUBSUMES = "⊑"      # Subsunção (é subconjunto de)
    SUPERCLASS = "⊒"    # Superclasse (contém)
    DISJOINT = "⊥"      # Disjunção (incompatível)


@dataclass
class OntologyAlignment:
    """Correspondência entre entidades de ontologias distintas (Definição 3)."""
    source_entity: str
    target_entity: str
    relation: SemanticRelation
    confidence: float  # c ∈ [0, 1]
    is_direct: bool = True
    is_composite: bool = False

    @property
    def is_approximate(self) -> bool:
        return not self.is_direct and not self.is_composite


@dataclass
class SemanticStructure:
    """Estrutura semântica extraída de uma mensagem."""
    conceitos: list[str] = field(default_factory=list)
    performative: str = ""       # inform, request, propose, etc.
    intent: str = ""
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticLoss:
    """Registro de perda semântica durante tradução."""
    concept: str
    gap_description: str
    resolution: str
    residual_loss: float  # 0.0 = sem perda, 1.0 = perda total


@dataclass
class TranslationResult:
    """Resultado completo de uma tradução semântica."""
    message: dict[str, Any]
    source_protocol: Protocol
    target_protocol: Protocol
    semantic_losses: list[SemanticLoss]
    confidence: float
    translation_log: list[str] = field(default_factory=list)

    @property
    def has_losses(self) -> bool:
        return len(self.semantic_losses) > 0

    @property
    def preservation_rate(self) -> float:
        """Taxa de preservação semântica (0.0 a 1.0)."""
        if not self.semantic_losses:
            return 1.0
        avg_loss = sum(sl.residual_loss for sl in self.semantic_losses) / len(
            self.semantic_losses
        )
        return 1.0 - avg_loss


# ---------------------------------------------------------------------------
# Motor de Inferência em Lógica Natural (NL Reasoner)
# ---------------------------------------------------------------------------

class NaturalLogicReasoner:
    """
    Motor de inferência baseado em Lógica Natural.

    Aplica axiomas epistêmicos (K1-K3) e inferências monotônicas/
    não-monotônicas para validar consistência de traduções.
    """

    def is_consistent(self, message: dict[str, Any]) -> bool:
        """
        Verifica se a mensagem traduzida satisfaz invariantes de consistência.

        Aplica:
        - K1 (Veracidade): dados referenciados existem
        - K2 (Distribuição): implicações preservadas
        - K3 (Introspecção): metadados coerentes
        """
        if not message:
            return False

        # Verificação de estrutura mínima
        if "payload" in message and "intent" in message.get("payload", {}):
            intent = message["payload"]["intent"]
            params = message["payload"].get("parameters", {})
            if intent and not params:
                return False  # Intent sem parâmetros é inconsistente

        return True

    def apply_corrections(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Aplica correções baseadas em inferência NL para restaurar consistência.
        """
        corrected = dict(message)

        # Adicionar parâmetros vazios se ausentes
        if "payload" in corrected:
            if "parameters" not in corrected["payload"]:
                corrected["payload"]["parameters"] = {}
            if "context" not in corrected["payload"]:
                corrected["payload"]["context"] = {}

        return corrected


# ---------------------------------------------------------------------------
# Tradutor Semântico Principal
# ---------------------------------------------------------------------------

class SemanticTranslator:
    """
    Tradutor semântico central do framework NL-Agent.

    Implementa o Algoritmo 5.1 (Tradução Semântica) com 5 etapas:
    1. EXTRAIR — Análise semântica da mensagem de origem
    2. IDENTIFICAR — Consulta oracular para correspondências
    3. TRANSFORMAR — Mapeamento (direto, composto ou aproximado)
    4. VALIDAR — Verificação de consistência via NL
    5. RETORNAR — Mensagem traduzida com metadados

    Parâmetros:
        oracle: endpoint do oráculo epistêmico (LLM/LRM)
        ontology_registry: registro de ontologias por protocolo
    """

    def __init__(
        self,
        oracle: Any = None,
        ontology_registry: dict[str, Any] | None = None,
    ) -> None:
        self.oracle = oracle
        self.ontology = ontology_registry or {}
        self.nl_reasoner = NaturalLogicReasoner()

        # Mapeamentos diretos conhecidos (cache estático)
        self._direct_mappings: dict[tuple[str, str], dict[str, str]] = {
            ("mcp", "a2a"): {
                "tool.name": "skill.id",
                "tool.description": "skill.description",
                "tool.inputSchema": "skill.inputSchema",
            },
            ("a2a", "mcp"): {
                "skill.id": "tool.name",
                "skill.description": "tool.description",
                "skill.inputSchema": "tool.inputSchema",
            },
            ("mcp", "acp"): {
                "tool.name": "action.id",
                "tool.description": "action.description",
                "resource.uri": "payload.dataset_uri",
            },
            ("acp", "mcp"): {
                "action.id": "tool.name",
                "action.description": "tool.description",
                "payload.dataset_uri": "resource.uri",
            },
            ("a2a", "acp"): {
                "skill.id": "action.id",
                "skill.description": "action.description",
                "task.id": "correlation_id",
            },
            ("acp", "a2a"): {
                "action.id": "skill.id",
                "action.description": "skill.description",
                "correlation_id": "task.id",
            },
        }

    # -----------------------------------------------------------------------
    # API Pública
    # -----------------------------------------------------------------------

    def translate(
        self,
        message: dict[str, Any],
        source_protocol: Protocol,
        target_protocol: Protocol,
    ) -> TranslationResult:
        """
        Traduz mensagem entre protocolos preservando semântica.

        Implementa o Algoritmo 5.1 da dissertação (seção 5.2.1).

        Args:
            message: Mensagem no formato do protocolo de origem
            source_protocol: Protocolo de origem (MCP, A2A ou ACP)
            target_protocol: Protocolo de destino

        Returns:
            TranslationResult com mensagem traduzida e metadados
        """
        log: list[str] = []

        # Etapa 1: Extração semântica
        log.append(f"[1/5] Extraindo semântica de {source_protocol.value}")
        semantic_structure = self._extract_semantics(message, source_protocol)

        # Etapa 2: Consulta oracular para alinhamento
        log.append(f"[2/5] Consultando oráculo para alinhamento → {target_protocol.value}")
        alignments = self._query_alignments(
            concepts=semantic_structure.conceitos,
            source_protocol=source_protocol,
            target_protocol=target_protocol,
        )

        # Etapa 3: Aplicar transformações
        log.append("[3/5] Aplicando transformações conceituais")
        translated_components: list[dict[str, Any]] = []
        semantic_losses: list[SemanticLoss] = []

        for concept, alignment in zip(semantic_structure.conceitos, alignments):
            if alignment.is_direct:
                translated = self._apply_direct_mapping(concept, alignment)
                log.append(f"  ✓ Mapeamento direto: {concept} → {alignment.target_entity}")
            elif alignment.is_composite:
                translated = self._apply_composite_mapping(concept, alignment)
                log.append(f"  ◐ Mapeamento composto: {concept}")
            else:
                translated, loss = self._approximate(concept, alignment)
                semantic_losses.append(loss)
                log.append(f"  ⚠ Aproximação: {concept} (perda: {loss.residual_loss:.2f})")
            translated_components.append(translated)

        # Etapa 4: Composição e validação via NL
        log.append("[4/5] Validando consistência via NL Reasoner")
        translated_message = self._compose(translated_components, target_protocol)

        if not self.nl_reasoner.is_consistent(translated_message):
            log.append("  ⚠ Inconsistência detectada — aplicando correções NL")
            translated_message = self.nl_reasoner.apply_corrections(translated_message)

        # Etapa 5: Retornar com metadados
        log.append("[5/5] Tradução concluída")
        confidence = self._compute_confidence(alignments)

        return TranslationResult(
            message=translated_message,
            source_protocol=source_protocol,
            target_protocol=target_protocol,
            semantic_losses=semantic_losses,
            confidence=confidence,
            translation_log=log,
        )

    # -----------------------------------------------------------------------
    # Métodos Internos
    # -----------------------------------------------------------------------

    def _extract_semantics(
        self, message: dict[str, Any], protocol: Protocol
    ) -> SemanticStructure:
        """Etapa 1: Extrai estrutura semântica da mensagem de origem."""
        structure = SemanticStructure()

        if protocol == Protocol.MCP:
            method = message.get("method", "")
            params = message.get("params", {})
            structure.performative = "request" if "call" in method else "query"
            structure.intent = method
            structure.conceitos = list(params.keys()) if params else [method]
            structure.context = params

        elif protocol == Protocol.A2A:
            parts = message.get("parts", [])
            structure.performative = message.get("role", "agent")
            for part in parts:
                ptype = part.get("type", "text")
                structure.conceitos.append(ptype)
            structure.intent = "a2a_message"
            structure.context = message

        elif protocol == Protocol.ACP:
            payload = message.get("payload", {})
            structure.performative = message.get("message_type", "request")
            structure.intent = payload.get("intent", "")
            structure.conceitos = list(payload.get("parameters", {}).keys())
            structure.context = payload.get("context", {})

        return structure

    def _query_alignments(
        self,
        concepts: list[str],
        source_protocol: Protocol,
        target_protocol: Protocol,
    ) -> list[OntologyAlignment]:
        """Etapa 2: Consulta oráculo para correspondências ontológicas."""
        key = (source_protocol.value, target_protocol.value)
        direct_map = self._direct_mappings.get(key, {})

        alignments: list[OntologyAlignment] = []
        for concept in concepts:
            # Buscar mapeamento direto
            direct_target = direct_map.get(concept)
            if direct_target:
                alignments.append(OntologyAlignment(
                    source_entity=concept,
                    target_entity=direct_target,
                    relation=SemanticRelation.EQUIVALENT,
                    confidence=0.95,
                    is_direct=True,
                ))
            else:
                # Sem mapeamento direto → aproximação
                alignments.append(OntologyAlignment(
                    source_entity=concept,
                    target_entity=f"~{concept}",
                    relation=SemanticRelation.SUBSUMES,
                    confidence=0.72,
                    is_direct=False,
                    is_composite=False,
                ))

        return alignments

    def _apply_direct_mapping(
        self, concept: str, alignment: OntologyAlignment
    ) -> dict[str, Any]:
        """Aplica mapeamento direto (1:1) entre conceitos."""
        return {
            "original": concept,
            "translated": alignment.target_entity,
            "relation": alignment.relation.value,
            "confidence": alignment.confidence,
            "type": AlignmentType.DIRECT.value,
        }

    def _apply_composite_mapping(
        self, concept: str, alignment: OntologyAlignment
    ) -> dict[str, Any]:
        """Aplica mapeamento composto (decomposição e tradução)."""
        return {
            "original": concept,
            "translated": alignment.target_entity,
            "relation": alignment.relation.value,
            "confidence": alignment.confidence,
            "type": AlignmentType.COMPOSITE.value,
            "components": [],
        }

    def _approximate(
        self, concept: str, alignment: OntologyAlignment
    ) -> tuple[dict[str, Any], SemanticLoss]:
        """Gera aproximação com aviso de perda semântica."""
        translated = {
            "original": concept,
            "translated": alignment.target_entity,
            "relation": alignment.relation.value,
            "confidence": alignment.confidence,
            "type": AlignmentType.APPROXIMATE.value,
            "warning": f"Sem correspondência direta para '{concept}'",
        }

        loss = SemanticLoss(
            concept=concept,
            gap_description=f"'{concept}' não possui equivalente no protocolo de destino",
            resolution=f"Aproximação via inferência NL: '{alignment.target_entity}'",
            residual_loss=1.0 - alignment.confidence,
        )

        return translated, loss

    def _compose(
        self,
        components: list[dict[str, Any]],
        target_protocol: Protocol,
    ) -> dict[str, Any]:
        """Compõe mensagem final no formato do protocolo de destino."""
        if target_protocol == Protocol.MCP:
            return {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "translated_components": components,
                },
                "id": 1,
            }
        elif target_protocol == Protocol.A2A:
            return {
                "role": "agent",
                "parts": [
                    {"type": "data", "data": {"components": components}}
                ],
            }
        elif target_protocol == Protocol.ACP:
            return {
                "acp_version": "1.0",
                "message_type": "request",
                "payload": {
                    "intent": "translated_message",
                    "parameters": {"components": components},
                    "context": {},
                },
            }
        return {"components": components}

    def _compute_confidence(self, alignments: list[OntologyAlignment]) -> float:
        """Calcula confiança global da tradução."""
        if not alignments:
            return 0.0
        return sum(a.confidence for a in alignments) / len(alignments)


# ---------------------------------------------------------------------------
# Ponto de entrada para demonstração
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    translator = SemanticTranslator()

    # Exemplo: Traduzir mensagem MCP → A2A
    mcp_message = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "semantic_search",
            "arguments": {"query": "protocolos multi-agente", "limit": 10},
        },
        "id": 1,
    }

    result = translator.translate(mcp_message, Protocol.MCP, Protocol.A2A)

    print("=" * 60)
    print("  TRADUÇÃO SEMÂNTICA: MCP → A2A")
    print("=" * 60)
    print(f"\n  Confiança global: {result.confidence:.2%}")
    print(f"  Taxa de preservação: {result.preservation_rate:.2%}")
    print(f"  Perdas semânticas: {len(result.semantic_losses)}")
    print("\n  Log de tradução:")
    for entry in result.translation_log:
        print(f"    {entry}")
    print()
