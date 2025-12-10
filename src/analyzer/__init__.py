"""Clean Code Analyzer - CLI tool for analyzing Python code quality."""

from src.analyzer.models import (
    ArchitectureDetection,
    ClassMetrics,
    CodebaseIndex,
    FileMetrics,
    FunctionMetrics,
    ImportInfo,
)
from src.analyzer.parser import Parser

__version__ = "0.1.0"
__all__ = [
    "Parser",
    "CodebaseIndex",
    "FileMetrics",
    "FunctionMetrics",
    "ClassMetrics",
    "ImportInfo",
    "ArchitectureDetection",
]
