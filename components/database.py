'''
module dedicated to defining database stuff

^ that used to be the full desc of this module for a while
but now i'll actually try to explain basic usage



so i won't be getting into how shit gets saved onto your hardrive
how it's structured there and shit

i'll just get into what this database bullshit is about and what it does



so every Context (ctx) object that gts receives in a command has two special attributes attached
these two are "database" and "db". they are both the fucking same, but one is obviously a shortcut to the other
these attributes, as their names suggest, point to the database

things you can do with the Database object:



ctx.database['a'] = 'give me sex' # you just set the database key 'a' to 'give me sex'
print(ctx.database['a']) # prints 'give me sex'



# replace the 'a' key
ctx.database['a'] = 'something else' # 'a' gets overwritten
print(ctx.database['a']) # prints 'something else'



# you're not limited to strings. you can do the same shit with ints and bools
# storing ints
ctx.database['b'] = 5
print(ctx.database['b']) # prints 5, not '5'

# but watch out, this module does this by str to int/bool conversion
# so `ctx.database['b'] = 5` is equivalent to `ctx.database['b'] = '5'`

# storing bools
ctx.database['c'] = True
print(ctx.database['c']) # prints True
ctx.database['d'] = 'no'
print(ctx.database['c']) # prints False

# it actually converts bools the same way that discord.py does when reading messages
# that combined with the str conversion and you get
ctx.database['e'] = 1
print(ctx.database['e']) # prints True
# this is not harmful at all because in python bools are subclasses of int anyway
print(True + True) # prints 2

# similar conversion mechanism happens with keys for ints, but not with bools !
# basically all it does is it converts your argument to a str

# key conversion with ints
ctx.database[5] = 2 # sets key '5' to '2'
print(ctx.database[5]) # prints 2, converted from '2'
print(ctx.database['5']) # prints 2 again

# key conversion with bools (not the same!)
ctx.database[False] = 'it cuts like a knife' # sets the key 'False' to 'it cuts like a knife'
print(ctx.database[False]) # prints 'it cuts like a knife'
print(ctx.database['False']) # prints that edgy shit again
# but there is no ctx.database['no'] or ctx.database[0] ! that would've been retarded anyway



# check if a key is inside the database

print('b' in ctx.database) # prints True, we set it before.
print('5' in ctx.database) # True
print(5 in ctx.database) # True, same shit
print(2 in ctx.database) # False
print('f' in ctx.database) # False



# delete a key

del ctx.database['c'] # deletes key 'c'
print('c' in ctx.database) # False

del ctx.database[5]
print(5 in ctx.database) # False
print('5' in ctx.database) # False

# NOTE: don't try to delete a key that doesn't exist, that's dumb



# congrats, you have scratched 5% of the surface of what databases can do !



# you can have as many layers as you desire to your database

ctx.database['f']['name'] = 'george'
print(ctx.database['f']['name']) # prints 'george'
print('f' in ctx.database) # True
print('name' in ctx.database['f']) # True
print('age' in ctx.database['f']) # False

ctx.database[77][27] = 17
print(77 in ctx.database) # True
print('27' in ctx.database[77]) # True
print(False in ctx.database['77']) # False

ctx.database[77][False] = 'sixsixsix'
print(False in ctx.database['77']) # True

del ctx.database[77]['27']
print(27 in ctx.database[77]) # nein










# now this is where shit gets a bit trippy



# if you access an attribute of a Database object that is not inside its dir()
# it will assume that you're trying to access a key

ctx.database['g'] = 2
print(ctx.database.g) # assumes you mean ctx.database['g'], so 2 is printed
ctx.database.g = 'distortion' # change the value 'g' points to to 'distortion'
print(ctx.database['g']) # prints 'distortion'

# but you can't do `del ctx.database.g` !!!



# same shit with multilayer

ctx.database.john_johnson.kids_raped = 19
print(ctx.database.john_johnson.kids_raped) # 19
print(ctx.database['john_johnson'].kids_raped) # 19
print(ctx.database.john_johnson['kids_raped']) # 19

ctx.database.john_johnson.id = 1234

print(ctx.database.john_johnson.id) # 1234



# using [] instead of . is recommended because it is more explicit








# W.I.P
# a fuckton more to write, this is barely scratching the surface

'''



PATH = '.' # relative file paths in python are relative to the location of the module which imports this module



def initialize(*args):
    '''
    running this function is completely optional for this module
    but you can run it and give it as an argument
    the path in which you would like your 'databases' and 'global database' folders to be
    '''
    global PATH
    PATH, = args



from os import remove, rmdir
from shutil import rmtree

from random import choice, shuffle



from .utilities import (
    Path,
    basic_conv, one_in,
    empty, limit,
    empty_iter, iter_len, iter_rand,
)



