# Règles de codage - Clean Code Analyzer

Ce document définit les règles et conventions de codage à respecter pour le projet Clean Code Analyzer.

## Python et Dépendances

### Version Python
- **Python 3.11+** minimum (déclaré dans `pyproject.toml`)
- Utiliser les fonctionnalités modernes de Python 3.11+

### Gestionnaire de paquets
- **uv** pour la gestion des dépendances
- Commandes principales :
  - `uv sync` - Installer les dépendances
  - `uv run python -m src.analyzer <path>` - Lancer l'application
  - `uv add <package>` - Ajouter une dépendance

### Configuration pyproject.toml
- ✅ Utiliser `dependency-groups.dev` pour les dépendances de développement
- ❌ **NE PAS** utiliser `tool.uv.dev-dependencies` (déprécié)

```toml
# ✅ CORRECT
[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "mypy>=1.0.0",
]

# ❌ INCORRECT (déprécié)
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
]
```

## Type Hints et Annotations

### Imports de types
- ❌ **NE PAS** utiliser `from __future__ import annotations` (inutile en Python 3.10+)
- ✅ Utiliser directement les types modernes : `list[str]`, `dict[str, int]`, `str | None`
- ✅ Pour les unions, utiliser l'opérateur `|` : `str | None` au lieu de `Optional[str]`

```python
# ✅ CORRECT (Python 3.11+)
def process_items(items: list[str]) -> dict[str, int]:
    pass

def get_user(user_id: int) -> User | None:
    pass

# ❌ INCORRECT
from __future__ import annotations
from typing import Optional, List, Dict

def process_items(items: List[str]) -> Dict[str, int]:
    pass

def get_user(user_id: int) -> Optional[User]:
    pass
```

## Imports

### Style d'imports
- ✅ **TOUJOURS** utiliser des imports absolus
- ❌ **NE JAMAIS** utiliser des imports relatifs

```python
# ✅ CORRECT - Imports absolus
from src.analyzer.models import FileMetrics
from src.analyzer.parser import Parser

# ❌ INCORRECT - Imports relatifs
from .models import FileMetrics
from ..parser import Parser
```

### Organisation des imports
1. Imports de la bibliothèque standard
2. Imports de bibliothèques tierces
3. Imports du projet (absolus)

Séparés par une ligne vide entre chaque groupe.

```python
# Standard library
import ast
from pathlib import Path

# Third-party
from rich.console import Console
from rich.logging import RichHandler

# Project imports
from src.analyzer.models import FileMetrics
from src.analyzer.parser import Parser
```

## Logging et Output

### Règle fondamentale : PAS DE PRINT
- ❌ **NE JAMAIS** utiliser `print()` directement
- ✅ **TOUJOURS** utiliser un logger configuré

### Configuration du logger
- Utiliser `logging` avec `rich.logging.RichHandler` pour un output élégant
- Niveaux de log appropriés : `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```python
# ✅ CORRECT - Setup du logger
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

logger = logging.getLogger(__name__)

# Utilisation
logger.info("Analyzing project: %s", project_path)
logger.warning("Could not parse file: %s", file_path)
logger.error("Failed to load configuration: %s", error)
logger.debug("Found %d Python files", len(files))
```

```python
# ❌ INCORRECT
print(f"Analyzing project: {project_path}")
print(f"Warning: Could not parse {file_path}")
```

### Messages de log structurés
- Messages clairs et informatifs
- Utiliser le formatage lazy (`%s`, `%d`) plutôt que f-strings dans les logs
- Inclure du contexte pertinent (chemins, compteurs, erreurs)

```python
# ✅ CORRECT
logger.info("Parsing completed: %d files, %d lines, complexity avg: %.2f",
            total_files, total_lines, avg_complexity)

# ❌ MOINS BON
logger.info(f"Parsing completed: {total_files} files")  # f-string évalué même si log désactivé
```

## Output utilisateur (Rapports)

### Pour les rapports finaux
- Utiliser **Rich** pour les rapports visuels élégants
- Tables, panels, syntax highlighting, progress bars, etc.

```python
from rich.console import Console
from rich.table import Table

console = Console()

# Table de résumé
table = Table(title="Project Analysis Summary")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="green")
table.add_row("Total Files", str(index.total_files))
table.add_row("Total Lines", str(index.total_lines))
console.print(table)

# Panel pour architecture
from rich.panel import Panel
console.print(Panel(f"Pattern: {arch.pattern}\nConfidence: {arch.confidence:.1%}",
                    title="Architecture Detection"))
```

## Structure du code

### Classes et fonctions
- Docstrings pour toutes les classes et fonctions publiques
- Type hints complets
- Noms explicites et significatifs

### Gestion des erreurs
- Logger les erreurs avec `logger.error()` ou `logger.exception()`
- Inclure le contexte de l'erreur
- Ne pas masquer les exceptions silencieusement

```python
# ✅ CORRECT
try:
    metrics = parse_file(file_path)
except SyntaxError as e:
    logger.warning("Syntax error in %s: %s", file_path, e)
    return None
except Exception as e:
    logger.exception("Unexpected error parsing %s", file_path)
    raise
```

## Tests

### Structure des tests
- Tests dans le répertoire `tests/`
- Un fichier de test par module : `test_<module>.py`
- Utiliser pytest
- Assertions claires avec messages explicites

```python
def test_parser_invalid_path():
    """Test that parser raises ValueError for invalid paths."""
    with pytest.raises(ValueError, match="must be a directory"):
        Parser("/nonexistent/path")
```

## Commandes de développement

### Lancement de l'application
```bash
# Lancer l'analyse
uv run python -m src.analyzer /path/to/project

# Avec options
uv run python -m src.analyzer /path/to/project --output ./reports
```

### Tests
```bash
# Lancer les tests
uv run pytest

# Avec coverage
uv run pytest --cov=src
```

### Linting et formatage
```bash
# Type checking
uv run mypy src/

# Linting
uv run ruff check src/

# Formatage
uv run ruff format src/
```

## Résumé des règles clés

1. ✅ Python 3.11+ avec fonctionnalités modernes
2. ✅ `dependency-groups.dev` au lieu de `tool.uv.dev-dependencies`
3. ❌ Pas de `from __future__ import annotations`
4. ✅ Imports absolus uniquement (`from src.analyzer...`)
5. ❌ Jamais de `print()`, toujours des loggers
6. ✅ Rich pour les outputs utilisateur élégants
7. ✅ Messages de log structurés et informatifs
8. ✅ Type hints complets avec syntaxe moderne
9. ✅ Docstrings pour toutes les fonctions/classes publiques
10. ✅ `uv run python -m src.analyzer <path>` pour lancer l'app
