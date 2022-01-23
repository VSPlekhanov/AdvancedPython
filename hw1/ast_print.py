import ast

if __name__ == '__main__':
    with open("fibonacci.py", 'r') as fibonacci:
        ast_object = ast.parse(fibonacci.read())
        print(ast.dump(ast_object))