class DatFile:
    'interface for .dat files'



    def __init__(self, path):
        self.__dict__['_dat_path'] = path.parent / f'{path.stem}.dat' # suffix will always be .dat



    def __contains__(self, item):
        to_search = f'{item}: '
        return self._dat_path and any(line.startswith(to_search) for line in self._dat_path.lines())



    def __getitem__(self, item):
        if self._dat_path:
            to_search = f'{item}: '
            for line in self._dat_path.lines():
                if line.startswith(to_search):

                    if line.endswith('\n'):
                        line = line[:-1]

                    return basic_conv(line[len(to_search):])

        raise KeyError('why the fuck did you even try this')

    __getattr__ = __getitem__



    def __delitem__(self, item):
        if item not in self:
            raise KeyError('don\'t be so aggressive. there is no key to hurt you')

        to_search = f'{item}: '

        # get ready for the most fuckfest line of code in this module

        self._dat_path.write_text(''.join(filter(lambda line: not line.startswith(to_search), self._dat_path.lines())).strip()) # rewrites the .dat file such that the value is not present anymore, and strips the file

        self._dat_path.strip()


    def __setitem__(self, item, value):
        if item in self:
            del self[item]
        self._dat_path.append(f'{item}: {value}\n')

    __setattr__ = __setitem__



    def __iter__(self):
        if self._dat_path:
            for line in self._dat_path.lines():
                line = line.strip()
                if ': ' in line:
                    yield line.split(': ')[0]



    def __bool__(self):
        return empty_iter(self)



















class LineSet:
    '''
    a set storing strings, all inside a file (.set file) separated by newline characters

    useful for storing strings that contain no newline characters
    '''



    def __init__(self, path):
        self.__dict__['_set_path'] = path.parent / (path.stem + '.set') # will always point to a .set file



    def __lshift__(self, element):

        self._set_path.append(f'{element}\n')

        return self



    def __iter__(self):

        if self._set_path:
            for line in self._set_path.lines():

                if line.endswith('\n'):
                    line = line[:-1]

                if line:
                    yield basic_conv(line)



    def __invert__(self):
        'clear the set'
        self._set_path.unlink_file()
        self._set_path.strip()














class StringSet:
    '''
    interface for .string files

    can store any string into a .string file in given path
    and iterate all stored strings
    it doesn't matter what the string contains, it can even contain newlines
    because each string gets its own cute little jar
    '''


    def __init__(self, path):
        self.__dict__['_path'] = path



    def __lshift__(self, element):
        'adds a string to the set as a .string file'

        new_path = None
        def increment():
            nonlocal nr, new_path
            new_path = self._path / f'{nr}.string'
            nr += 1

        nr = 0
        increment()
        while new_path:
            increment()

        new_path.write_text(element)

        return self



    def __iter__(self):
        for direction in self._path:
            if direction.suffix == '.string':
                string = direction.read_text()
                if string:
                    yield string



    def __invert__(self):
        'clear the set, deleting all .string files'
        for direction in self._path:
            if direction.suffix == '.string':
                direction.unlink_file()








class _AwaitMe:
    'makes the `await (set << attachment1 << attachment2 << ...)` shit possible'

    def __init__(self, coro_call, *, set):
        self.coro_calls = [coro_call]
        self.set = set

    def __lshift__(self, attachment):
        self.coro_calls.extend(self.set.__lshift__(attachment).coro_calls)
        return self

    async def run(self):
        for call in self.coro_calls:
            await call
        return self.set

    def __await__(self):
        return self.run().__await__()










class AttachmentSet:
    'interface for literally fucking everything'


    def __init__(self, path):
        self.__dict__['_path'] = path



    def __lshift__(self, attachment):
        'returns an awaitable which adds the attachment to the set (when awaited ofc)'

        try:
            last_dot = attachment.filename.rindex('.')
            stem, suffix = attachment.filename[:last_dot], attachment.filename[last_dot:]
        except ValueError:
            stem, suffix = attachment.filename, ''

        new_path = self._path / attachment.filename

        nr = 0
        while new_path: # preventing overwrite
            new_path = self._path / (stem + f' ({nr})' + suffix)
            nr += 1

        new_path.assure(force_file = True)
        return _AwaitMe(attachment.save(new_path), set = self)



    def __iter__(self):
        yield from self._path.files() # absorbs literally every file it sees



    def __invert__(self):
        'clears the whole set, by deleting every file it sees'
        for direction in self._path.files():
            direction.unlink_file()















RESERVED = 'string', 'set', 'dat' # all these file types are special and should not be considered attachments
TO_MANGLE = (*RESERVED, 'exe', 'dll') # these are all file suffixes that will be saved with a trailing underscore

_dotify = lambda str_iter: tuple(map(lambda string: '.' + string, str_iter)) # adds a dot to all strings in the tuple

RESERVED_ = _dotify(RESERVED)
TO_MANGLE_ = _dotify(TO_MANGLE)

