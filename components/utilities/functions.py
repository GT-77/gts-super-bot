"""
module dedicated to defining the most basic and low level functions
that are not even tied to discord or gts in particular
"""


# NOTE: all paths in this module are assumed to be pathlib.Path objects, because i'm hip and cool


from os import remove, rmdir

from random import randrange # used in the one_in function

# from types import SimpleNamespace


def files(path):
    "yields all files from given path"
    for subpath in path.iterdir():
        if not subpath.is_dir():
            yield subpath



def folders(path):
    "yields all folders from given path"
    for subpath in path.iterdir():
        if subpath.is_dir():
            yield subpath



def append(string, path, *args, **kwargs):
    "appends text to the end of the file with given path"
    kwargs.setdefault("encoding", "UTF-8")
    path.write_text(f"{path.read_text()}{string}", *args, **kwargs)



def lines(path, *args, **kwargs):
    "yields lines from the file with given path"
    kwargs.setdefault("encoding", "UTF-8")
    with path.open(*args, **kwargs) as file:
        yield from file



def is_empty(iterator):
    "checks if given iterator is exhausted"
    try:
        next(iterator)
    except StopIteration:
        return True
    return False



def assure(path):
    "makes sure given path exists, by creating the adequate folders and the file too if given"
    if not path.exists():
        if path.suffix:
            path.parent.mkdir(parents = True, exist_ok = True)
            path.open("x", encoding = "UTF-8").close()
        else:
            path.mkdir(parents = True, exist_ok = True)



def strip(path):
    "basically reverts what assure(...) does"
    if path.exists():
        if path.is_file():
            if path.read_text(encoding = "UTF-8"):
                return

            path.unlink()
            path = path.parent

        while is_empty(path.iterdir()):
            path.rmdir()
            path = path.parent



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
        string.replace(ignored_character, "")

    for line in string.split("\n"):
        for word in line.split():
            match = neutralize(word, container)
            if match is not None:
                return match



def one_in(x):
    "has a one in x chance to return True instead of False"
    return not randrange(x) # it doesn't get more elegant than this, i'm telling you
