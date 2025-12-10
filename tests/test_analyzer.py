"""Tests for the analyzer module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import Parser


def test_parser_initialization():
    """Test parser can be initialized with a valid path."""
    parser = Parser(Path(__file__).parent.parent / "src")
    assert parser.root_path.exists()
    assert parser.root_path.is_dir()


def test_parser_parse_project():
    """Test parser can parse a project."""
    parser = Parser(Path(__file__).parent.parent / "src")
    index = parser.parse_project()

    assert index.total_files > 0
    assert index.total_lines > 0
    assert index.architecture is not None
    assert index.architecture.pattern in ["hexagonal", "layered", "unknown"]


def test_parser_invalid_path():
    """Test parser raises error with invalid path."""
    try:
        Parser("/nonexistent/path")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "must be a directory" in str(e)


if __name__ == "__main__":
    test_parser_initialization()
    test_parser_parse_project()
    test_parser_invalid_path()
    print("All tests passed!")
