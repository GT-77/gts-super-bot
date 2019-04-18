PREFIX = "7!" # this is the prefix gts responds to. yes, if you change this you indeed change everything
NO_DEFAULT = type("NO_DEFAULT", (), dict()) # i use this to mark whenever a parameter has no default value
NO_CONVERTER = lambda x: x # function that does no compiling whatsoever and leaves the argument in its string format
commands = list() # used to store all commands declared

def get_command(command_name):
    # returns the command named 'command_name'. if it doesn't exist then it returns the command 'NO_COMMAND'
    for command in commands:
        if command.name == command_name:
            return command
    return NO_COMMAND

 #### how this shit works ####
# so every command gts knows will be written something like this:

#     @command(command_name, parameter1, parameter2, ... , option1 = x, option2 = y ...)
#     async def some_func(arg):
#         do_shit

# let's break the shit down

# - command_name is the name of the command. you call it by doing "7!command_name". the name you set to some_func in the code doesn't matter

# - parameters are like slots that can be filled with values in your message
#   for example in the expression "7!slap jerome 13", the hypothetical command "slap" which, let's say, slaps someone x times (the command doesn't exist so don't try it)
#   receives the arguments "jerome" and "13" to its first and second parameter
#   a parameter in code can be written 3 ways:
#       1) just a hashable value like a string (except tuple). ex: "value", "a", 46
#       2) a tuple containing a hashable value and a string. ex: ("a", "13"), ("towho", "highguard then"), (None, "@bebas")
#       3) a tuple containing a hashable value and a converter function. ex: ("name", lambda x: x + " from autoglass"), (77, comp_int)
#       4) a tuple containing a hashable value, a string, and a converter function. ex: ("slapcount", "1", comp_int), ("betaXB", "5ABX72ABA2", lambda gega: gega if "72" in gega else NO_DEFAULT)
#       5) a Parameter instance. ex: Parameter("index", converter = lambda x: "highguard" in x)
#   (i'll explain these shortly)
#   a 'Parameter' object has the following variable attributes: name, default_value, and the converter
#   when you declare an instance of Parameter, the only must-give argument is the name. default_value and converter are optional
#   if the default_value has not been set, that parameter is marked as 'necessary' by gts. which means that if you don't give it a value in your message gts will flip the bird
#   if default_value has been set, that parameter is marked as 'optional'. which means that if you don't give it a value in your message then it's ok, gts will just pretend you gave it default_value and get the job done with no fuss or remorse
#   if the converter has not been set, the value given in your message remains in its string format and gets delivered in your 'arg' dictionary raw (which i will get into later)
#   if the converter has been set, the argument given to your parameter will get passed to the converter you set, and the return value of the converter will be the value you get in your 'arg' dict
#   a converter can get an argument and deem it as invalid by returning NO_DEFAULT. in that case gts will call you out for bullshit and not do anythin. ex: "456bABX;1" given to comp_int returns NO_DEFAULT cuz that ain't lookin like a number 2 me. (i'll declare comp_int later in converters.py)
#   default_value is marked as nonexistent with NO_DEFAULT, and the converter with NO_CONVERTER
#   so now knowing that let's explain the writing
#   let's start with the tuple containing the hashable value, string and converter. so, obviously, when you write that, the first element is the parameters name, second is the default_value, and third is the converter. so it's like this (name, default_value, converter)
#   when you write a tuple containing a hashable value and a string, gts pretends you wrote (hashable_value, string, NO_CONVERTER)
#   when you write a tuple containing a hashable value and a function, gts pretends you wrote (hashable_value, NO_DEFAULT, function)
#   when you only write a hashable value, gts pretends you wrote (hashable_value, NO_DEFAULT, NO_CONVERTER)
#   when you write a Parameter instance, gts doesn't pretend or do anything and just takes the Parameter instance as it is, throwing the whole tuple shortcut thing out the window
#       XXX IMPORTANT: necessary parameters MUST be given first XXX
#       anything like this might result in gts doing unexpected shit: @command("a", "b", ("c", "foo"), "d")

# - i'm getting into 'arg' next because it's tightly related to what i've just covered about parameters
#   if it's not obvious enough already, it stands for arguments and it's literally that. just a dict containing all parameter names of your command as keys and converted values grabbed from the message as corresponding values
#   (of course, the name 'arg' is just a convention i made for myself when creating commands. it's a function parameter so you can name it 'p3n1s' aswell and access your values through the 'p3n1s' dictionary)

# - options are literally just that. options for the command. there are no available options as of now.


# - do_shit is your code. in this code you have access to all arguments given and shit.
# TODO: i should add fancy database access too
 #### done explainin, have fun readin ####
class Parameter:
    def __init__(self, name, default_value = NO_DEFAULT, converter = NO_CONVERTER):
        if not (isinstance(default_value, str) or default_value is NO_DEFAULT): # this handles the 3rd parameter writing case described in the collection of comments above
            converter = default_value
            default_value = NO_DEFAULT
        self.name = name
        self.default_value = default_value
        self.convert = converter
    def kvpair(self, argument = None):
        if argument is None:
            argument = self.default_value
        return {self.name: self.convert(argument)}
    def is_necessary(self):
        return self.default_value is NO_DEFAULT
    def is_optional(self):
        return not self.is_necessary()
    def __repr__(self):
        return f"Parameter({self.name!r}, {self.default_value!r}, {self.convert!r})"
    @classmethod
    def from_decorator_argument(Class, argument):
        # this handles converting from what was given in the decorator to an actual Parameter instance
        if isinstance(argument, Class):
            return argument
        elif isinstance(argument, tuple):
            return Class(*argument)
        else:
            return Class(argument)

class Parameters:
    # this class handles all parameters of a command and the process of taking the message content as input and outputting the contents of the 'arg' dictionary
    def __init__(self, *parameters):
        self.parameters = tuple(Parameter.from_decorator_argument(argument) for argument in parameters)
        self._necessary_parameters = sum(parameter.is_necessary() for parameter in self.parameters)
    def arg(self, message_content):
        # takes the contant of the message as input and returns the 'arg' dict contents
        cm = message_content.split()[1:]
        len_cm = len(cm)
        if len_cm < self._necessary_parameters:
            return None
        for unassigned_parameter in range(len(self.parameters) - len_cm):
            cm.append(None)
        arg_ = dict()
        for parameter, argument in zip(self.parameters, cm):
            arg_.update(parameter.kvpair(argument))
        if NO_DEFAULT in arg_.values():
            return None
        return arg_

class Command:
    def __init__(self, func, command_name, *parameters, **options):
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
        commands.append(Command(func, commandname, *parameters, **options))
        return commands[-1]
    return decorator



@command("_NO_COMMAND")
async def NO_COMMAND(arg):
    "when gts doesn't recognize a command, he runs this command instead"
    return
