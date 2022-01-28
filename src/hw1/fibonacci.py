def fibonacci(n: int) -> int:
    curr, prev = 1, 1
    for i in range(n - 2):
        tmp = curr + prev
        prev = curr
        curr = tmp
    return curr


if __name__ == '__main__':
    n = int(input())
    with open("artifacts/out_fibonacci.txt", 'a') as out:
        out.write(str(str(n) + ' : '))
        out.write(str(fibonacci(n)) + '\n')
