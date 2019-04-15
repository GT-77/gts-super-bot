from utilities import multipleinstances
from collections import OrderedDict # gon need this later
PREFIX = "7!" # this is the prefix gts responds to. yes, if you change this you indeed change everything (!!! prefixes and command names should not contain spaces !!!)
NO_DEFAULT = type("NO_DEFAULT", (), dict()) # i use this to mark whenever a parameter has no default value, thus 'None' is a default value and so is '"DEFAULT"', but 'command.NO_DEFAULT' isn't
NO_COMPILING = lambda x: x # function that does no compiling whatsoever and leaves the argument as it is in the message
def _convert(parameter):
    # converts a parameter given as an argument when creating a 'Command' to the normal format of a parameter
    # format of a parameter is the following: (parameter_name, default_value, compiler_function)

    # parameter_name represents the key you will give the 'arg' 'OrderedDict' (or whatever else you called it) inside your command code to access the value
    # default_value represents the value given to 'arg' when the discord message has not specified the value. if you set it to NO_DEFAULT then gts will not treat that argument as optional and will be unhappy when you don't give it a value in your discord message command
    # compiler_function represents a function which takes given value as an argument in string format and returns the useful format. if it returns NO_DEFAULT the input is considered invalid and gts flips the bird

    # examples:
    #   parameter = "xyz"
    #   then return ("xyz", NO_DEFAULT, NO_COMPILING)

    #   parameter = ("amount", "5")
    #   then return ("amount", "5", NO_COMPILING)
    if isinstance(parameter, tuple):
        if len(parameter) < 3:
            parameter += NO_COMPILING,
    else:
        parameter = parameter, NO_DEFAULT, NO_COMPILING
    return parameter

def _write_over_ordered_dict(ordered_dict, lis):
    # updates the 'ordered_dict' 's values by iterating the list 'lis' over them
    # 'lis' gets consumed
    returning = ordered_dict
    for key in returning:
        if lis:
            returning[key] = lis.pop(0)
        else:
            break
    return returning

class Command:
    def __init__(self, func, command_name, *parameters, **options):
        # a Command object needs to be initialized like this:
        #   Command(function, command_name, parameter0, parameter1, ... , option0, option1, ... )
        # !!! parameters with NO_DEFAULT must be given first !!!
        self._func = func
        self.name = command_name
        self._defaults, self._compilers = multipleinstances(OrderedDict, 2)
        for parameter in map(_convert, parameters):
            self._defaults[parameter[0]], self._compilers[parameter[0]] = parameter[1], parameter[2]
    async def run(self, messagecontent):
        # executes command for given message content
        # (this ignores whether the command in the call is the same as this one and just reads the parameters)
        arg = _write_over_ordered_dict(self._defaults, messagecontent.split(" ")[1:]) # write input from the message over default values
        arg = OrderedDict(((parameter, self._compilers[parameter](arg[parameter])) for parameter in arg)) # run validators over values
        if NO_DEFAULT in arg.values():
            return "invalid"
        try:
            await self._func(arg)
        except:
            return "fail"
        return "success"

def command(commandname, *parameters, **options):
    def decorator(func):
        return Command(func, commandname, *parameters, **options)
    return decorator
