# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-10

### Added
- **AST Parser**: Recursive Python code parsing with abstract syntax tree analysis
- **Complexity Metrics**: Cyclomatic and cognitive complexity calculation via radon
- **Architecture Detection**: Heuristic-based detection of hexagonal and layered architectures
- **CLI Interface**: User-friendly command-line interface with Typer + Rich formatting
- **Beautiful Output**: Rich tables and panels for visual project analysis
- **Code Metrics**: LOC counting, import analysis, function/class extraction
- **Modern Python**: Full support for Python 3.13+ with modern syntax (union types, etc.)

### Infrastructure
- **GitHub Actions**: CI/CD workflow for linting, testing, and quality gates
- **Pre-commit Hooks**: Automated code formatting and type checking with ruff + ty
- **Testing**: Comprehensive test suite with pytest and 80%+ coverage enforcement
- **Type Safety**: Full type hints with ty type checker integration
- **Package Distribution**: Wheel and source distribution builds via hatchling

### Documentation
- Complete README with feature matrix and usage examples
- CLAUDE.md project context and development guide
- .claude/coding-rules.md for Python 3.13+ standards
- Inline code documentation and docstrings

### Quality Standards
- Structured logging with Rich (no print statements)
- Absolute imports throughout codebase
- Modern Python type hints (PEP 604, PEP 613)
- Ruff configuration for consistent code style
- Comprehensive .gitignore for Python projects

## [Unreleased]

### Planned for v0.2.0
- Multi-agent architecture (CleanCodeAgent, SecurityAgent, PerformanceAgent)
- LLM integration with Claude API
- Intelligent file selection with multi-criteria scoring
- Context optimization for LLM analysis
- Custom rule loading from Markdown files
- JSON and Markdown report generation
- Batch analysis with retry logic

### Planned for v0.3.0
- Advanced caching and incremental analysis
- Parallel multi-agent execution
- HTML interactive report output
- Configuration via `.analyzer.yml`
- Support for additional LLM providers
