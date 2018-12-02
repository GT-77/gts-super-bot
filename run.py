import discord as d
from command import commands
import constants, responding, reacting, os
client = d.Client()
def _evaluate(text):
    if text.startswith(constants.prefix):
        text = text[len(constants.prefix):].split(" ")
        commands[text[0]](*text[1:])
        return True
def _respond(message):
    if client.user in message.mentions:
        responding(message.content)
        return True
def _react(message):
    reacting(message.content)
@client.event
async def on_message(message):
    if not _evaluate(message.content):
        if not _respond(message):
            _react(message)
    _react(message.content)
@client.event
async def on_member_join(member):
    commands["evaluate"](member.mention)
client.run(os.environ["TOKEN"])
