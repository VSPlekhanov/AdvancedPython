prefix = """
\\documentclass{article}
\\usepackage[T2A]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[russian]{babel}
\\title{test}
\\author{Слава Плеханов}

\\begin{document}
\\begin{tabular}{"""

postfix = """
\\hline
\\end{tabular}
\\end{document}
"""

escape_set = {'&', '%', '#', '_', '{', '}', '\\'}


class Appendable:
    def __init__(self, state):
        self.state = state

    def append(self, additional):
        return Appendable(self.state + additional)

    def get(self):
        return self.state


class Optional:
    def __init__(self, state):
        self.state = state

    def compute_if_present(self, func):
        return func() if self.state else ''


def to_table(array):
    def escape(sentence):
        return ''.join(map(lambda c: c if c not in escape_set else '\\' + c, sentence))

    def handle_line(line):
        return " & ".join(map(lambda y: escape(y), line))

    def create_table(arr):
        return Appendable(prefix)\
            .append("l".join(map(lambda x: " | ", range(len(arr[0]) + 1))))\
            .append('}\n\\hline\n')\
            .append(handle_line(arr[0]))\
            .append(' \\\\ \\hline\n')\
            .append("\\\\\n".join(map(lambda x: handle_line(x), arr[1:])))\
            .append("\\\\\n" if len(arr) > 1 else '')\
            .append(postfix)\
            .get()

    return Optional(array).compute_if_present(lambda: create_table(array))


tests = [
    [
        ['Writer', 'Year of birth', 'Country of birth'],
        ['Dovlatov', '1941', 'USSR'],
        ['Pelevin', '1962', 'USSR'],
        ['Lem', '1962', 'Poland'],
        ['Sholohov', '1905', 'Russian Empire'],
        ['Remark', '1898', 'Germany'],
        ['Strugatsky', '1925 & 1933', 'USSR']
    ],
    [
        ['A', 'B'],
        ['True', 'False']
    ],
    [],
    ['a', 'b', 'c']
]
for i, test in enumerate(tests):
    with open(f"artifacts/out_table_{i}.tex", 'a') as out:
        out.write(to_table(test))
