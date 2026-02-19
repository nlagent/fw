"""
oracle_query.py — Padrões de Consulta Oracular (NL-Agent Framework)

Implementa padrões de invocação que maximizam a precisão das consultas
a oráculos epistêmicos (LLMs/LRMs), conforme seção 4.3.2 da dissertação.

Definição 4 (Oráculo Epistêmico):
    O = ⟨D, Q, R, φ⟩ onde:
    D = domínio de conhecimento
    Q = consultas admissíveis
    R = respostas possíveis
    φ: Q → R = função de resposta

Propriedades:
    (O1) Consistência: φ(q) não contradiz conhecimento prévio
    (O2) Completude Parcial: ∃q ∈ Q tal que φ(q) = ⊥
    (O3) Opacidade: mecanismo interno de φ não é observável

Autor: Framework NL-Agent, 2026
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

class OracleType(Enum):
    """Tipos de oráculo conforme taxonomia (seção 4.1.2)."""
    FIRST_ORDER = "first_order"    # Consultas factuais diretas
    SECOND_ORDER = "second_order"  # Sobre conhecimento de outros agentes
    HIGHER_ORDER = "higher_order"  # Meta-epistêmico


class OracleRole(Enum):
    """Papel funcional do oráculo na mediação (seção 4.2.1)."""
    SEMANTIC = "semantic"          # Preservação de significado
    ONTOLOGICAL = "ontological"    # Tradução de conceitos
    PRAGMATIC = "pragmatic"        # Adaptação contextual


class ModelTier(Enum):
    """
    Classificação do modelo conforme a dualidade LLM/LRM.
    System 1 = rápido, intuitivo (LLM)
    System 2 = lento, deliberativo (LRM)
    """
    SYSTEM_1_LLM = "llm"   # GPT-4o, Gemini Flash — tradução, resumo
    SYSTEM_2_LRM = "lrm"   # o1, R1, Gemini Pro — compliance, cálculos


@dataclass
class OracleResponse:
    """Resposta estruturada de um oráculo epistêmico."""
    answer: str
    confidence: float                       # 0.0 a 1.0
    sources: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)
    oracle_type: OracleType = OracleType.FIRST_ORDER
    model_tier: ModelTier = ModelTier.SYSTEM_1_LLM
    latency_ms: float = 0.0

    @property
    def is_high_confidence(self) -> bool:
        return self.confidence >= 0.85

    @property
    def requires_human_review(self) -> bool:
        return self.confidence < 0.70


@dataclass
class SemanticAlignmentQuery:
    """Consulta de alinhamento semântico entre protocolos."""
    source_protocol: str
    source_concept: str
    source_definition: str
    target_protocol: str
    target_concept: str
    constraints: list[str] = field(default_factory=list)


@dataclass
class AlignmentResponse:
    """Resposta de alinhamento semântico."""
    relation: str        # ≡, ⊑, ⊒, ⊥
    confidence: float
    mapping: dict[str, str] = field(default_factory=dict)
    semantic_gaps: list[dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Motor de Consulta Oracular
# ---------------------------------------------------------------------------

class OracleQuery:
    """
    Consulta oracular com contexto e restrições.

    Implementa o padrão de Consulta Estruturada com Contexto (seção 4.3.2).
    Roteia automaticamente para o tipo de oráculo adequado conforme a
    Heurística de Roteamento (seção 7.1.3).

    Args:
        llm_endpoint: endpoint do oráculo semântico (LLM)
        lrm_endpoint: endpoint do oráculo raciocinador (LRM)
    """

    def __init__(
        self,
        llm_endpoint: Any = None,
        lrm_endpoint: Any = None,
    ) -> None:
        self.llm = llm_endpoint
        self.lrm = lrm_endpoint

    # -----------------------------------------------------------------------
    # Consulta genérica com contexto
    # -----------------------------------------------------------------------

    def query_with_context(
        self,
        question: str,
        context: str,
        constraints: list[str] | None = None,
        oracle_type: OracleType = OracleType.FIRST_ORDER,
    ) -> OracleResponse:
        """
        Consulta oracular com contexto e restrições.

        Args:
            question: Pergunta em linguagem natural
            context: Conhecimento prévio relevante
            constraints: Restrições sobre a resposta
            oracle_type: Tipo de consulta (1ª, 2ª ou superior)

        Returns:
            OracleResponse com resposta estruturada e metadados epistêmicos
        """
        constraints = constraints or []

        # Heurística de Roteamento: determinar o modelo adequado
        model_tier = self._classify_task(question, constraints)
        prompt = self._construct_prompt(question, context, constraints)

        # Invocar o oráculo apropriado
        if model_tier == ModelTier.SYSTEM_2_LRM and self.lrm:
            raw = self._invoke_oracle(self.lrm, prompt)
        elif self.llm:
            raw = self._invoke_oracle(self.llm, prompt)
        else:
            raw = self._simulate_response(question)

        return self._parse_response(raw, oracle_type, model_tier)

    # -----------------------------------------------------------------------
    # Consulta de alinhamento semântico
    # -----------------------------------------------------------------------

    def query_alignment(self, query: SemanticAlignmentQuery) -> AlignmentResponse:
        """
        Consulta oracular para alinhamento semântico entre protocolos.

        Implementa o Protocolo de Consulta Oracular (seção 4.2.2).
        """
        prompt = self._construct_alignment_prompt(query)

        if self.llm:
            raw = self._invoke_oracle(self.llm, prompt)
        else:
            raw = self._simulate_alignment(query)

        return self._parse_alignment(raw)

    # -----------------------------------------------------------------------
    # Métodos Internos
    # -----------------------------------------------------------------------

    def _classify_task(
        self, question: str, constraints: list[str]
    ) -> ModelTier:
        """
        Heurística de Roteamento LLM/LRM (seção 7.1.3).

        Classifica a tarefa para direcionar ao tipo de oráculo adequado:
        - LLM: tradução, resumo, formatação
        - LRM: cálculos, compliance, otimização
        """
        lrm_keywords = [
            "calcul", "orçament", "fundeb", "pdde", "compliance",
            "otimiz", "rota", "nutricional", "pnae", "lei", "legal",
            "audit", "verific", "consistên",
        ]

        text = (question + " ".join(constraints)).lower()
        for kw in lrm_keywords:
            if kw in text:
                return ModelTier.SYSTEM_2_LRM

        return ModelTier.SYSTEM_1_LLM

    def _construct_prompt(
        self, question: str, context: str, constraints: list[str]
    ) -> str:
        """Constrói prompt estruturado para consulta oracular."""
        constraints_text = "\n".join(f"  - {c}" for c in constraints) if constraints else "  (nenhuma)"

        return f"""Contexto:
{context}

