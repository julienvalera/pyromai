"""Parse Python code and extract metrics using AST."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Union

from .models import (
    ArchitectureDetection,
    ClassMetrics,
    CodebaseIndex,
    FileMetrics,
    FunctionMetrics,
    ImportInfo,
)


class FunctionVisitor(ast.NodeVisitor):
    """Extract function metrics from AST."""

    def __init__(self, source: str):
        self.functions: list = []
        self.source = source
        self.source_lines = source.split('\n')

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self._process_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self._process_function(node, is_async=True)
        self.generic_visit(node)

    def _process_function(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], is_async: bool = False
    ) -> None:
        """Process a function and extract metrics."""
        # Calculate function length
        end_lineno = node.end_lineno or node.lineno
        length = end_lineno - node.lineno + 1

        # Count parameters
        params_count = len(node.args.args)
        params_count += len(node.args.posonlyargs)
        params_count += len(node.args.kwonlyargs)
        if node.args.vararg:
            params_count += 1
        if node.args.kwarg:
            params_count += 1

        # Calculate cyclomatic complexity
        cyclomatic = self._calculate_cyclomatic_complexity(node)
        cognitive = self._calculate_cognitive_complexity(node)

        func_metrics = FunctionMetrics(
            name=node.name,
            lineno=node.lineno,
            col_offset=node.col_offset,
            length=length,
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            parameters_count=params_count,
            is_async=is_async,
        )
        self.functions.append(func_metrics)

    @staticmethod
    def _calculate_cyclomatic_complexity(node: ast.AST) -> int:
        """Calculate cyclomatic complexity (simplified)."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    @staticmethod
    def _calculate_cognitive_complexity(node: ast.AST) -> int:
        """Calculate cognitive complexity (simplified)."""
        complexity = 0
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                complexity += 1
            elif isinstance(child, (ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        return complexity


class ClassVisitor(ast.NodeVisitor):
    """Extract class metrics from AST."""

    def __init__(self):
        self.classes: list = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        # Calculate class length
        end_lineno = node.end_lineno or node.lineno
        length = end_lineno - node.lineno + 1

        # Count methods
        methods_count = sum(1 for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)))

        # Check for __init__
        has_init = any(
            isinstance(item, ast.FunctionDef) and item.name == '__init__'
            for item in node.body
        )

        # Extract parent classes
        parent_classes: list = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                parent_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                parent_classes.append(self._get_attribute_name(base))

        class_metrics = ClassMetrics(
            name=node.name,
            lineno=node.lineno,
            col_offset=node.col_offset,
            length=length,
            methods_count=methods_count,
            has_init=has_init,
            parent_classes=parent_classes,
        )
        self.classes.append(class_metrics)
        self.generic_visit(node)

    @staticmethod
    def _get_attribute_name(node: ast.Attribute) -> str:
        """Get full name of an attribute."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{ClassVisitor._get_attribute_name(node.value)}.{node.attr}"
        return node.attr


class ImportVisitor(ast.NodeVisitor):
    """Extract import information from AST."""

    def __init__(self):
        self.imports: list = []

    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statement."""
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=alias.name,
                    names=[alias.asname or alias.name],
                    lineno=node.lineno,
                    is_relative=False,
                )
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from-import statement."""
        module = node.module or ""
        is_relative = node.level > 0
        names = [alias.name for alias in node.names]

        self.imports.append(
            ImportInfo(
                module=module,
                names=names,
                lineno=node.lineno,
                is_relative=is_relative,
            )
        )


class Parser:
    """Parse Python codebase and extract metrics."""

    def __init__(self, root_path: Union[Path, str]):
        """Initialize parser with root path."""
        self.root_path = Path(root_path)
        if not self.root_path.is_dir():
            raise ValueError(f"Root path must be a directory: {root_path}")

    def parse_project(self) -> CodebaseIndex:
        """Parse entire project and return index."""
        python_files = self._find_python_files()
        file_metrics: dict = {}
        total_lines = 0
        total_imports = 0

        for py_file in python_files:
            try:
                metrics = self._parse_file(py_file)
                if metrics:
                    file_metrics[py_file] = metrics
                    total_lines += metrics.length
                    total_imports += metrics.import_count
            except Exception as e:
                print(f"Warning: Could not parse {py_file}: {e}")

        # Detect architecture
        architecture = self._detect_architecture(file_metrics)

        # Calculate aggregate metrics
        complexities = [
            m.max_cyclomatic_complexity
            for m in file_metrics.values()
            if m.max_cyclomatic_complexity > 0
        ]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0
        max_complexity = max(complexities) if complexities else 0

        return CodebaseIndex(
            root_path=self.root_path,
            python_files=python_files,
            file_metrics=file_metrics,
            architecture=architecture,
            total_files=len(python_files),
            total_lines=total_lines,
            total_imports=total_imports,
            avg_file_complexity=avg_complexity,
            max_file_complexity=max_complexity,
        )

    def _parse_file(self, file_path: Path) -> Union[FileMetrics, None]:
        """Parse a single Python file."""
        try:
            source = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, IOError):
            return None

        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError:
            return None

        # Extract functions
        func_visitor = FunctionVisitor(source)
        func_visitor.visit(tree)

        # Extract classes
        class_visitor = ClassVisitor()
        class_visitor.visit(tree)

        # Extract imports
        import_visitor = ImportVisitor()
        import_visitor.visit(tree)

        # Check for main
        has_main = any(
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == '__name__'
            for node in ast.walk(tree)
        )

        # Calculate metrics
        lines = source.split('\n')
        length = len(lines)
        is_test = '_test' in file_path.name or 'test_' in file_path.name

        # Calculate average complexity
        complexities = [f.cyclomatic_complexity for f in func_visitor.functions]
        max_complexity = max(complexities) if complexities else 0
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0

        return FileMetrics(
            path=file_path,
            name=file_path.name,
            length=length,
            import_count=len(import_visitor.imports),
            class_count=len(class_visitor.classes),
            function_count=len(func_visitor.functions),
            avg_cyclomatic_complexity=avg_complexity,
            max_cyclomatic_complexity=max_complexity,
            imports=import_visitor.imports,
            classes=class_visitor.classes,
            functions=func_visitor.functions,
            has_main=has_main,
            is_test=is_test,
        )

    def _find_python_files(self) -> list[Path]:
        """Find all Python files in project."""
        python_files = []
        for py_file in self.root_path.rglob("*.py"):
            # Skip common exclusions
            if any(
                part in py_file.parts
                for part in ['.venv', '.git', '__pycache__', '.tox', 'node_modules']
            ):
                continue
            python_files.append(py_file)
        return sorted(python_files)

    def _detect_architecture(self, file_metrics: dict[Path, FileMetrics]) -> ArchitectureDetection:
        """Detect architecture pattern from file structure and naming."""
        layers_detected = []
        domain_files = 0
        application_files = 0
        infrastructure_files = 0
        presentation_files = 0

        for file_path in file_metrics.keys():
            parts = file_path.relative_to(self.root_path).parts
            path_str = str(file_path).lower()

            if any(part in ['domain', 'entities', 'models'] for part in parts):
                domain_files += 1
                if 'domain' not in layers_detected:
                    layers_detected.append('domain')

            if any(part in ['application', 'use_cases', 'services', 'app'] for part in parts):
                application_files += 1
                if 'application' not in layers_detected:
                    layers_detected.append('application')

            if any(part in ['infrastructure', 'adapters', 'infra'] for part in parts):
                infrastructure_files += 1
                if 'infrastructure' not in layers_detected:
                    layers_detected.append('infrastructure')

            if any(part in ['presentation', 'api', 'handlers'] for part in parts):
                presentation_files += 1
                if 'presentation' not in layers_detected:
                    layers_detected.append('presentation')

        # Determine pattern
        if domain_files > 0 and application_files > 0 and infrastructure_files > 0:
            pattern = "hexagonal"
            confidence = 0.9 if presentation_files > 0 else 0.7
        elif len(layers_detected) >= 2:
            pattern = "layered"
            confidence = 0.6
        else:
            pattern = "unknown"
            confidence = 0.0

        return ArchitectureDetection(
            pattern=pattern,
            confidence=confidence,
            layers_detected=layers_detected,
            domain_files=domain_files,
            application_files=application_files,
            infrastructure_files=infrastructure_files,
            presentation_files=presentation_files,
        )
