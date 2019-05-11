"""
module dedicated to defining database stuff
"""



PATH = "." # relative file paths in python are relative to the location of the module which imports this module



def initialize(*args):
    """
    running this function is completely optional for this module
    but you can run it and give it as an argument
    the path in which you would like your 'databases' and 'global database' folders to be
    """
    global PATH
    PATH, = args



from os import remove, rmdir
from pathlib import Path
from shutil import rmtree

from .utilities import append, lines, assure, strip, basic_conv



class DatFile:
    "class that abstration-ates (?) database files"



    def __init__(self, path):
        self.__dict__["_dat_path"] = path.parent / f"{path.stem}.dat" # suffix will always be .dat
        self.__dict__["_path"] = path.parent / path.stem # will never have a suffix



    def __contains__(self, item):
        to_search = f"{item}: "
        return self._dat_path.exists() and any(line.startswith(to_search) for line in lines(self._dat_path))



    def __getitem__(self, item):
        if self._dat_path.exists():
            to_search = f"{item}: "
            for line in lines(self._dat_path):
                if line.startswith(to_search):
                    return basic_conv(line[len(to_search): -1])

        raise KeyError("why the fuck did you even try this")

    __getattr__ = __getitem__



    def __delitem__(self, item):
        if item not in self:
            raise KeyError("don't be so aggressive. there is no key to hurt you")

        to_search = f"{item}: "

        # get ready for the most fuckfest line of code in this module

        self._dat_path.write_text("\n".join(filter(lambda line: not line.startswith(to_search), self._dat_path.read_text().split("\n")))) # rewrites the .dat file such that the value is not present anymore

        strip(self._dat_path)


    def __setitem__(self, item, value):
        if item in self:
            del self[item]
        assure(self._dat_path)
        append(f"{item}: {value}\n", self._dat_path)

    __setattr__ = __setitem__



    def __iter__(self):
        if self._dat_path.exists():
            for line in lines(self._dat_path):
                line = line.strip()
                if ": " in line:
                    yield line.split(": ")[0]



    def __bool__(self):
        try:
            next(iter(self))
        except StopIteration:
            return False
        return True



class Pointer(DatFile):
    "class that points to a path in the database"



    def __contains__(self, item):
        return str(item) in iter(self)



    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        else:
            return Pointer(self._path / str(item))

    __getattr__ = __getitem__



    def __delitem__(self, item):
        if super().__contains__(item):
            return super().__delitem__(item)

        if item in self:
            new_path = self._path / str(item)
            if new_path.exists():
                rmtree(new_path, ignore_errors = True)
            else:
                remove(self._path / f"{item}.dat")

            strip(self._path)
            return

        raise KeyError("the key ran away before you could catch it")



    def __iter__(self):
        yield from super().__iter__()
        if self._path.exists():
            for direction in self._path.iterdir():
                if direction.is_dir() or direction.suffix == ".dat":
                    yield direction.stem



class Database(Pointer):
    "represents the interface for a command database"



    def __init__(self, command_name):
        super().__init__(Path(PATH) / "databases" / command_name)



class GlobalDatabase(Pointer):
    "represents the interface for the global bot database"


    def __init__(self):
        super().__init__(Path(PATH) / "global database")
