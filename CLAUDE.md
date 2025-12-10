# Pyromai - Contexte du projet

## Vue d'ensemble

**Pyromai** (anciennement Clean Code Analyzer) est un outil CLI d'analyse de code Python utilisant l'IA (Claude) pour détecter les violations des principes Clean Code et Clean Architecture. L'objectif est de fournir des recommandations actionnables et pédagogiques, similaires à SonarQube, mais avec une analyse contextuelle basée sur LLM.

## Motivation

- **Besoin** : Pas d'outils 100% gratuits pour l'analyse approfondie de code selon Clean Code/Clean Architecture
- **Objectif** : Industrialiser l'analyse de qualité de code avec des règles personnalisables
- **Approche** : LLM pour analyse contextuelle (complémentaire aux outils comme Sonar/Pylint)
- **Stratégie** : Commencer par un PoC/MVP simple et itérer

## Règles de codage

Ce projet suit des règles de codage strictes définies dans [.claude/coding-rules.md](.claude/coding-rules.md).

**Points clés** :
- Python 3.13+ avec fonctionnalités modernes (pas de `from __future__ import annotations`)
- Imports absolus uniquement (`from analyzer...` depuis le package root)
- Logging structuré avec Rich (jamais de `print()`)
- Type hints modernes : `list[str]`, `dict[str, int]`, `str | None`
- Output utilisateur avec Rich (tables, panels, syntax highlighting)
- Configuration moderne : `dependency-groups.dev` (uv)
- Linting + formatting : ruff (lint + format) + ty (type checker)

Voir [.claude/coding-rules.md](.claude/coding-rules.md) pour le guide complet.

## Contexte technique

### Projet cible pour validation
- **Codebase de test** : [Olbia Backend](/Users/julienvalera/Projets/olbia/backend)
  - Application Python serverless sur AWS (Lambda, Aurora, API Gateway)
  - Architecture hexagonale (Ports & Adapters)
  - ~50 fichiers Python, ~3,200 lignes de code
  - Stack : Python 3.11, SQLAlchemy, asyncio, OpenTelemetry
  - Infrastructure : Terraform
  - Bonnes pratiques déjà présentes : mypy, ruff, pytest, pre-commit hooks

### Scope du PoC (Version Minimale)

**Focus** : Clean Code + Clean Architecture uniquement (pas de sécurité/performance/AWS Well-Architected pour le moment)

**Fonctionnalités MVP** :
1. Parser un projet Python (structure, imports, classes, fonctions, métriques)
2. Sélection intelligente des fichiers à analyser (scoring multi-critères)
3. Préparation du contexte optimisé (format compact + code complet prioritaire)
4. Analyser avec Claude selon des règles prédéfinies (batch analysis)
5. Générer rapport JSON + résumé Markdown avec exemples (style Sonar)
6. Exécution en local (CLI)

**Améliorations par rapport au plan initial** :
- ✅ Métriques objectives calculées (complexité via radon)
- ✅ Sélection intelligente des fichiers (pas de limite arbitraire à 20)
- ✅ Règles en fichiers Markdown dès le PoC (extensibilité)
- ✅ Validation robuste du JSON retourné par Claude
- ✅ Retry logic pour appels API
- ✅ Prompt en anglais (meilleure performance LLM)

**Limitations assumées du PoC** :
- Analyse en une seule passe (pas de multi-niveaux) - Phase 2
- Pas de compaction sémantique avancée - Phase 2
- Pas de cache/analyse incrémentale - Phase 2
- Pas de tests unitaires - Focus fonctionnel d'abord
- Pas de parallélisation - Phase 2 si nécessaire

## Architecture du PoC

### Structure du projet

