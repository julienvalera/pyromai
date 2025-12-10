"""Data models for code analysis using Pydantic."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FunctionMetrics:
    """Metrics for a function."""

    name: str
    lineno: int
    col_offset: int
    length: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    parameters_count: int
    is_async: bool


@dataclass
class ClassMetrics:
    """Metrics for a class."""

    name: str
    lineno: int
    col_offset: int
    length: int
    methods_count: int
    has_init: bool
    parent_classes: list[str]


@dataclass
class ImportInfo:
    """Information about an import."""

    module: str
    names: list[str]
    lineno: int
    is_relative: bool


@dataclass
class FileMetrics:
    """Metrics for a Python file."""

    path: Path
    name: str
    length: int
    import_count: int
    class_count: int
    function_count: int
    avg_cyclomatic_complexity: float
    max_cyclomatic_complexity: int
    imports: list[ImportInfo]
    classes: list[ClassMetrics]
    functions: list[FunctionMetrics]
    has_main: bool
    is_test: bool


@dataclass
class ArchitectureDetection:
    """Detected architecture pattern."""

    pattern: str  # hexagonal, layered, unknown
    confidence: float  # 0.0 to 1.0
    layers_detected: list[str]
    domain_files: int
    application_files: int
    infrastructure_files: int
    presentation_files: int


@dataclass
class CodebaseIndex:
    """Complete index of a codebase."""

    root_path: Path
    python_files: list[Path]
    file_metrics: dict[Path, FileMetrics]
    architecture: ArchitectureDetection
    total_files: int
    total_lines: int
    total_imports: int
    avg_file_complexity: float
    max_file_complexity: int
