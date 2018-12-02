import discord as d
import commands, dialogue, constants, os
client = d.Client()
commands._command.utilities.client, commands._command.dialogue.client, commands.utilities.client, dialogue.client = (client,) * 4
commands = commands.commands
async def _evaluate(message):
    if message.content.startswith(constants.prefix):
        cm = message.content[len(constants.prefix):].split(" ")
        await commands[cm[0]](message, *cm[1:])
        return True
async def _respond(message):
    if client.user in message.mentions:
        await responding(message.content)
        return True
def _react(message):
    reacting(message.content)
@client.event
async def on_message(message):
    if not await _evaluate(message):
        await _respond(message)
@client.event
async def on_member_join(member):
    commands["evaluate"](member.mention)
client.run(os.environ["TOKEN"])
