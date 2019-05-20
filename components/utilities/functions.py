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



def empty_iter(iterable, *, return_from_iterator = False):
    return empty(iter(iterable), return_from_iterator = return_from_iterator)



def iter_len(iterable):
    'counts the length of an iterable'
    length = 0
    while True:
        try:
            next(iterable)
        except StopIteration:
            break
        length += 1
    return length



def iter_index(iterable, index):
    iterator = iter(iterable)
    for i in range(index):
        next(iterator)
    return next(iterator)



def basic_conv(string):
    "handles converting from string to bool or int when reading values in the database"
    lowered = string.lower()

    if lowered in ("yes", "y", "true", "t", "1", "enable", "on"):
        return True
    if lowered in ("no", "n", "false", "f", "0", "disable", "off"):
        return False

    try:
        return int(string)
    except ValueError:
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
