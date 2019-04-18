# module dedicated to writing compilers
# check command.py for more info
import command as c
NO_DEFAULT = c.NO_DEFAULT

def comp(Class):
    # returns a compiler function for given Class (works for int and float)
    def comp_(x):
        try:
            return Class(x)
        except ValueError:
            return NO_DEFAULT
    return comp_

comp_int = comp(int)
comp_float = comp(float)
something = comp(bool) # idk why i made this one

def comp_bool(x):
    # compiler for boolean
    x = x.lower()
    if x == "true":
        return True
    if x == "false":
        return False
    return NO_DEFAULT
