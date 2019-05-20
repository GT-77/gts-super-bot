'''
customizes the Path class from pathlib to suit my godly desires
'''



from pathlib import Path as _Path

from .functions import nonempty, empty_iter



_PathType = type(_Path())



class Path(_PathType):



    def __iter__(self):
        if self.exists() and not self.is_file():
            yield from self.iterdir()



    def assure(self, *, force_file = False):
        'makes sure given path exists, by creating the adequate folders and the file too if given'
        if not self.exists():
            if self.suffix or force_file:
                self.parent.mkdir(parents = True, exist_ok = True)
                self.open('x', encoding = 'UTF-8').close()
            else:
                self.mkdir(parents = True, exist_ok = True)



    def strip(self):
        'basically reverts what assure(...) does, by doing the exact opposite'
        if self.exists():
            if self.is_file():
                if self.read_text(encoding = 'UTF-8'):
                    return

                self.unlink()
                self = self.parent

            while not nonempty(self.__iter__()):
                self.rmdir()
                self = self.parent



    def write_text(self, text, *args, **kwargs):
        kwargs.setdefault('encoding', 'UTF-8')
        self.assure()
        super().write_text(text, *args, **kwargs)



    def append(self, string, *args, **kwargs):
        'appends text to the end of the file with given path'
        kwargs.setdefault('encoding', 'UTF-8')
        kwargs.setdefault('mode', 'a')
        self.assure()
        with self.open(*args, **kwargs) as file:
            file.write(string)



    def read_text(self, *args, **kwargs):
        kwargs.setdefault('encoding', 'utf-8')
        return super().read_text(*args, **kwargs)



    def lines(self, *args, **kwargs):
        'yields lines from the file of the path'
        kwargs.setdefault('encoding', 'UTF-8')
        with self.open(*args, **kwargs) as file:
            yield from file



    def files(self, *suffixes, exclude = False):
        'yields files from given path'
        if suffixes:
            if exclude:
                for subpath in self:
                    if subpath.suffix not in suffixes:
                        yield subpath
            else:
                for subpath in self:
                    if subpath.suffix in suffixes:
                        yield subpath
        else:
            for subpath in self:
                if not subpath.is_dir():
                    yield subpath



    def folders(self):
        'yields all folders from given path'
        for subpath in self:
            if subpath.is_dir():
                yield subpath



    def unlink_file(self):
        if self:
            self.unlink()



    def unlink_folder(self):
        if self.empty():
            self.rmdir()


    __bool__ = _PathType.exists



    def empty(self):
        return empty_iter(self)



    def with_suffix(self, suffix):
        return self.parent / (self.stem + suffix)



    def with_stem(self, stem):
        return self.parent / (stem + self.suffix)









































#
