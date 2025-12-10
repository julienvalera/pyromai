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

## Qualité du Code

### Linters et Type Checkers
- **ruff** : Linter moderne avec moderate strictness
  - Règles activées : F, E, W, I, N, UP, B, A, C4, SIM, RUF
  - Line length : 100 caractères
- **ty** (Astral) : Type checker moderne et ultra-rapide
  - Configuration defaults (compatible avec Python 3.11+)
- **pytest** + **coverage** : Tests avec seuil minimum de 80%

### Pré-commit Hooks
- **OBLIGATOIRE** avant chaque commit
- Auto-format avec ruff
- Auto-check types avec ty
- Prévient les commits non-conformes

Installation :
```bash
pre-commit install
```

### Vérification avant commit
**Cette checklist est OBLIGATOIRE avant chaque `git commit`** :

```bash
# 1. Linting
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# 2. Type checking
uv run ty check src/

# 3. Tests avec coverage
uv run pytest --cov=src --cov-fail-under=80

# 4. Si tout passe, commit !
git commit -m "..."
```

Ou utiliser pre-commit pour automatiser :
```bash
pre-commit run --all-files
```

### CI/CD Automatique
- GitHub Actions vérifie ruff, ty, pytest à chaque push/PR
- Matrix : Python 3.11, 3.12, 3.13
- Fail sur coverage < 80% ou linting errors

## Commandes de développement

### Lancement de l'application
```bash
# CLI installable
uv run pyromai /path/to/project

# Avec source en développement
cd /path/to/pyromai
uv sync
uv run pyromai /path/to/project
```

### Tests
```bash
# Lancer les tests
uv run pytest

# Avec coverage (affiche les % par fichier)
uv run pytest --cov=src

# Générer rapport HTML
uv run pytest --cov=src --cov-report=html
# Ouvrir : open htmlcov/index.html
```

### Linting et formatage
```bash
# Vérifier tout
uv run ruff check src/ tests/
uv run ty check src/

# Auto-formatter (modifie les fichiers)
uv run ruff format src/ tests/

# Pre-commit pour tout d'un coup
pre-commit run --all-files
```

### Build et publication
```bash
# Build wheel + sdist
uv build

# Publier sur PyPI (après obtenir des crédentials)
uv publish
```

## Résumé des règles clés

### Codage
1. ✅ Python 3.11+ avec fonctionnalités modernes
2. ✅ `dependency-groups.dev` au lieu de `tool.uv.dev-dependencies`
3. ❌ Pas de `from __future__ import annotations`
4. ✅ Imports absolus uniquement (`from analyzer...`)
5. ❌ Jamais de `print()`, toujours des loggers
6. ✅ Rich pour les outputs utilisateur élégants
7. ✅ Messages de log structurés et informatifs
8. ✅ Type hints complets avec syntaxe moderne
9. ✅ Docstrings pour toutes les fonctions/classes publiques

### Qualité (OBLIGATOIRE avant chaque commit)
10. ✅ **ruff check + ruff format** passent (linting)
11. ✅ **ty check src/** passe (type checking)
12. ✅ **pytest --cov=src --cov-fail-under=80** passe (tests + 80% coverage min)
13. ✅ Pre-commit hooks installés et passants : `pre-commit install`
14. ✅ CLI : `uv run pyromai /path/to/project`

### Avant chaque commit
```bash
pre-commit run --all-files  # Auto-fix + check
uv run pytest --cov=src --cov-fail-under=80  # Tests
git commit -m "..."  # Si tout passe
```