✅ **Implémenté** (Phase 1 PoC + Quality Infrastructure) :
```
pyromai/
├── pyproject.toml              # ✅ Dépendances (uv, dependency-groups.dev, hatchling)
├── uv.lock                     # ✅ Lockfile uv (mis à jour)
├── .python-version             # ✅ Python 3.13 (default)
├── README.md                   # ✅ Documentation complète
├── CLAUDE.md                   # Ce fichier (contexte du projet)
│
├── .env.example                # ✅ Template pour ANTHROPIC_API_KEY
├── .gitignore                  # ✅ Optimisé pour Python + IDE
├── .pre-commit-config.yaml     # ✅ Pre-commit hooks (ruff + ty)
│
├── .github/
│   └── workflows/
│       └── ci.yml              # ✅ GitHub Actions (lint, test, quality gate)
│
├── .claude/
│   ├── coding-rules.md         # ✅ Règles de codage (Python 3.13+ standards)
│   └── commands/
│       ├── start-feature.md    # ✅ Commande /start-feature
│       └── sync.md             # ✅ Commande /sync pour resynchronisation
│
├── rules/
│   └── clean-architecture/     # 🔮 À remplir Phase 2
│       ├── solid-d.md
│       ├── solid-s.md
│       ├── dry.md
│       ├── naming.md
│       └── complexity.md
│
├── src/
│   ├── __init__.py             # ✅ Package root
│   └── analyzer/
│       ├── __init__.py         # ✅ Exports principaux (Parser)
│       ├── __main__.py         # ✅ Entry point CLI (typer + Rich)
│       ├── models.py           # ✅ Dataclasses pour AST/metrics
│       ├── parser.py           # ✅ AST parser + radon metrics + arch detection
│       ├── agents/
│       │   └── __init__.py     # 🔮 Phase 2 : Multi-agents
│       ├── selector.py         # 🔮 Phase 2 : Sélection intelligente
│       ├── context.py          # 🔮 Phase 2 : Préparation contexte LLM
│       ├── llm_client.py       # 🔮 Phase 2 : Claude client + retry
│       ├── rules_loader.py     # 🔮 Phase 2 : Loader règles Markdown
│       └── report.py           # 🔮 Phase 2 : Report generators
│
├── tests/
│   ├── __init__.py             # ✅ Package tests
│   └── test_analyzer.py        # ✅ Tests (3/3 passing, 80%+ coverage)
│
├── assets/                     # ✅ Logo + banner (webp)
├── dist/                       # ✅ Build artifacts (wheel + sdist)
├── htmlcov/                    # ✅ Coverage report HTML
└── screens/                    # Dashboard screenshot (Phase 3)
```

### Stack technique

**Core** :
- **Python 3.13+** (minimum)
- **anthropic** (>=0.7.0) : Client Claude API
- **typer** (>=0.9.0) : CLI framework avec click sous-jacent
- **rich** (>=13.0.0) : Terminal UI (tables, panels, syntax highlighting)
- **pydantic** (>=2.0.0) : Validation + serialization de données
- **python-dotenv** (>=1.0.0) : Environment variables management

**Analyse & Parsing** :
- **ast** (stdlib) : Python AST parsing
- **radon** (>=6.0.0) : Complexity metrics (cyclomatic, cognitive)
- **tenacity** (>=8.0.0) : Retry logic avec exponential backoff

**Quality & Testing** :
- **pytest** (>=7.0.0) : Unit testing
- **pytest-asyncio** (>=0.21.0) : Async test support
- **pytest-cov** (>=5.0.0) : Coverage reporting
- **ruff** (>=0.1.0) : Lint + format (astral-sh)
- **ty** (>=0.0.1a1) : Type checker (astral-sh)
- **pre-commit** (>=3.0.0) : Git hooks automation

**Build & Distribution** :
- **hatchling** : Python packaging backend
- **uv** : Fast Python package manager (Rust-based)

**Futur (Phase 2+)** :
- **tree-sitter** : Multi-language AST parsing
- **astroid** : Static type inference