SET_BUFF_MAGNITUDE = 777 # a vague number denoting how much you're dedicated to sacrifice memory for speed with set buffers

class Set(LineSet, StringSet, AttachmentSet):
    'brings all set types into one'



    def __init__(self, path):

        for attr, value in {
            '_superclasses': (LineSet, StringSet, AttachmentSet),
            '_len': None,
            '_buffer': list(),
        }.items():
            self.__dict__[attr] = value

        for superclass in self._superclasses:
            superclass.__init__(self, path)



    def __lshift__(self, element):

        if self._len is not None:
            self.__dict__['_len'] += 1




        if isinstance(element, int) or isinstance(element, bool):
            element = str(element)



        if isinstance(element, str):
            if '\n' in element:
                return StringSet.__lshift__(self, element)
            return LineSet.__lshift__(self, element)



        # element is assumed to be a discord.Attachment
        if '.' in element.filename:
            if element.filename.split('.')[-1].lower() in TO_MANGLE:
                element.filename += '_' # you know what i'm trying to avoid here

        return AttachmentSet.__lshift__(self, element)






    def __iter__(self):
        for superclass in self._superclasses[:-1]:
            yield from superclass.__iter__(self)

        for direction in self._path.files():
            if direction.suffix.lower() not in RESERVED_:
                yield direction



    def __pos__(self):
        'returns a random element from the set'



        if self._len is None:
            self.__dict__['_len'] = iter_len(self)



        if not self._buffer:

            for element in self:
                if one_in(self._len // SET_BUFF_MAGNITUDE + 1):
                    self._buffer.append(element)

            shuffle(self._buffer)



        return self._buffer.pop()



    def __bool__(self):
        'is there anything in the set?'
        return empty_iter(self)



    def __invert__(self):
        'clears the set by removing any file with a non-reserved type'
        for superclass in self._superclasses[:-1]:
            superclass.__invert__(self)

        for direction in self._path.files():
            if direction.suffix not in RESERVED_:
                direction.unlink_file()

        self._path.strip()

        self.__dict__['_len'] = None
        self.__dict__['_buffer'] = list()



    def __add__(self, other):
        'returns a random element selected from both self and other proportionally to their lengths'
        if self._len is None:
            from_s = +self
        else:
            from_s = None

        if other._len is None:
            from_o = +other
        else:
            from_o = None



        if one_in(other._len // self._len):
            if from_s is None:
                return +self
            else:
                return from_s
        else:
            if from_o is None:
                return +other
            else:
                return from_o



    def __len__(self):

        if self._len is None:
            +self

        return self._len








REPR_LEN = 5 # the max amount of elements to show on a pointer repr

class Pointer(DatFile, Set):
    'points to a path in the database'



    def __init__(self, path):
        super().__init__(path)
        Set.__init__(self, path)



    def __contains__(self, item):
        return str(item) in iter(self)



    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        else:
            return Pointer(self._path / str(item))

    __getattr__ = __getitem__



    def __setitem__(self, item, value):
        super().__setitem__(item, value)

        for attr, value in {
            '_len': None,
            '_buffer': list(),
        }.items():
            self.__dict__[attr] = value

    __setattr__ = __setitem__



    def __delitem__(self, item):
        if super().__contains__(item):
            return super().__delitem__(item)

        if item in self:
            new_path = self._path / str(item)
            if new_path:
                rmtree(new_path, ignore_errors = True)
            else:
                (self._path / f'{item}.dat').unlink_file()

            self._path.strip()
            return

        raise KeyError('the key ran away before you could catch it')



    def __iter__(self):
        # pointer is pointer/dat file mode
        yield from super().__iter__()
        if self._path:
            for direction in self._path:
                if direction.is_dir() or direction.suffix in ('.dat', '.set'):
                    yield direction.stem

        # pointer is Set mode
        yield from Set.__iter__(self)



    def __bool__(self):
        return not empty_iter(self)



    def __repr__(self):

        itr = iter(self)

        cls_name = self.__class__.__name__
        showing_elements = ', '.join( map(repr, limit(itr, REPR_LEN)) )
        there_are_more = ', ...' if not empty(itr) else ''

        angle_brackets = f' <{showing_elements}{there_are_more}>' if showing_elements else ''
        round_brackets = f'({self._path!r})'

        return cls_name + round_brackets + angle_brackets




















class Database(Pointer):
    'represents the interface for a command database'



    def __init__(self, command_name):
        super().__init__(Path(PATH) / 'databases' / command_name)



    def __repr__(self):
        super_repr = super().__repr__()
        parenthesis_opening = super_repr.index('(')
        parenthesis_closing = super_repr.index(')')
        return super_repr[:parenthesis_opening] + f"('{self._path.stem}'" + super_repr[parenthesis_closing + 1:]



class GlobalDatabase(Pointer):
    'represents the interface for the global bot database'


    def __init__(self):
        super().__init__(Path(PATH) / 'global database')
