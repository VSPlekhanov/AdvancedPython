import test_data
import subprocess
from plekhanov_hw1 import ast_print


def prefix(graphic_path):
    return """
    \\documentclass{article}
    \\usepackage[T2A]{fontenc}
    \\usepackage[utf8]{inputenc}
    \\usepackage[russian]{babel}
    \\title{test}
    \\usepackage{graphicx}
    \\graphicspath{ {%s} }
    \\author{Слава Плеханов}
    
    \\begin{document}""" % graphic_path


separator = """
    \\hfill \\break
    \\hfill \\break
    \\hfill \\break
    \\hfill \\break
    \\hfill \\break
"""

title_table = """
    \\begin{center}
        Amazing Table:
    \\end{center}
"""

title_picture = """
    \\begin{center}
        Fantastic Picture:
    \\end{center}
"""

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

    def compute_if_present(self, func, default):
        return func() if self.state else default


def to_table_with_picture(array, graphic_path, picture_name):
    def escape(sentence):
        return ''.join(map(lambda c: c if c not in escape_set else '\\' + c, sentence))

    def handle_line(line):
        return " & ".join(map(lambda y: escape(y), line))

    def create_table(arr):
        return Appendable(prefix(graphic_path)) \
            .append(title_table) \
            .append('\\begin{tabular}{') \
            .append("l".join(map(lambda x: " | ", range(len(arr[0]) + 1)))) \
            .append('}\n\\hline\n') \
            .append(handle_line(arr[0])) \
            .append(' \\\\ \\hline\n') \
            .append("\\\\\n".join(map(lambda x: handle_line(x), arr[1:]))) \
            .append("\\\\\n" if len(arr) > 1 else '') \
            .append('\\hline') \
            .append('\\end{tabular}') \
            .append(separator) \
            .append(title_picture) \
            .append('\\includegraphics[scale=0.15]{%s}' % picture_name) \
            .append('\\end{document}') \
            .append(postfix) \
            .get()

    return Optional(array).compute_if_present(lambda: create_table(array), '')


if __name__ == '__main__':
    path = 'artifacts/'
    filename = 'tree'
    ast_print.render(path, filename)
    for i, test in enumerate(test_data.get_tests()):
        res = to_table_with_picture(test, path, filename + '.png')
        if len(res) > 0:
            curr_file = f"artifacts/out_table_{i}.tex"
            with open(curr_file, 'w') as out:
                out.write(res)
            subprocess.run(["latexmk", "-cd", "-pdf", curr_file])
            subprocess.run(["latexmk", "-cd", "-c", curr_file])