### Workflow d'analyse

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PARSING & INDEXING                                      │
├─────────────────────────────────────────────────────────────┤
│ - Scan récursif du répertoire Python                       │
│ - Parse AST : imports, classes, fonctions, signatures      │
│ - Calcul métriques : complexité (radon), LOC, imports      │
│ - Détection architecture : hexagonal, layered, unknown     │
│ → Output: CodebaseIndex (structure complète du projet)     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. INTELLIGENT FILE SELECTION                              │
├─────────────────────────────────────────────────────────────┤
│ Scoring multi-critères :                                   │
│ - Taille fichier (LOC > 200 = +10 pts)                    │
│ - Complexité (cyclomatic > 10 = +15 pts)                  │
│ - Nombre d'imports (couplage élevé = +pts)                │
│ - Couche architecturale (domain/app = priorité)           │
│ - Noms suspects (handler, manager, service = +pts)        │
│ → Output: Top N fichiers par score décroissant             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CONTEXT PREPARATION (Budget: 150K tokens)               │
├─────────────────────────────────────────────────────────────┤
│ Architecture overview (~1K tokens)                          │
│ + Tous les fichiers en format compact (~200 tokens/file)   │
│   - Path, imports, signatures, métriques                   │
│ + Top 10-15 fichiers en code complet (~2-5K tokens/file)  │
│ + Règles Markdown chargées depuis rules/default/           │
│ → Output: Prompt optimisé < 150K tokens                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LLM ANALYSIS (Batch, single-pass)                       │
├─────────────────────────────────────────────────────────────┤
│ - Appel API Claude (model: sonnet-4.5)                     │
│ - Prompt en anglais (meilleure performance)                │
│ - Retry logic avec backoff exponentiel (tenacity)          │
│ - Extraction & validation JSON (Pydantic)                  │
│ → Output: AnalysisResult (issues + strengths + metrics)    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. REPORT GENERATION                                        │
├─────────────────────────────────────────────────────────────┤
│ - JSON structuré (machine-readable)                        │
│ - Markdown formaté (human-readable, style Sonar)           │
│   * Résumé visuel avec emojis                             │
│   * Issues triées par sévérité                             │
│   * Exemples do/don't pour chaque issue                   │
│   * Points forts du code                                   │
│   * Recommandations actionnables                           │
└─────────────────────────────────────────────────────────────┘
```

**Performance estimée (50 fichiers)** :
- Parsing : ~2-5 secondes
- Sélection : ~0.1 secondes
- Context prep : ~1 seconde
- LLM analysis : ~30-60 secondes
- Report gen : ~0.5 secondes
- **Total : 35-70 secondes** ✅

**Budget tokens (50 fichiers)** :
- Architecture overview : 1K
- 50 fichiers compacts : 10K
- 10 fichiers complets : 30K
- Règles : 5K
- Prompt template : 4K
- **Total input : ~50K tokens** (~$0.15)
- Output : ~8K tokens (~$0.12)
- **Coût total : ~$0.27 par analyse** ✅

## Règles d'analyse (Version PoC)

**Format** : Fichiers Markdown dans `rules/default/` (extensible dès le PoC)

**Règles par défaut (5 règles)** :
1. **solid-d.md** : Dependency Inversion Principle (SOLID-D)
2. **solid-s.md** : Single Responsibility Principle (SOLID-S)
3. **dry.md** : Don't Repeat Yourself
4. **naming.md** : Conventions de nommage (variables, fonctions, classes)
5. **complexity.md** : Fonctions trop complexes (responsabilités multiples)

**Structure d'une règle** :
```markdown
# Nom de la règle (ex: Dependency Inversion Principle)

**Catégorie** : Architecture / Code Quality / Performance / Security
**Sévérité** : Critical / Major / Minor

## Description
[Explication du principe]

## Pourquoi c'est important
[Impact sur maintenabilité, testabilité, etc.]

## ❌ Mauvaise pratique
```python
[Code à éviter]
```

## ✅ Bonne pratique
```python
[Code recommandé]
```

## Détection
[Comment identifier cette violation]
```

**Chargement des règles** :
```python
# Loader automatique depuis rules/
def load_rules(rules_dir: Path = Path("rules/default")) -> list[str]:
    """Charge toutes les règles Markdown du répertoire"""
    rules = []
    for rule_file in sorted(rules_dir.glob("*.md")):
        rules.append(rule_file.read_text())
    return rules
