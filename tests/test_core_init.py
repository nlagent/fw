"""Testes unitários para __init__.py do pacote core."""

from src.core import (
    ConsistencyLevel,
    ConsistencyReport,
    ModelTier,
    NLReasoner,
    OracleQuery,
    OracleResponse,
    OracleType,
    Protocol,
    SemanticTranslator,
    TranslationResult,
)


def test_core_exports_are_importable():
    """Verifica que todos os exports do __init__.py são importáveis."""
    assert SemanticTranslator is not None
    assert Protocol is not None
    assert TranslationResult is not None
    assert NLReasoner is not None
    assert ConsistencyReport is not None
    assert ConsistencyLevel is not None
    assert OracleQuery is not None
    assert OracleResponse is not None
    assert OracleType is not None
    assert ModelTier is not None


def test_protocol_enum_values():
    """Verifica os valores do enum Protocol."""
    assert Protocol.MCP.value == "mcp"
    assert Protocol.A2A.value == "a2a"
    assert Protocol.ACP.value == "acp"


def test_oracle_type_enum_values():
    """Verifica os valores do enum OracleType."""
    assert OracleType.FIRST_ORDER.value == "first_order"
    assert OracleType.SECOND_ORDER.value == "second_order"
    assert OracleType.HIGHER_ORDER.value == "higher_order"


def test_model_tier_enum_values():
    """Verifica os valores do enum ModelTier."""
    assert ModelTier.SYSTEM_1_LLM.value == "llm"
    assert ModelTier.SYSTEM_2_LRM.value == "lrm"
