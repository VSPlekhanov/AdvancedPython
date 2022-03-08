from hw1.src.plekhanov_hw1 import fibonacci
from time import time
import threading
import multiprocessing


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


def use_processes(count, n):
    processes = []
    for _ in range(count):
        p = multiprocessing.Process(target=fibonacci.fibonacci, args=(n,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


if __name__ == '__main__':
    with open("artifacts/result.txt", "w") as out:
        proc_time = str(measure(lambda: use_processes(10, 500000)))
        threads_time = str(measure(lambda: use_threads(10, 500000)))
        out.write(f"Processes time: {proc_time}s\n")
        out.write(f"Threads time: {threads_time}s\n")
