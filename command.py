import discord as d
import os
commands = dict()
def command(name):
    def functionality(message):
        core(message)
    def decorator(core):
        return core
    commands.update({name: functionality})
    return decorator
def __getitem__(self, item):
    return self.commands[item]
