import numpy as np
import timeit

print("testing the time for transpose vs enumerate")


def enu():
    allowed_states = {}
    maze = np.random.randint(2, size=(10, 10))
    for index, state in np.ndenumerate(maze):
        if state != 1:
            allowed_states[index] = []


def trans():
    allowed_states = {}
    maze = np.random.randint(2, size=(10, 10))
    s = np.transpose(np.nonzero(maze != 1))
    for x, y in s:
        allowed_states[x, y] = []


print("enumerate")
e = timeit.Timer(enu)
print(e.timeit())
#103.33356400000048

print("transpose")
t = timeit.Timer(trans)
print(t.timeit())
#144.01140609999857
