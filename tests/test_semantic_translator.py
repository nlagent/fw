"""
test_semantic_translator.py — Testes unitários para o Tradutor Semântico.
"""

import pytest
from src.core.semantic_translator import SemanticTranslator, Protocol, TranslationResult

def test_translator_initialization():
    translator = SemanticTranslator()
    assert translator is not None
    assert translator.nl_reasoner is not None

def test_mcp_to_a2a_translation_structure():
    translator = SemanticTranslator()
    mcp_message = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "test_tool",
            "arguments": {"key": "value"}
        },
        "id": 1
    }
    
    result = translator.translate(mcp_message, Protocol.MCP, Protocol.A2A)
    
    assert isinstance(result, TranslationResult)
    assert result.source_protocol == Protocol.MCP
    assert result.target_protocol == Protocol.A2A
    assert "role" in result.message
    assert result.confidence >= 0.0
