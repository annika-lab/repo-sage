import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.calls = []
        self.inheritance = []

        # context tracking
        self.current_function = None
        self.current_class = None

    def visit_FunctionDef(self, node):
        func_name = node.name

        # If inside class → treat as method
        if self.current_class:
            func_name = f"{self.current_class}.{func_name}"

        self.functions.append(func_name)

        # Track current function
        prev_function = self.current_function
        self.current_function = func_name

        self.generic_visit(node)

        # Restore previous context
        self.current_function = prev_function

    def visit_ClassDef(self, node):
        class_name = node.name
        self.classes.append(class_name)

        # Track inheritance
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.inheritance.append((class_name, base.id))
            elif isinstance(base, ast.Attribute):
                self.inheritance.append((class_name, base.attr))

        # Track current class
        prev_class = self.current_class
        self.current_class = class_name

        self.generic_visit(node)

        self.current_class = prev_class

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")

    def visit_Call(self, node):
        if self.current_function:
            # simple function call → foo()
            if isinstance(node.func, ast.Name):
                callee = node.func.id
                self.calls.append((self.current_function, callee))

            # method call → obj.method()
            elif isinstance(node.func, ast.Attribute):
                callee = node.func.attr
                self.calls.append((self.current_function, callee))

        self.generic_visit(node)

def parse_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        tree = ast.parse(code)

        parser = CodeParser()
        parser.visit(tree)

        return {
            "file": file_path,  # added for context
            "functions": parser.functions,
            "classes": parser.classes,
            "imports": parser.imports,
            "calls": parser.calls,              
            "inheritance": parser.inheritance   
        }

    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return None