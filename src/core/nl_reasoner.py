"""
nl_reasoner.py — Motor de Inferência em Lógica Natural (NL-Agent Framework)

Axiomas: K1 Veracidade, K2 Distribuição, K3 Introspecção Positiva.
Autor: Framework NL-Agent, 2026
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import json


class InferenceMode(Enum):
    MONOTONIC = "monotonic"
    NON_MONOTONIC = "non_monotonic"


class ConsistencyLevel(Enum):
    CONSISTENT = "consistent"
    MINOR_ISSUES = "minor_issues"
    MAJOR_ISSUES = "major_issues"
    INCONSISTENT = "inconsistent"


@dataclass
class Proposition:
    content: str
    confidence: float = 1.0
    source: str = ""
    defeasible: bool = False

    def __str__(self) -> str:
        prefix = "~" if self.defeasible else ""
        return f"{prefix}{self.content} [{self.confidence:.0%}]"


@dataclass
class ConsistencyReport:
    level: ConsistencyLevel
    issues: list[str] = field(default_factory=list)
    corrections_applied: list[str] = field(default_factory=list)
    original_propositions: int = 0
    valid_propositions: int = 0

    @property
    def is_acceptable(self) -> bool:
        return self.level in (ConsistencyLevel.CONSISTENT, ConsistencyLevel.MINOR_ISSUES)

    @property
    def validity_rate(self) -> float:
        if self.original_propositions == 0:
            return 0.0
        return self.valid_propositions / self.original_propositions


class NLReasoner:
    """Motor de inferência NL com axiomas K1-K3 e inferência monotônica/não-monotônica."""

    def __init__(self, consistency_threshold: float = 0.95) -> None:
        self.threshold = consistency_threshold
        self._knowledge_base: list[Proposition] = []

    def validate_message(self, message: dict[str, Any]) -> ConsistencyReport:
        issues: list[str] = []
        propositions = self._extract_propositions(message)
        valid_count = 0
        for prop in propositions:
            if not prop.content.strip():
                issues.append(f"K1 violado: proposição vazia de '{prop.source}'")
                continue
            if not self._check_distribution(prop):
                issues.append(f"K2 violado: implicação inconsistente em '{prop.content[:40]}...'")
                continue
            if prop.confidence < 0.0 or prop.confidence > 1.0:
                issues.append(f"K3 violado: confiança fora de [0,1]")
                continue
            valid_count += 1
        if not issues:
            level = ConsistencyLevel.CONSISTENT
        elif len(issues) <= 2:
            level = ConsistencyLevel.MINOR_ISSUES
        elif len(issues) <= 5:
            level = ConsistencyLevel.MAJOR_ISSUES
        else:
            level = ConsistencyLevel.INCONSISTENT
        return ConsistencyReport(level=level, issues=issues,
                                 original_propositions=len(propositions),
                                 valid_propositions=valid_count)

    def apply_corrections(self, message: dict[str, Any], report: ConsistencyReport) -> dict[str, Any]:
        corrected = dict(message)
        corrections: list[str] = []
        if "payload" in corrected:
            if "parameters" not in corrected["payload"]:
                corrected["payload"]["parameters"] = {}
                corrections.append("Adicionado 'parameters' vazio")
            if "context" not in corrected["payload"]:
                corrected["payload"]["context"] = {}
                corrections.append("Adicionado 'context' vazio")
        if "translation_metadata" not in corrected:
            corrected["translation_metadata"] = {"corrections_applied": True, "original_issues": len(report.issues)}
            corrections.append("Adicionado metadados de tradução")
        report.corrections_applied = corrections
        return corrected

    def infer_monotonic(self, base: list[Proposition], new: Proposition) -> list[Proposition]:
        result = list(base)
        if not any(p.content == new.content for p in result):
            result.append(new)
        return result

    def infer_non_monotonic(self, base: list[Proposition], new: Proposition) -> list[Proposition]:
        result = [p for p in base if not (p.defeasible and self._contradicts(p, new))]
        result.append(new)
        return result

    def _extract_propositions(self, message: dict[str, Any]) -> list[Proposition]:
        propositions: list[Proposition] = []
        def _traverse(obj: Any, path: str = "") -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    cp = f"{path}.{key}" if path else key
                    if isinstance(value, str) and value.strip():
                        propositions.append(Proposition(content=value, confidence=0.9, source=cp))
                    elif isinstance(value, (int, float)):
                        propositions.append(Proposition(content=f"{cp}={value}", confidence=1.0, source=cp))
                    else:
                        _traverse(value, cp)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    _traverse(item, f"{path}[{i}]")
        _traverse(message)
        return propositions

    def _check_distribution(self, prop: Proposition) -> bool:
        if prop.content.startswith("{") or prop.content.startswith("["):
            try:
                json.loads(prop.content)
            except json.JSONDecodeError:
                return False
        return True

    def _contradicts(self, existing: Proposition, new: Proposition) -> bool:
        if existing.source and new.source and existing.source == new.source:
            return existing.content != new.content
        return False


if __name__ == "__main__":
    reasoner = NLReasoner(consistency_threshold=0.90)
    message = {"acp_version": "1.0", "message_type": "request",
               "payload": {"intent": "analyze_route", "parameters": {"route_id": "R-042", "students": 50},
                           "context": {"session_id": "sess-abc", "source_system": "SGTE"}}}
    report = reasoner.validate_message(message)
    print(f"Nível: {report.level.value} | Válidas: {report.valid_propositions}/{report.original_propositions}")