```

**Extensibilité** :
- ✅ Règles par défaut : `rules/default/` (fournies avec l'outil)
- 🔮 Règles custom : `rules/custom/` (ajoutées par l'utilisateur, Phase 2)
- 🔮 Règles d'équipe : Partageables via Git (Phase 2)

## Output du PoC

### Format JSON
```json
{
  "summary": {
    "total_issues": 12,
    "critical": 2,
    "major": 5,
    "minor": 5
  },
  "issues": [
    {
      "id": "CC-001",
      "severity": "major",
      "category": "architecture",
      "title": "Infrastructure dependency in application layer",
      "description": "Why it's problematic...",
      "location": "src/application/use_cases/foo.py:15",
      "code_snippet": "from infrastructure.sql import Engine",
      "recommendation": "How to fix...",
      "examples": {
        "bad": "...",
        "good": "..."
      }
    }
  ],
  "strengths": ["What's well done"],
  "recommendations": ["General improvements"]
}
```

### Format Markdown
- En-tête avec métadonnées (date, projet, architecture)
- Résumé visuel (emojis, compteurs)
- Issues détaillées par sévérité avec exemples
- Points forts du code
- Recommandations générales

## Usage (Phase 1 PoC - Parser fonctionnel)

✅ **Actuellement implémenté** :
```bash
# Setup
cd clean-code-analyzer
uv sync                    # Installe les dépendances

# Analyse : Parser CLI (AST + Architecture detection)
uv run python -m src.analyzer /path/to/project

# Exemple : Analyser le projet lui-même
uv run python -m src.analyzer /Users/julienvalera/Projets/perso/clean-code-analyzer/src

# Output : Tableau récapitulatif + Architecture detection panel (Rich formatting)
#
# 📊 Project Analysis Summary
# ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
# ┃ Metric              ┃ Value┃
# ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
# │ Total Files         │    6 │
# │ Total Lines         │  548 │
# │ Average Complexity  │ 9.50 │
# └─────────────────────┴──────┘
```

🔮 **Phase 2 - Planifié** :
```bash
# Options à venir
uv run python -m src.analyzer /path/to/project \
  --output ./reports \
  --format both  # json, markdown, ou both

# Multi-agents spécialisés
uv run python -m src.analyzer /path/to/project \
  --agents clean-code,security,performance
