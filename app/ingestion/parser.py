import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)

    parser = CodeParser()
    parser.visit(tree)

    return {
        "functions": parser.functions,
        "classes": parser.classes,
        "imports": parser.imports
    }

