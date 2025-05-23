import time
import ast
import inspect
import traceback
import warnings
from collections import defaultdict

# Shared registry for GUI or other tools to access
inspection_results = {}

def getInspect(func):
    def wrapper(*args, **kwargs):
        result_data = defaultdict(str)

        # Start timing
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            exception = None
        except Exception as e:
            result = None
            exception = traceback.format_exc()
        end_time = time.time()

        # Execution time
        result_data["Execution Time"] = f"{end_time - start_time:.4f} seconds"

        # Get source and AST
        try:
            source = inspect.getsource(func)
            tree = ast.parse(source)
        except Exception as e:
            inspection_results[func.__name__] = {
                "error": f"Failed to parse source: {e}"
            }
            return result

        lines = source.splitlines()

        # Line count stats
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
        blank_lines = sum(1 for line in lines if line.strip() == "")
        result_data["Total Lines"] = total_lines
        result_data["Comment Lines"] = comment_lines
        result_data["Blank Lines"] = blank_lines
        result_data["Comment Ratio"] = f"{(comment_lines / total_lines):.2%}" if total_lines > 0 else "0%"

        # Duplicate lines
        duplicates = [line for line in lines if lines.count(line) > 1 and line.strip()]
        result_data["Duplicate Lines"] = len(set(duplicates))

        # Variable Count
        class VarCounter(ast.NodeVisitor):
            def __init__(self):
                self.vars = set()

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    self.vars.add(node.id)

        vc = VarCounter()
        vc.visit(tree)
        result_data["Variable Count"] = len(vc.vars)

        # Nesting Depth
        class DepthCounter(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0

            def generic_visit(self, node):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.FunctionDef)):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    super().generic_visit(node)
                    self.current_depth -= 1
                else:
                    super().generic_visit(node)

        dc = DepthCounter()
        dc.visit(tree)
        result_data["Max Nesting Depth"] = dc.max_depth

        # Cyclomatic Complexity
        class ComplexityCounter(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 1

            def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
            def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
            def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
            def visit_Try(self, node): self.complexity += 1; self.generic_visit(node)
            def visit_BoolOp(self, node): self.complexity += len(node.values) - 1; self.generic_visit(node)

        cc = ComplexityCounter()
        cc.visit(tree)
        result_data["Complexity"] = cc.complexity

        # Import Usage
        class ImportAnalyzer(ast.NodeVisitor):
            def __init__(self):
                self.imports = set()
                self.used = set()

            def visit_Import(self, node):
                for alias in node.names:
                    self.imports.add(alias.name)

            def visit_ImportFrom(self, node):
                if node.module:
                    self.imports.add(node.module)

            def visit_Name(self, node):
                self.used.add(node.id)

        ia = ImportAnalyzer()
        ia.visit(tree)
        unused_imports = ia.imports - ia.used
        result_data["Unused Imports"] = ", ".join(unused_imports) if unused_imports else "None"

        # Runtime Warnings
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            try:
                func(*args, **kwargs)
            except:
                pass  # already handled above
            result_data["Warnings"] = len(caught_warnings)

        # Exception info
        result_data["Exception"] = exception.strip().splitlines()[-1] if exception else "None"

        # Store result in shared registry
        inspection_results[func.__name__] = dict(result_data)

        return result

    return wrapper
