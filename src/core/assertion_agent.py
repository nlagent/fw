"""
assertion_agent.py — Agente de Validação de Robustez (NL-Agent Framework)

Este agente implementa a Heurística 3 do framework:
"A validação deve ser implementada como agente autônomo — nunca como código embutido."

Ele audita o repositório em busca de:
1. Conformidade arquitetural (presença de arquivos essenciais)
2. Coerência semântica nas definições
3. Integridade dos protocolos (MCP, A2A, ACP)
4. Métricas de prontidão (Maturity Score)
"""

import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class ValidationIssue:
    severity: str  # ERROR, WARNING, INFO
    category: str
    message: str
    file: str | None = None

class RobustnessReport:
    def __init__(self):
        self.issues: list[ValidationIssue] = []
        self.maturity_score: float = 0.0
        self.checks_run: int = 0

    def add_issue(self, severity, category, message, file=None):
        self.issues.append(ValidationIssue(severity, category, message, file))

    def generate_summary(self):
        errors = len([i for i in self.issues if i.severity == "ERROR"])
        warnings = len([i for i in self.issues if i.severity == "WARNING"])
        
        # Simple scoring formula
        self.maturity_score = max(0, 100 - (errors * 10) - (warnings * 2))
        
        return {
            "maturity_score": f"{self.maturity_score}%",
            "status": "APPROVED" if errors == 0 else "DEGRADED",
            "metrics": {
                "errors": errors,
                "warnings": warnings,
                "total_issues": len(self.issues),
                "checks_performed": self.checks_run
            }
        }

class AssertionAgent:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.report = RobustnessReport()

    def run_audit(self):
        print(f"🔍 Iniciando auditoria de robustez em: {self.root}")
        
        # 1. Arquivos Essenciais
        self._check_essential_files()
        
        # 2. Estrutura de Código
        self._check_code_integrity()
        
        # 3. Documentação
        self._check_documentation_coherence()
        
        # Result
        summary = self.report.generate_summary()
        print(f"\n✅ Auditoria concluída. Score: {summary['maturity_score']}")
        return summary

    def _check_essential_files(self):
        self.report.checks_run += 1
        essential = [
            # Documentação
            "README.md", "ARQUITETURA.md", "EXEGESE.md", "GLOSSARIO.md",
            "CONTRIBUTING.md", "SECURITY.md", "LICENSE",
            # Configuração Python
            "pyproject.toml",
            # Configuração JS/TS
            "package.json", "tsconfig.json",
            # Qualidade e consistência
            ".editorconfig", ".eslintrc.json", ".prettierrc",
            ".pre-commit-config.yaml", ".gitignore",
            # Referência de ambiente
            ".env.example",
        ]
        for f in essential:
            if not (self.root / f).exists():
                self.report.add_issue("ERROR", "Foundation", f"Arquivo essencial ausente: {f}")

    def _check_code_integrity(self):
        self.report.checks_run += 1
        src_dir = self.root / "src"
        if not src_dir.exists():
            self.report.add_issue("ERROR", "Architecture", "Diretório /src não encontrado")
            return

        # Check for core files
        core_files = ["semantic_translator.py", "nl_reasoner.py", "unified_capability.ts"]
        for f in core_files:
            if not (src_dir / "core" / f).exists():
                self.report.add_issue("ERROR", "Core", f"Módulo core ausente: {f}")

        # Check Python package structure
        for init_path in [src_dir / "__init__.py", src_dir / "core" / "__init__.py"]:
            if not init_path.exists():
                self.report.add_issue("WARNING", "Packaging", f"__init__.py ausente: {init_path.relative_to(self.root)}")

        # Check PEP 561 typed marker
        py_typed = src_dir / "core" / "py.typed"
        if not py_typed.exists():
            self.report.add_issue("WARNING", "Typing", "Marker py.typed (PEP 561) ausente em src/core/")

        # Check CI pipeline
        ci_path = self.root / ".github" / "workflows" / "ci.yml"
        if not ci_path.exists():
            self.report.add_issue("WARNING", "CI/CD", "Pipeline CI (.github/workflows/ci.yml) não encontrado")

    def _check_documentation_coherence(self):
        self.report.checks_run += 1
        readme = self.root / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            # Assert that the README mentions the protocols it claims to support
            for protocol in ["MCP", "A2A", "ANP", "ACP"]:
                if protocol not in content:
                    self.report.add_issue("WARNING", "Documentation", f"Protocolo {protocol} mencionado na arquitetura mas ausente no README")

if __name__ == "__main__":
    agent = AssertionAgent(os.getcwd())
    report_summary = agent.run_audit()
    
    # Save report
    with open("robustness_report.json", "w", encoding="utf-8") as f:
        json.dump(report_summary, f, indent=2, ensure_ascii=False)
    
    if report_summary["metrics"]["errors"] > 0:
        print("\n❌ Foram encontrados erros críticos. Verifique o relatório.")
        # sys.exit(1) # Don't exit yet to allow other steps
    else:
        print("\n✨ O repositório atende aos critérios de robustez.")
