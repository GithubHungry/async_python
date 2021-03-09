"""
Coroutines, .send(in gens) ....
Coroutines = generators which can get data from outside.
Notes:
    - .send(args) , second case of using yield operator.
    - .throw(exception) , raise an exception.
Result:
    - Useful info about generators.
    - Average value counter with generators.
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


def subgen():
    x = 'Ready to accept message'
    message = yield x  # g=subgen() -> g.send(None)[:Ready to accept message] -> g.send('text')[message='text']
    print('Subgen received:', message)


class ShitException(Exception):
    pass


@coroutine
def average():
    """Yield average value of all given nums."""
    count = 0
    sum = 0
    average = None
    while True:
        try:
            x = yield average  # .send(value)
        except StopIteration:
            print('Done!')  # Useful code can be here!
            break
        except ShitException:  # we can get into this code-block using gen.throw(ShitException)
            print('Shit exception!')  # Useful code can be here!
            break
        else:
            count += 1
            sum += x
            average = round(sum / count, 2)

    return average  # can get after exception + break, but value we can get only with following commands:
# try:
#     g.throw(ShitException)
# except ShitException as e:
#     print('Average',e.value)
