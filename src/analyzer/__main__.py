"""Entry point for Clean Code Analyzer CLI."""

import sys
from pathlib import Path

from .parser import Parser


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m analyzer <project_path>")
        print("Example: python -m analyzer /path/to/project")
        return 1

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return 1

    try:
        print(f"Analyzing project: {project_path}")
        parser = Parser(project_path)
        index = parser.parse_project()

        print(f"\nProject Summary:")
        print(f"  Total files: {index.total_files}")
        print(f"  Total lines: {index.total_lines}")
        print(f"  Total imports: {index.total_imports}")
        print(f"  Average complexity: {index.avg_file_complexity:.2f}")
        print(f"  Max complexity: {index.max_file_complexity}")
        print(f"\nArchitecture Detection:")
        print(f"  Pattern: {index.architecture.pattern}")
        print(f"  Confidence: {index.architecture.confidence:.1%}")
        print(f"  Layers detected: {', '.join(index.architecture.layers_detected)}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
