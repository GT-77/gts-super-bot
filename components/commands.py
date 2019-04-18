# module dedicated to defining all converter functions and commands
from command import command, get_command, NO_DEFAULT, NO_CONVERTER, NO_COMMAND, PREFIX
client, reply = (None,) * 2
from dialogue import command_reply as reply
def initialize(*args):
    # this module requires a discord.Client and the command_reply function from dialogue.py, which it should grab from run.py
    # the reason i don't just do 'from dialogue import command_reply as reply' is because it's a massive waste of memory to import it more than once
    global client, reply
    client, reply = args

async def message(content):
    print(content)

def converter(func):
    # nicer to use None instead of NO_DEFAULT for simpler converters that don't have None as a conviled value
    def wrapper(argument):
        conviled = func(argument)
        if conviled is None:
            conviled = NO_DEFAULT
        return conviled
    return wrapper

def conv(Class):
    # returns a very basic converter for given Class
    @converter
    def wrapper(argument):
        try:
            return Class(argument)
        except ValueError:
            return
    return wrapper

# COMPILERS #

conv_int = conv(int) # converter for integer parameters
conv_float = conv(float) # converter for floating point parameters

@converter
def conv_bool(argument):
    # converter for boolean parameters
    argument, tf = argument.lower(), dict(true = True, false = False)
    if argument in tf:
        return tf[argument]

# COMMANDS #

@command("add", "a", "b")
async def add(arg):
    "adds 2 numbers"
    if arg["a"] == arg["b"] == "1":
        result = arg["a"] + arg["b"]
    else:
        result = "idk"
    await message(f"```{arg['a']}+{arg['b']}={result}```")

# # # # # # # # # # # # # # # # # # # # # #

async def evaluate(message_):
    # the ultimate function that evaluates the command in given message_
    if message_.content.startswith(PREFIX):
        command = get_command(message_.content.split()[0][len(PREFIX):])
        print("command", command.name)
        await message(reply(command.name, await command.run(message_.content)))
