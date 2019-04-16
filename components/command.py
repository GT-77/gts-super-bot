from utilities import multipleinstances
from collections import OrderedDict # gon need this later
PREFIX = "7!" # this is the prefix gts responds to. yes, if you change this you indeed change everything (!!! prefixes and command names should not contain spaces !!!)
NO_DEFAULT = type("NO_DEFAULT", (), dict()) # i use this to mark whenever a parameter has no default value, thus 'None' is a default value and so is '"DEFAULT"', but 'command.NO_DEFAULT' isn't
NO_COMPILING = lambda x: x # function that does no compiling whatsoever and leaves the argument as it is in the message

class Parameter:
    def __init__(self, name, default_value = NO_DEFAULT, compiler = NO_COMPILING):
        self.name = name
        self.default_value = default_value
        self.compile = compiler
    def kvpair(self, argument = None):
        if argument is None:
            argument = self.default_value
        return {self.name: self.compile(argument)}
    def is_necessary(self):
        return self.default_value is NO_DEFAULT
    def is_optional(self):
        return not self.is_necessary()

class Parameters:
    def __init__(self, *parameters):
        self.parameters = tuple((Parameter(*(parameter if isinstance(parameter, tuple) else (parameter,))) for parameter in parameters))
        self.necessary_parameters = sum(parameter.is_necessary() for parameter in self.parameters)
    def arg(self, message_content):
        cm = message_content.split(" ")[1:]
        len_cm = len(cm)
        if len_cm < self.necessary_parameters:
            return None
        for i in range(len(self.parameters) - len_cm):
            cm.append(None)
        arg_ = dict()
        for parameter, argument in zip(self.parameters, cm):
            arg_.update(parameter.kvpair(argument))
        return arg_

class Command:
    def __init__(self, func, command_name, *parameters, **options):
        # a Command object needs to be initialized like this:
        #   Command(function, command_name, parameter0, parameter1, ... , option0, option1, ... )
        # !!! parameters with NO_DEFAULT must be given first !!!
        self.func = func
        self.name = command_name
        self.parameters = Parameters(*parameters)
    async def run(self, message_content):
        # executes command for given message content
        # (this ignores whether the command in the call is the same as this one and just reads the arguments)
        arg = self.parameters.arg(message_content)
        if arg is None:
            return "invalid"
        try:
            await self.func(arg)
        except:
            return "fail"
        return "success"

def command(commandname, *parameters, **options):
    def decorator(func):
        return Command(func, commandname, *parameters, **options)
    return decorator
