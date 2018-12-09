import discord as d
import components as comp
client = d.Client()
comp.initialize(client)
async def _evaluate(message):
    if message.content.startswith(constants.prefix):
        cm = message.content[len(constants.prefix):].split(" ")
        try:
            await comp.commands[cm[0]](message, *cm[1:])
        except KeyError:
            await comp.sub.fur.feedback(message, cm[0], "INVALID")
        return True
async def _respond(message):
    if client.user in message.mentions:
        await comp.reply(message)
        return True
@client.event
async def on_message(message):
    if not await _evaluate(message):
        await _respond(message)
@client.event
async def on_member_join(member):   pass
    #commands["evaluate"](member.mention)
client.run(os.environ["TOKEN"])
