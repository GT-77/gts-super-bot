import random as r
import os
until = lambda x: r.randint(0, x - 1)
walk = os.walk
def quickread(*options, **options_):
    # returns the content of given file
    with open(*options, encoding = "UTF-8", **options_) as file:
        return file.read()
def quickwrite(content, *options, **options_):
    # writes into given file
    with open(*options, encoding = "UTF-8", **options_) as file:
        return file.write(content)
def filesindir(dir = "."):
    # returns all files in given directory, relative to the folder utility.py is in (components)
    return next(walk(dir))[2]
def foldersindir(dir = "."):
    # returns all folders in given directory, relative to the folder utility.py is in (components)
    return next(walk(dir))[1]
def randomelement(subscriptable):
    # returns a random element from given subscriptable
    return subscriptable[until(len(subscriptable))]
