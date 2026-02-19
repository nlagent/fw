"""Core — Módulos centrais do NL-Agent Framework.

Exporta os componentes principais:
- SemanticTranslator: Tradução semântica entre protocolos (MCP, A2A, ACP)
- NLReasoner: Motor de inferência em Lógica Natural (axiomas K1-K3)
- OracleQuery: Consultas oraculares a LLMs/LRMs
- AssertionAgent: Validação de robustez do repositório
"""

from src.core.semantic_translator import SemanticTranslator, Protocol, TranslationResult
from src.core.nl_reasoner import NLReasoner, ConsistencyReport, ConsistencyLevel
from src.core.oracle_query import OracleQuery, OracleResponse, OracleType, ModelTier

__all__ = [
    "SemanticTranslator",
    "Protocol",
    "TranslationResult",
    "NLReasoner",
    "ConsistencyReport",
    "ConsistencyLevel",
    "OracleQuery",
    "OracleResponse",
    "OracleType",
    "ModelTier",
]