```

## Roadmap

### Phase 1 : PoC Minimal + Quality Infrastructure ✅ COMPLÉTÉ

**Objectif** : Valider l'approche LLM pour l'analyse de code + mettre en place l'infrastructure de qualité

**Implémentation** (10-12-2024 - Complété) :

**PoC Core** :
- ✅ Parser AST avec métriques de complexité (cyclomatique + cognitive via radon)
- ✅ Architecture detection (hexagonal/layered patterns via heuristics)
- ✅ Dataclasses models pour structure de données cohérente
- ✅ Entry point CLI avec logging structuré (logging + Rich)
- ✅ Beautiful output avec Rich (tables + panels + syntax highlighting)
- ✅ Type hints modernes (Python 3.13 syntax : `|` pour unions)
- ✅ Imports absolus (meilleure lisibilité)
- ✅ Test sur Olbia backend (1710 fichiers, 586K LOC) - Hexagonal architecture detected 90% confidence

**Quality Infrastructure** :
- ✅ GitHub Actions CI/CD (lint, test, quality gate)
- ✅ Pre-commit hooks (ruff lint/format + ty type check)
- ✅ Ruff configuration (lint + format)
- ✅ Ty type checker integration
- ✅ Coverage reporting (80%+ enforcement)
- ✅ Pytest avec coverage + HTML reports
- ✅ Build system (hatchling + uv)
- ✅ Packaging (Python 3.13 entry point setup)

**Code Quality** :
- ✅ No print() statements (structured logging only)
- ✅ Modern configuration (dependency-groups.dev)
- ✅ Type checking avec ty (strict mode)
- ✅ All tests passing (pytest: 3/3)
- ✅ Coverage 80%+ (enforced via CI)
- ✅ Ruff lint rules configured
- ✅ Coding rules documented (.claude/coding-rules.md)

**Livrable** :
- CLI fonctionnel "pyromai" capable d'analyser n'importe quel projet Python
- Infrastructure de qualité enterprise-ready (CI/CD, pre-commit, testing, coverage)
- Package distributable (pip install pyromai)

---

### Phase 2 : MVP Complet (2-3 semaines)

**Objectif** : Améliorer performance, extensibilité et multi-agents spécialisés

**Architecture multi-agents** :
- 🔮 **BaseAgent abstraction** : Interface commune pour tous les agents
- 🔮 **Agents spécialisés optionnels** :
  - `CleanCodeAgent` (déjà présent dans PoC)
  - `SecurityAgent` : SAST (SQL injection, XSS, secrets, OWASP Top 10)
  - `PerformanceAgent` : N+1 queries, memory leaks, complexité algorithmique
  - `AWSWellArchitectedAgent` : 5 piliers AWS (operational excellence, security, reliability, performance, cost)
- 🔮 **Orchestrateur multi-agents** : Parallélisation avec `asyncio.gather`
- 🔮 **CLI avec flags** : `--agents clean-code,security,performance`
- 🔮 **Fusion intelligente des résultats** : Déduplication, agrégation des scores
- 🔮 **Coût contrôlé** : Activation agent par agent (default : clean-code only)

**Performance** :
- 🔮 Compaction sémantique avancée (80% gain tokens)
- 🔮 Repository map (inspiration Aider)
- 🔮 Analyse multi-niveaux (Architecture → Modules → Fichiers ciblés)
- 🔮 Parallélisation multi-agents (indépendants)

**Qualité** :
- 🔮 Métriques avancées (couplage afférent/efférent, cohésion LCOM)
- 🔮 Tests unitaires + intégration
- 🔮 Règles custom utilisateur (`rules/custom/`)
- 🔮 Configuration par projet (`.analyzer.yml`)

**UX** :
- 🔮 Mode `--dry-run` (estimation coût/durée par agent)
- 🔮 Mode `--summary-only` (architecture uniquement)
- 🔮 Output HTML interactif
- 🔮 Scoring impact/effort (matrice priorités)

---

### Phase 3 : Industrialisation (futures itérations)

**Objectif** : Production-ready et usage en équipe

**Intégration** :
- 🔮 Cache et analyse incrémentale (delta uniquement)
- 🔮 CI/CD integration (GitHub Actions, GitLab CI, pre-commit)
- 🔮 Analyse de MR/PR (changements uniquement)
- 🔮 Baseline comparison (évolution dans le temps)

**Visualisation** :
- 🔮 Dashboard Streamlit (tendances, métriques, graphes)
- 🔮 Exports pour SonarQube, CodeClimate
- 🔮 Badges README (code quality score)

**Extensibilité** :
- 🔮 Support multi-langages (TypeScript, Java, Go via tree-sitter)
- 🔮 Analyses spécialisées : Sécurité (SAST), Performance, AWS Well-Architected
- 🔮 Plugin system (custom analyzers)
- 🔮 Multi-LLM support (GPT-4, Gemini, local models)

## Principes de développement

### Experts Software/ML Engineering
Le projet est développé avec une approche experte :
- Clean Architecture pour l'outil lui-même
- Type hints complet (mypy)
- Tests automatisés (pytest)
- CI/CD dès le départ
- Documentation as code

### Itération et feedback
- Commencer simple (PoC) et valider l'approche
- Itérer selon retours utilisateur réels
- Prioriser valeur métier sur complexité technique

### Extensibilité
Concevoir pour l'évolution :
- Plugin system pour nouvelles règles
- Adapter pattern pour autres LLM providers
- Format de règles extensible (Markdown → DSL custom)

## Variables d'environnement

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...  # Clé API Claude (obligatoire)
```

## Références

### Clean Code & Architecture
- **Clean Code** (Robert C. Martin) - Principes fondamentaux
- **Clean Architecture** (Robert C. Martin) - Dependency Rule, Hexagonal
- **Refactoring** (Martin Fowler) - Catalogue de code smells
- **Domain-Driven Design: Tackling Complexity in the Heart of Software** (Eric Evans) - Conception de logiciels guidés par le domaine métier

### Python Best Practices
- PEP 8 - Style Guide
- PEP 20 - The Zen of Python
- Python Type Hints (PEP 484)

### AWS Well-Architected Framework (Phase 3)
- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization

## Notes d'implémentation

### Choix techniques justifiés

