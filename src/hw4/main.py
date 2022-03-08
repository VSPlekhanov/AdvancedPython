from hw1.src.plekhanov_hw1 import fibonacci
from time import time
import threading


def measure(f):
    now = time()
    f()
    return time() - now


def use_threads(count, n):
    threads = []
    for _ in range(count):
        t = threading.Thread(target=fibonacci.fibonacci, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


print(measure(lambda: use_threads(10, 500000)))
