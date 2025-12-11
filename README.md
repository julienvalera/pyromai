# Pyromai

<div align="center">
  <img src="./assets/logo.webp" alt="Pyromai Logo" width="120" height="120">
</div>

**Intelligent Python code analysis for Clean Code & Clean Architecture — powered by Claude AI**

Detect architectural violations, SOLID principle breaches, and code quality issues with AI-powered contextual analysis. Get structured reports with real examples and actionable recommendations.

![Pyromai Banner](./assets/banner.webp)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-green.svg)](#)

---

## Why Pyromai?

Unlike traditional linters (Pylint, Flake8) focused on syntax and style, **Pyromai understands architectural patterns and code quality principles through AI**. Think **SonarQube meets Claude**.

| Feature | Pylint/Flake8 | SonarQube | **Pyromai** |
|---------|---------------|----------|-----------|
| Syntax & Style | ✅ | ✅ | ✅ |
| Complexity Metrics | ❌ | ✅ | ✅ |
| Architecture Detection | ❌ | ❌ | ✅ |
| SOLID Principles | ❌ | ⚠ | ✅ |
| Contextual Analysis | ❌ | ⚠ | ✅ |
| Cost | Free | Paid | Free (+ Claude API) |

---

## Quick Start

### Installation

```bash
pip install pyromai
```

Or from source with uv:

```bash
git clone https://github.com/julienvalera/pyromai.git
cd pyromai
uv sync
```

### Setup

1. Get an API key from [Anthropic](https://console.anthropic.com/)
2. Create `.env` file:

```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

### Analyze Your Project

```bash
# After installation: pip install pyromai
pyromai /path/to/your/project

# Or from source:
uv run pyromai /path/to/your/project
```

### Example Output

```
Analysis Report: my-project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Architecture: Hexagonal
Total Issues: 12 (2 Critical, 5 Major, 5 Minor)
Analysis time: 1.2s

Report generated:
  • my-project-report.json
  • my-project-report.md
```

---

## Features

### AI-Powered Analysis
- Contextual understanding of your codebase
- Detects non-obvious architectural issues
- Learns from patterns and conventions

### Architecture Detection
Automatically identifies:
- **Hexagonal (Ports & Adapters)**
- **Layered (N-tier)**
- **Custom** patterns

### Clean Code Rules (PoC)
1. **SOLID-D** - Dependency Inversion Principle
2. **SOLID-S** - Single Responsibility Principle
3. **DRY** - Don't Repeat Yourself
4. **Naming** - Conventions (variables, functions, classes)
5. **Complexity** - Function/class complexity limits

### Structured Reports

**JSON Format** (Machine-readable)
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
      "title": "Infrastructure dependency in application layer",
      "location": "src/application/use_cases/foo.py:15",
      "recommendation": "Move this to the infrastructure layer"
    }
  ],
  "strengths": ["Good separation of concerns", "..."],
  "recommendations": ["Consider implementing..."]
}
```

**Markdown Format** (Human-friendly)
- Clear summary with visual elements
- Issues grouped by severity
- Real code examples (bad vs. good)
- Actionable recommendations
- Architecture insights

---

## Use Cases

Perfect for:
- **Teams** enforcing Clean Code/Architecture standards
- **Code Reviews** at scale
- **Learning** best practices
- **Legacy** codebase modernization
- **Architectural** validation

---

## Architecture

```
pyromai/
├── src/analyzer/
│   ├── __main__.py         # CLI entry point
│   ├── cli.py              # Typer + Rich UI
│   ├── parser.py           # AST parsing & structure detection
│   ├── llm_analyzer.py     # Claude API client & prompts
│   ├── rules.py            # Clean Code rules (Markdown)
│   ├── models.py           # Pydantic data models
│   └── report.py           # JSON + Markdown generators
└── tests/
    └── test_analyzer.py
```

### Technology Stack
- **Python 3.11+** - Core language
- **anthropic** - Claude API client
- **typer** - Modern CLI framework
- **rich** - Beautiful terminal UI
- **pydantic** - Data validation
- **python-dotenv** - Environment configuration
- **uv** - Fast Python package manager

---

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Rules Reference](docs/rules.md)
- [Output Formats](docs/output.md)
- [Roadmap](docs/roadmap.md)

---

## Release & Deployment

### Automated Releases with semantic-release

Pyromai uses **semantic-release** for fully automated versioning, tagging, and publishing. Just follow Conventional Commits, and releases happen automatically!

#### Quick Setup

1. **Create GitHub Token**
   ```bash
   # Go to: https://github.com/settings/tokens/new
   # Scopes: repo + workflow
   # Add to GitHub secrets as: GH_TOKEN
   ```

2. **Create PyPI Tokens**
   ```bash
   # PyPI: https://pypi.org/manage/account/tokens/ → PYPI_API_TOKEN
   # TestPyPI: https://test.pypi.org/manage/account/tokens/ → TESTPYPI_API_TOKEN
   # Add both to GitHub secrets
   ```

3. **Add secrets via GitHub CLI**
   ```bash
   gh secret set GH_TOKEN --repo julienvalera/pyromai --body "ghp_..."
   gh secret set PYPI_API_TOKEN --repo julienvalera/pyromai --body "pypi-..."
   gh secret set TESTPYPI_API_TOKEN --repo julienvalera/pyromai --body "pypi-..."
   ```

#### Making a Release

Just follow **Conventional Commits** on main branch:

```bash
# Patch release (0.1.0 → 0.1.1)
git commit -m "fix: Correct parser bug"

# Minor release (0.1.0 → 0.2.0)
git commit -m "feat: Add new analysis rule"

# Major release (0.1.0 → 1.0.0)
git commit -m "feat!: Redesign CLI interface"
```

Push to main:
```bash
git push origin main
```

GitHub Actions will:
1. ✅ Run quality checks (lint, test, coverage)
2. ✅ Detect version bump from commits
3. ✅ Update `pyproject.toml` version
4. ✅ Update `CHANGELOG.md`
5. ✅ Create git commit + tag
6. ✅ Build package (wheel + sdist)
7. ✅ Publish to TestPyPI
8. ✅ Publish to PyPI (production)
9. ✅ Create GitHub Release

#### Manual Release (Local)

For testing before pushing:

```bash
# Check next version (no changes)
uv run semantic-release version --noop

# Make actual release (requires GH_TOKEN)
export GH_TOKEN="ghp_..."
uv run semantic-release version --push
```

#### Commit Message Format

- **feat**: New feature → MINOR bump
- **fix**: Bug fix → PATCH bump
- **perf**: Performance → PATCH bump
- **docs**, **test**, **ci**, **chore**: No version bump
- **BREAKING CHANGE**: → MAJOR bump

---

## Roadmap

### Phase 1: PoC (✅ Completed)
- [x] Basic parser (AST + directory structure)
- [x] 5 hardcoded rules
- [x] Claude integration
- [x] JSON + Markdown output
- [x] Quality infrastructure (CI/CD, pre-commit, tests)
- [x] Automated releases with semantic-release

### Phase 2: MVP (Q1 2025)
- [ ] Objective metrics (complexity, coupling, cohesion)
- [ ] Multi-level analysis (Architecture -> Modules -> Files)
- [ ] External rule configuration
- [ ] Smart chunking (context window management)
- [ ] Unit & integration tests

### Phase 3: Production (Q2-Q3 2025)
- [ ] Incremental analysis & caching
- [ ] CI/CD integration (GitHub Actions, GitLab CI)
- [ ] Dashboard (Streamlit)
- [ ] Multi-language support (TypeScript, Java, Go)
- [ ] Security (SAST) + Performance analysis
- [ ] PR/MR analysis

---

## Configuration

### Custom Rules (Phase 2)
Define your own rules in Markdown:

```markdown
# My Custom Rule

**Category**: Code Quality
**Severity**: Major

## Description
...

## Detection
...
```

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required
PYROMAI_OUTPUT_DIR=./reports   # Optional
PYROMAI_LOG_LEVEL=INFO        # Optional
```

---

## Examples

### Analyze a Django Project
```bash
pyromai analyze ./my-django-project --format markdown
```

### Analyze with Custom Output
```bash
pyromai analyze ./src --output /tmp/reports --format json
```

### Analyze Specific Path
```bash
pyromai analyze ./src/app --depth 2
```

---

## Contributing

This is an early-stage project. We'd love your feedback and contributions!

- Found a bug? [Open an issue](https://github.com/julienvalera/pyromai/issues)
- Have ideas? [Start a discussion](https://github.com/julienvalera/pyromai/discussions)
- Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## Acknowledgments

- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin
- [Clean Architecture](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/) - Robert C. Martin
- [Claude AI](https://claude.ai) - Anthropic
- Inspired by [SonarQube](https://www.sonarqube.org/) and modern linting tools

---

## Contact

- **Author**: Julien Valera
- **Project**: [GitHub](https://github.com/julienvalera/pyromai)

---

**Made with care by engineers who care about code quality**
