"""Shared fixtures e configuração para pytest."""

import sys
from pathlib import Path

# Garante que o diretório raiz está no sys.path para imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
