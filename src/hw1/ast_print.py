import ast
import graphviz
import time
import re

node_labels = ['name', 'id', 'value', 'attr', 'arg']
node_children = ['args', 'body', 'targets', 'elts', 'comparators', 'items']
node_child = ['value', 'left', 'right', 'iter', 'target', 'args', 'annotation', 'func', 'test', 'context_expr',
              'optional_vars']
labels_black_list = {'Name', 'Constant'}
edges_black_list = {'elts': '', 'test': '', 'comparators': 'right', 'context_expr': 'expr', 'optional_vars': 'as'}
ops_map = {'Add': '+', 'Sub': '-', 'Eq': '==', 'Mul': '*', 'Div': '/'}
color_map = {'Constant': 'burlywood', 'Name': 'green', 'arg': 'green', 'Call': 'orange', 'Return': 'orange',
             'For': 'orange', 'With': 'orange', 'If': 'orange', 'Expr': 'orange', 'Assign': 'orange',
             'Tuple': 'orange', 'Attribute': 'pink', 'withitem': 'orange', 'FunctionDef': 'gold', 'Module': 'grey',
             'Add': 'aqua', 'Mul': 'aqua', 'Sub': 'aqua', 'Div': 'aqua', "Eq": 'aqua', 'nEq': 'aqua'}
node_black_list = {'arguments': 'args'}


class MyVisitor(ast.NodeVisitor):
    def __init__(self, G):
        self.G = G

    @staticmethod
    def get_labels(node_params):
        labels = []
        for label_name in node_labels:
            if label_name in node_params and not isinstance(node_params[label_name], ast.AST):
                labels.append(re.escape(repr(node_params[label_name])).strip('\''))
        label = " ".join(labels)
        return label

    @staticmethod
    def get_name(name, label):
        if not label:
            return name
        if name in labels_black_list:
            return label
        return f'{name}: {label}'

    @staticmethod
    def get_unique_id():
        return str(time.time())

    def add_node(self, node_id, label, name):
        color = color_map[name] if name in color_map else 'white'
        self.G.node(node_id, label, fillcolor=color, style='filled')

    def visit_or_skip(self, node, parent, relation_name):
        name = type(node).__name__
        if name not in node_black_list:
            self.add_edge(parent, node, relation_name)
            self.visit(node)
        else:
            n = node.__dict__[node_black_list[name]]
            if type(n) == list:
                for x in n:
                    self.add_edge(parent, x, relation_name)
                    self.visit(x)
            else:
                self.add_edge(parent, n, relation_name)
                self.visit(n)

    def add_edge(self, parent, child, name):
        if name not in edges_black_list:
            self.G.edge(parent, str(id(child)), label=name)
        else:
            self.G.edge(parent, str(id(child)), label=edges_black_list[name])

    def add_ops(self, ops, node_id):
        for op in ops:
            name = type(op).__name__
            label = f'{ops_map[type(op).__name__]}' if name in ops_map else name
            self.add_node(node_id, label, name)

    def generic_visit(self, node: ast.AST) -> None:
        parent_id = str(id(node))
        name = type(node).__name__
        node_params = node.__dict__
        label = self.get_labels(node_params)
        ops = node_params['ops'] if 'ops' in node_params else [node_params['op']] if 'op' in node_params else []
        if ops:
            self.add_ops(ops, parent_id)
        else:
            self.add_node(parent_id, self.get_name(name, label), name)

        for child_name in node_child:
            if child_name in node_params and isinstance(node_params[child_name], ast.AST):
                child = node_params[child_name]
                self.visit_or_skip(child, parent_id, child_name)

        for children_name in node_children:
            if children_name in node_params and isinstance(node_params[children_name], list):
                for child in node_params[children_name]:
                    self.visit_or_skip(child, parent_id, children_name)


if __name__ == '__main__':
    with open("fibonacci.py", 'r') as fibonacci:
        ast_object = ast.parse(fibonacci.read())
        dot = graphviz.Digraph('round-table', comment='The Round Table')
        v = MyVisitor(dot)
        v.visit(ast_object)
        dot.render(directory='artifacts', view=True)