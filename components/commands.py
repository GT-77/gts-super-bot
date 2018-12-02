import command as _command
import utilities
command = _command.command
@command("test")
async def test(message):
    utilities.message("460494504986935316", "hi")