**1. Règles en fichiers Markdown (dès PoC)**
- ✅ Lisible et éditable sans modifier le code
- ✅ Rich content (code formaté, explications détaillées)
- ✅ LLM-friendly (Claude comprend nativement Markdown)
- ✅ Versionnable (Git diff clair)
- ✅ Extensible : utilisateur peut ajouter ses règles custom
- ❌ Rejeté : Hardcoding dans le code (rigidité, rebuild nécessaire)

**2. Sélection intelligente multi-critères**
- ✅ Priorise les fichiers critiques (complexité, taille, couplage)
- ✅ Équilibre couverture architecturale (domain, app, infra)
- ✅ Pas de limite arbitraire (ex: 20 fichiers), mais budget tokens
- ✅ Scalable : fonctionne pour 50 comme 500 fichiers
- ❌ Rejeté : Échantillonnage aléatoire (rate les fichiers importants)

**3. Format compact + code complet (stratégie hybride)**
- ✅ Tous les fichiers en format compact (~200 tokens/fichier)
- ✅ Top N fichiers prioritaires en code complet
- ✅ Gain : 3x plus de fichiers dans le même budget
- ✅ Claude a la vue d'ensemble + détails sur les zones critiques
- 🔮 Phase 2 : Compaction sémantique avancée (80% gain)

**4. Batch analysis (single-pass)**
- ✅ Une seule requête Claude = contexte complet
- ✅ Analyse cohérente (Claude voit tout en même temps)
- ✅ Coût maîtrisé (~$0.27 pour 50 fichiers)
- ✅ Temps raisonnable (30-60s)
- 🔮 Phase 2 : Parallélisation par couche si nécessaire

**5. Prompt en anglais**
- ✅ Claude plus performant en anglais pour tâches techniques
- ✅ Plus d'exemples dans les données d'entraînement
- ✅ Output configurable (français ou anglais selon besoin)
- ❌ Rejeté : Prompt en français (moins performant)

