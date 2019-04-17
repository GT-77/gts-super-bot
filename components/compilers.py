from command import NO_DEFAULT
def comp(Class):
    def comp_(x):
        try:
            return Class(x)
        except ValueError:
            return NO_DEFAULT
    return comp_

comp_int = comp(int)
comp_bool = comp(bool)
comp_float = comp(float)
