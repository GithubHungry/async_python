"""
Generator intro.
    1) Generator it is a function with yield and it returns control back.
    2) Maybe more than 1 yield in one gen_function.
    3) next() move function execution to the next yield.
Round Robin cycle example.
Unique file name generation.
"""

import time


def gen1(name):
    for letter in name:
        yield letter


def gen2(n):
    for num in range(n):
        yield num


g1 = gen1('Vadim')
g2 = gen2(5)

# Round Robin cycle :
tasks = [g1, g2]  # Queue of tasks

while tasks:  # While have at least one task in queue
    task = tasks.pop(0)  # Get first task from queue, and remove it from queue

    try:
        i = next(task)
        print(i)  # Here must be a useful task!! + here we can get control
        tasks.append(task)  # If gen isn`t exhausted
    except StopIteration:  # Catch errors
        pass


# ----------------------------------------------
def get_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time.time() * 1000)
        yield pattern.format(str(t))
        print('a')


gen = get_filename()

for i in range(20):
    time.sleep(1)
    print(next(gen))