Pergunta:
{question}

Restrições:
{constraints_text}
  - Responder apenas com base no contexto fornecido
  - Indicar nível de confiança (0-1)
  - Citar fontes quando aplicável

Formato de resposta (JSON):
{{
  "answer": "...",
  "confidence": 0.X,
  "sources": [...],
  "caveats": [...]
}}"""

    def _construct_alignment_prompt(self, query: SemanticAlignmentQuery) -> str:
        """Constrói prompt para consulta de alinhamento semântico."""
        return f"""Alinhe semanticamente os conceitos entre protocolos:

Origem:
  Protocolo: {query.source_protocol}
  Conceito: {query.source_concept}
  Definição: {query.source_definition}

Destino:
  Protocolo: {query.target_protocol}
  Conceito: {query.target_concept}

Restrições: {', '.join(query.constraints) if query.constraints else 'nenhuma'}

Determine:
1. Relação semântica (≡ equivalente, ⊑ subsume, ⊒ superclasse, ⊥ disjunto)
2. Mapeamento de campos
3. Lacunas semânticas e resoluções propostas

Responda em JSON."""

    def _invoke_oracle(self, endpoint: Any, prompt: str) -> str:
        """Invoca o oráculo (LLM ou LRM) com o prompt construído."""
        if hasattr(endpoint, "generate"):
            return endpoint.generate(prompt)
        return self._simulate_response(prompt)

    def _simulate_response(self, question: str) -> str:
        """Simulação para ambiente sem oráculo real."""
        return json.dumps({
            "answer": f"[Resposta simulada para: {question[:80]}...]",
            "confidence": 0.75,
            "sources": ["simulação_local"],
            "caveats": ["Oráculo não conectado — resposta simulada"],
        })

    def _simulate_alignment(self, query: SemanticAlignmentQuery) -> str:
        """Simulação de alinhamento semântico."""
        return json.dumps({
            "relation": "subsumes",
            "confidence": 0.89,
            "mapping": {
                f"{query.source_concept}.name": f"{query.target_concept}.id",
                f"{query.source_concept}.description": f"{query.target_concept}.description",
            },
            "semantic_gaps": [
                {
                    "gap": f"{query.target_concept}.tags não presente em {query.source_concept}",
                    "resolution": f"Derivar de {query.source_concept}.description via NLP",
                }
            ],
        })

    def _parse_response(
        self, raw: str, oracle_type: OracleType, model_tier: ModelTier
    ) -> OracleResponse:
        """Parseia resposta do oráculo em estrutura tipada."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"answer": raw, "confidence": 0.5, "sources": [], "caveats": ["Parse falhou"]}

        return OracleResponse(
            answer=data.get("answer", ""),
            confidence=data.get("confidence", 0.5),
            sources=data.get("sources", []),
            caveats=data.get("caveats", []),
            oracle_type=oracle_type,
            model_tier=model_tier,
        )

    def _parse_alignment(self, raw: str) -> AlignmentResponse:
        """Parseia resposta de alinhamento."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"relation": "⊥", "confidence": 0.0, "mapping": {}, "semantic_gaps": []}

        return AlignmentResponse(
            relation=data.get("relation", "⊥"),
            confidence=data.get("confidence", 0.0),
            mapping=data.get("mapping", {}),
            semantic_gaps=data.get("semantic_gaps", []),
        )


# ---------------------------------------------------------------------------
# Demonstração
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    oracle = OracleQuery()

    print("=" * 60)
    print("  CONSULTA ORACULAR — Demonstração")
    print("=" * 60)

    # Consulta factual (1ª Ordem → LLM)
    r1 = oracle.query_with_context(
        question="Qual é o status atual do protocolo A2A?",
        context="A2A é um protocolo peer-to-peer desenvolvido pela Google.",
        oracle_type=OracleType.FIRST_ORDER,
    )
    print(f"\n  [1ª Ordem | {r1.model_tier.value}] Confiança: {r1.confidence:.0%}")
    print(f"  Resposta: {r1.answer[:80]}...")

    # Consulta de compliance (→ LRM)
    r2 = oracle.query_with_context(
        question="Esta despesa viola a regra de 70% do FUNDEB?",
        context="Despesa de R$ 150.000 em material didático. Orçamento total: R$ 200.000.",
        constraints=["Verificar conformidade com Lei do FUNDEB"],
        oracle_type=OracleType.FIRST_ORDER,
    )
    print(f"\n  [Compliance | {r2.model_tier.value}] Confiança: {r2.confidence:.0%}")
    print(f"  Resposta: {r2.answer[:80]}...")

    # Alinhamento semântico
    align = oracle.query_alignment(SemanticAlignmentQuery(
        source_protocol="MCP",
        source_concept="tool",
        source_definition="An executable capability exposed by a server",
        target_protocol="A2A",
        target_concept="skill",
        constraints=["preserve_semantics", "maintain_composability"],
    ))
    print(f"\n  [Alinhamento] Relação: {align.relation} | Confiança: {align.confidence:.0%}")
    print(f"  Mapeamento: {align.mapping}")
    print()
