prefix = """
\\documentclass{article}
\\usepackage[T2A]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[russian]{babel}
\\title{test}
\\author{Слава Плеханов}

\\begin{document}

"""
postfix = """
\\hline
\\end{tabular}
\\end{document}
"""

escape_set = {'&', '%', '#', '_', '{', '}', '\\'}


def to_table(arr):
    l = len(arr)
    if l == 0:
        return ''
    result = prefix
    result += '\\begin{tabular}{'
    result += "l".join([" | " for _ in range(len(arr[0]) + 1)])
    result += '}\n'
    result += '\\hline\n'
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            for c in escape_set:
                if c in arr[i][j]:
                    arr[i][j] = arr[i][j].replace(c, '\\' + c)
            result += (' & ' + arr[i][j]) if j != 0 else arr[i][j]
        result += ' \\\\\n' if i != 0 else ' \\\\ \\hline\n'
    result += postfix
    return result


arr1 = [
    ['Writer', 'Year of birth', 'Country of birth'],
    ['Dovlatov', '1941', 'USSR'],
    ['Pelevin', '1962', 'USSR'],
    ['Lem', '1962', 'Poland'],
    ['Sholohov', '1905', 'Russian Empire'],
    ['Remark', '1898', 'Germany'],
    ['Strugatskie', '1925 & 1933', 'USSR']
]

arr2 = [
    ['A', 'B'],
    ['True', 'False']
]

arr3 = [
]

arr4 = ['arr']

print(to_table(arr1))