**6. Validation robuste JSON + Retry logic**
- ✅ Extraction JSON même avec markdown wrapper (```json)
- ✅ Validation Pydantic (schema strict)
- ✅ Retry automatique avec backoff exponentiel (tenacity)
- ✅ Robuste face aux erreurs API temporaires
- ❌ Rejeté : JSON parsing naïf (crash si malformé)

**7. Parser stdlib (ast) + radon**
- ✅ PoC : ast suffisant pour structure + imports
- ✅ Radon : métriques objectives (complexité) sans overhead
- ✅ Légères dépendances
- 🔮 Phase 2 : astroid pour inférence de types avancée
- 🔮 Phase 3 : tree-sitter pour multi-langage

**8. CLI local uniquement (PoC)**
- ✅ Pas de déploiement cloud (itération rapide)
- ✅ Privacy : code reste sur machine utilisateur
- ✅ Appels API Claude directs (transparence)
- 🔮 Phase 3 : Option cloud/SaaS si besoin

**9. Agent unique polyvalent (PoC) vs Multi-agents spécialisés (Phase 2)**
- ✅ PoC : Un seul agent CleanCodeAgent avec prompt structuré par catégories
  - Avantages : Simple, un seul appel API (~$0.27), contexte unifié
  - Inconvénient : Moins spécialisé par domaine
- 🔮 Phase 2 : Multi-agents optionnels (clean-code, security, performance, aws)
  - Avantages : Prompts spécialisés, parallélisation, expertise ciblée, activable par flag
  - Coût : ~$0.27 par agent (contrôlable, désactivables par défaut)
  - Architecture : BaseAgent + orchestrateur avec `asyncio.gather`
- ❌ Rejeté : Multi-agents dès le PoC (sur-engineering, coût multiplié sans validation)

**10. uv au lieu de Poetry**
- ✅ uv : Gestionnaire de dépendances ultra-rapide (Rust-based)
- ✅ Compatible avec pyproject.toml (standard Python)
- ✅ Installation : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- ✅ Commandes : `uv sync` (install), `uv run` (execute), `uv add` (add dep)
- ✅ Lock file : `uv.lock` (déterministe)
- ❌ Rejeté : Poetry (plus lent, moins moderne)

## Critères de succès du PoC

1. ✅ Génération de rapport sans erreur sur Olbia backend
2. ✅ Au moins 5 issues détectées avec exemples pertinents
3. ✅ Identification correcte de l'architecture hexagonale
4. ✅ Recommandations actionnables et spécifiques
5. ✅ Format de sortie clair et lisible (JSON + Markdown)
6. ✅ Temps d'analyse raisonnable (< 2 minutes pour ~50 fichiers)

## Synchronisation du contexte

### Pourquoi synchroniser ?

Lorsque tu développes des features sans Claude, le contexte dans ce fichier CLAUDE.md peut devenir obsolète. Pour que Claude reste efficace, il doit avoir une vision à jour du projet.

### Comment synchroniser ?

**Méthode simple** : Utilise la commande personnalisée `/sync`

```bash
# Dans ta conversation avec Claude, tape simplement :
/sync
```

**Ce que fait `/sync`** :
1. Explore tous les fichiers du projet (nouveaux + modifiés)
2. Analyse le code implémenté récemment
3. Détecte les changements d'architecture, dépendances, features
4. Met à jour automatiquement CLAUDE.md :
   - Architecture technique (si changements)
   - Stack technique (nouvelles dépendances)
   - Roadmap (features terminées ✅)
   - Journal des modifications (nouvelle entrée datée)
5. Te présente un résumé des changements détectés pour validation

**Quand synchroniser ?**
- Après avoir développé une nouvelle feature
- Après avoir ajouté des dépendances
- Après avoir changé l'architecture
- Avant de demander de l'aide à Claude sur du nouveau code
- Régulièrement (ex: chaque fin de session de dev)

### Bonnes pratiques

**Avec Git** : Des commits descriptifs aident Claude à mieux comprendre
```bash
git commit -m "feat: Add AST parser with architecture detection

- Implemented parser.py with recursive directory scan
- Added heuristics for hexagonal/layered architecture detection"
```

**Sans Git** : Pas de problème, Claude analyse directement les fichiers

## Journal des modifications

### 2024-12-10 - Phase 1 Complétée : Quality Infrastructure & Enterprise Setup (Julien solo)

**Infrastructure de qualité mise en place** (commits récents) :
- ✅ **GitHub Actions CI/CD** (`fa3f966`) :
  - Workflow lint (ruff check + format check + ty type check)
  - Workflow test (pytest avec coverage HTML/XML + codecov upload)
  - Quality gate (vérification que lint + test réussissent)
  - Configuration : Python 3.13 only (PoC simplifié)
- ✅ **Ruff configuration complète** (`.ruff.toml` dans `pyproject.toml`) :
  - Lint rules : F, E, W, I, N, UP, B, A, C4, SIM, RUF
  - Format rules : double quotes, space indent
  - Per-file ignores (Typer pattern, AST methods)
  - Target version : Python 3.11
- ✅ **Type checker Ty (Astral)** :
  - Intégration dans CI/CD
  - Pre-commit hook pour vérification locale
  - Configuration dans `pyproject.toml`
- ✅ **Pre-commit hooks** (`.pre-commit-config.yaml`) :
  - ruff check + ruff format
  - ty type checker (src/ only)
- ✅ **Coverage enforcement** :
  - pytest-cov avec 80% minimum
  - HTML reports générés automatiquement
  - Upload vers Codecov en CI
- ✅ **Build system** (hatchling) :
  - Package name : "pyromai"
  - Entry point : `pyromai = "analyzer.__main__:main"`
  - Build artifacts générés dans `dist/`
- ✅ **Python version upgrade** :
  - Minimum : Python 3.13
  - `.python-version` file: "3.13"
  - CI/CD matrix : Python 3.13 only
  - Coding rules updatées

**Documentation et packaging** :
- ✅ README.md enrichi avec feature matrix (Pylint/Flake8 vs SonarQube vs Pyromai)
- ✅ Changement de nom du projet : "Clean Code Analyzer" → **"Pyromai"**
- ✅ Branding : Logo + banner assets créés
- ✅ Commits récents bien documentés

**Git history (derniers commits)** :
- `fa3f966` - ci: Simplify to Python 3.13 only (PoC phase)
- `bf4ea13` - ci: Fix duplicate workflow runs and restore full matrix testing
- `4090554` - docs: Update coding rules with quality gates and pre-commit workflow
- `357dd39` - feat: Add quality tooling and CI/CD infrastructure (v0.1.0)
- `4e06e78` - refactor: Replace manual CLI argument parsing with Typer

**État actuel du projet** :
- ✅ CLI entièrement fonctionnel avec typer + rich
- ✅ Parser AST complet avec métriques radon
- ✅ Tests : 3/3 passing avec 80%+ coverage
- ✅ Type checking : ty passe en CI
- ✅ Linting : ruff passe en CI/CD
- ✅ Pre-commit hooks : configuré et prêt
- ✅ Package distributable : wheel + sdist générés

**Prêt pour Phase 2** : Infrastructure solide pour accueillir multi-agents, LLM integration, et features avancées.

---

### 2024-12-10 - Phase 1 PoC Complétée (Refactoring + Coding Standards)

**Refactoring complet du code** (avec Claude) :
- ✅ Suppression de `from __future__ import annotations` (inutile en Python 3.11+)
- ✅ Conversion de TOUS les imports en imports absolus (`from src.analyzer...`)
- ✅ Remplacement complet des `print()` par logging structuré
- ✅ Modernisation des type hints : `Union[A, B]` → `A | B`, `Optional[X]` → `X | None`
- ✅ Refactor majeur de `__main__.py` :
  - Logging configuré avec `RichHandler`
  - Beautiful output avec Rich `Table` et `Panel`
  - Messages de log structurés (lazy formatting)
- ✅ Configuration moderne : Migration de `tool.uv.dev-dependencies` vers `dependency-groups.dev`
- ✅ Documentation des standards : Création de `.claude/coding-rules.md`

**Commits effectués** :
- `5752231` - feat: Implement AST parser with complexity metrics (première version fonctionnelle)
- `70993a6` - refactor: Apply coding standards (Python 3.11+ modern practices)

**Tests et validation** :
- ✅ Tous les imports fonctionnent (absolute imports correctement résolus)
- ✅ Parser testé sur le projet lui-même (6 fichiers, 548 LOC)
- ✅ Parser testé sur Olbia backend (1710 fichiers, 586K LOC)
- ✅ Tous les tests unitaires passent (pytest: 3/3)
- ✅ Type checking passe (mypy: Success)

**Code Quality Metrics** :
- 0 print() statements
- 100% absolute imports
- Modern Python 3.11+ syntax throughout
- Structured logging with Rich
- Beautiful CLI output with tables and panels

---

### 2024-12-10 - Initialisation du projet (avec Claude)
- Création de la structure du projet dans `/Users/julienvalera/Projets/perso/clean-code-analyzer`
- Définition de l'architecture du PoC avec améliorations challengées :
  - Sélection intelligente des fichiers (scoring multi-critères)
  - Format compact + code complet (stratégie hybride)
  - Règles en fichiers Markdown dès le PoC (extensibilité)
  - Validation robuste JSON + Retry logic API
  - Prompt en anglais pour meilleure performance
  - Agent unique polyvalent pour PoC (multi-agents en Phase 2)
  - Migration vers uv (au lieu de Poetry) pour gestion dépendances
- Documentation complète dans CLAUDE.md avec :
  - Architecture technique détaillée
  - Workflow d'analyse (5 étapes)
  - Budget tokens et performance estimée
  - Choix techniques justifiés (10 décisions)
  - Roadmap en 3 phases avec vision multi-agents Phase 2
  - Structure rules/ organisée par domaine (clean-architecture, security, performance, aws)
- Création de la commande `/sync` pour synchronisation automatique
- Création du `.gitignore` pour le projet
- Discussion architecture multi-agents :
  - Décision : Agent unique pour PoC, multi-agents optionnels Phase 2
  - Agents spécialisés : CleanCodeAgent, SecurityAgent, PerformanceAgent, AWSWellArchitectedAgent
  - Orchestration avec asyncio.gather pour parallélisation
  - CLI avec flags `--agents` pour activation sélective

## Auteur & Contexte

- **Développeur** : Julien Valera
- **Expertise** : Software Engineering, ML Engineering
- **Assistant** : Claude (Anthropic) pour conception et implémentation
- **Date de démarrage** : Décembre 2024
