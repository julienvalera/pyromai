"""Entry point for Clean Code Analyzer CLI."""

import logging
from pathlib import Path

import typer
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

app = typer.Typer(
    name="pyromai",
    help="Analyze Python projects for Clean Code and Clean Architecture violations",
    no_args_is_help=True,
)


@app.command()
def analyze(
    project_path: Path = typer.Argument(
        ..., help="Path to the Python project to analyze", exists=True
    ),
) -> None:
    """Analyze a Python project for code quality issues."""
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

    except Exception:
        logger.exception("Analysis failed")
        raise typer.Exit(code=1)


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
