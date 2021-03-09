"""
Delegation in generators, yield from...
Notes:
    - yield from is equal to await in other languages.
    - delegator must wait for sub_gen during it working time.
    - In sub_gen must be returning code (because delegator can be blocked forever).
Result:
    - Delegator + sub_generator example.
"""
from functools import wraps


def coroutine(func):
    # to avoid typing g.send(None) in each case
    @wraps(func)
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class BlaBlaException(Exception):
    pass


# @coroutine  # with yield from gen in delegator
def sub_gen():
    while True:
        try:
            message = yield
        except StopIteration:
            # print('Hello from sub_gen')
            break  # Code that allow us unlock delegator
        else:
            print('.......', message)
    return 'Returned from sub(gen)'  # Code that allow us unlock delegator


@coroutine
def delegator(gen):  # gen = sub_gen
    """Control sub generator(gives it parameters, throw exceptions, and so on)."""

    # while True:
    #     try:
    #         data = yield
    #         gen.send(data)
    #     except BlaBlaException as e:
    #         gen.throw(e)  # throw to the sub_gen

    result = yield from gen  # Here all data from sub_gen (return) + it`s equal to while True cycle
    print(result)
# Usage:
# g = delegator(sub_gen())
# g.throw(StopIteration)
