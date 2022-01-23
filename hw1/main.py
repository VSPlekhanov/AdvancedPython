def fibonacci(n: int) -> int:
    curr, prev = 1, 1
    for i in range(n - 2):
        tmp = curr + prev
        prev = curr
        curr = tmp
    return curr


if __name__ == '__main__':
    print(fibonacci(int(input())))
