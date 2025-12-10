"""Entry point for Clean Code Analyzer CLI."""

import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from src.analyzer.parser import Parser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger(__name__)
console = Console()


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] uv run python -m src.analyzer <project_path>")
        console.print("[dim]Example:[/dim] uv run python -m src.analyzer /path/to/project")
        return 1

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        logger.error("Project path does not exist: %s", project_path)
        return 1

    try:
        logger.info("Analyzing project: %s", project_path)
        parser = Parser(project_path)
        index = parser.parse_project()

        # Create summary table
        table = Table(
            title="📊 Project Analysis Summary",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Metric", style="cyan", width=25)
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Files", str(index.total_files))
        table.add_row("Total Lines", f"{index.total_lines:,}")
        table.add_row("Total Imports", str(index.total_imports))
        table.add_row("Average Complexity", f"{index.avg_file_complexity:.2f}")
        table.add_row("Max Complexity", str(index.max_file_complexity))

        console.print(table)

        # Architecture detection panel
        layers = ", ".join(index.architecture.layers_detected) or "None detected"
        arch_text = (
            f"[bold]Pattern:[/bold] {index.architecture.pattern}\n"
            f"[bold]Confidence:[/bold] {index.architecture.confidence:.1%}\n"
            f"[bold]Layers:[/bold] {layers}"
        )
        console.print(
            Panel(arch_text, title="🏗️  Architecture Detection", border_style="blue")
        )

        return 0
    except Exception as e:
        logger.exception("Analysis failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
