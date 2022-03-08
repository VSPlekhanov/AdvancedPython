from hw1.src.plekhanov_hw1 import fibonacci
from time import time

t = time()
[fibonacci.fibonacci(250000) for _ in range(10)]
print(time() - t)