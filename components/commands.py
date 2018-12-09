import subcomponents as sub
client = None
command = sub.command.command
commands = sub.command.commands
@command("test")
async def test(message):
    utilities.message("460494504986935316", "hi")
