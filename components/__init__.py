import subcomponents as sub
import commands, replying
componenets = commands, replying
def initialize(client):
    for componenet in componenets:
        component.client = client
        component.sub.initialize(client)
    sub.client = client
    commands = commands.commands
