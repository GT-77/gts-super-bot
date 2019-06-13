"""
this is the most low-level module

it's dedicated to defining the most basic functions
that are mostly not even tied to discord or gts in particular
"""



from random import randrange # used in the one_in function



def nonempty(iterator, *, return_from_iterator = False):
    "checks if given iterator is not exhausted"
    try:
        value = next(iterator)
        if return_from_iterator:
            return value
    except StopIteration:
        return False
    return True



def empty(iterator, *, return_from_iterator = False):
    "checks if given iterator is exhausted"
    try:
        value = next(iterator)
        if return_from_iterator:
            return value
    except StopIteration:
        return True
    return False



def limit(iterator, count):
    'iterates maximum count elements from the iterable'

    while count:
        yield next(iterator)
        count -= 1


def empty_iter(iterable, *, return_from_iterator = False):
    return empty(iter(iterable), return_from_iterator = return_from_iterator)



def iter_len(iterable):
    'counts the length of an iterable'
    iterator = iter(iterable)

    length = 0
    while True:
        try:
            next(iterator)
        except StopIteration:
            break
        length += 1

    return length



def iter_index(iterable, index):
    iterator = iter(iterable)
    for i in range(index):
        next(iterator)
    return next(iterator)




def iter_rand(iterable, length):
    return iter_index(iterable, randrange(length))



class takewhile:

    def __init__(self, condition, iterable):

        self.condition = condition
        self.iterator = iter(iterable)
        self._tw_mode = True

    def __next__(self):

        if self._tw_mode:

            self._next = next(self.iterator)

            if condition(self._next):

                return self._next

            else:

                self._tw_mode = False
                self.condition_breaker = self._next
                self._to_return_cb = True

                raise StopIteration



        if self._to_return_cb:

            self._to_return_cb = False

            return self.condition_breaker



        return next(self.iterator)


    def __iter__(self):

        return self













def basic_conv(string):
    # "handles converting from string to bool or int when reading values in the database"
    # lowered = string.lower()
    #
    # if lowered in ("yes", "y", "true", "t", "1", "enable", "on"):
    #     return True
    # if lowered in ("no", "n", "false", "f", "0", "disable", "off"):
    #     return False
    #
    # try:
    #     return int(string)
    # except ValueError:
    #     return string

    return string



def neutralize(word, container):
    "sees if the lowered singular form of a word fits in the container, and returns found match"
    lowered = word.lower()
    if lowered in container:
        return lowered
    if lowered.endswith("s"):
        singular = lowered[:-1]
        if singular in container:
            return singular



def word_in_container(string, container):
    "returns the first word from the string that is inside the container, returns None if no word is inside"
    for ignored_character in "~!@#$%^&*()_+{}:\"|<>?-=[];'\,./'":
        string = string.replace(ignored_character, "")

    for line in string.split("\n"):
        for word in line.split():
            match = neutralize(word, container)
            if match is not None:
                return match



def one_in(x):
    "has a one in x chance to return True instead of False"
    return not randrange(x) # it doesn't get more elegant than this, i'm telling you



def exponential_randrange(start, stop = None, step = 1, exponentialness = 2):
    'has a lower and lower chance of returning something more distant from start'

    if stop is None:

        stop = start
        start = 0



    rt = stop - 1

    for i in range(exponentialness):

        rt = randrange(start, rt + 1, step)

    return rt









def indent(string, amount = 1, style = '   '):

    string = str(string)

    indent = style * amount

    return '\n'.join(indent + line for line in string.split('\n'))
