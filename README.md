# Pyromai

**Intelligent Python code analysis for Clean Code & Clean Architecture — powered by Claude AI**

Detect architectural violations, SOLID principle breaches, and code quality issues with AI-powered contextual analysis. Get structured reports with real examples and actionable recommendations.

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
git clone https://github.com/yourusername/pyromai.git
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
pyromai analyze /path/to/your/project

# With options
pyromai analyze /path/to/project \
  --output ./reports \
  --format both  # json, markdown, or both
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

## Roadmap

### Phase 1: PoC (In Progress)
- [x] Basic parser (AST + directory structure)
- [x] 5 hardcoded rules
- [x] Claude integration
- [x] JSON + Markdown output

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

- Found a bug? [Open an issue](https://github.com/yourusername/pyromai/issues)
- Have ideas? [Start a discussion](https://github.com/yourusername/pyromai/discussions)
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
- **Project**: [GitHub](https://github.com/yourusername/pyromai)

---

**Made with care by engineers who care about code quality**
