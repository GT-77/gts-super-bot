"""
module dedicated to defining all commands on a GTS instance

run.py will import the instance, bring everything together and make some last touches
before making the bot jump into action
"""



from discord import (
    Member, TextChannel, Role,
    Colour, Emoji
)

from discord.ext.commands import (
    Greedy,
    is_owner, is_nsfw, guild_only, has_role, has_permissions,
    Converter,
    BadArgument,
)

from .structure import GTS, global_database, global_db, gdb

from .utilities import formatting



gts = GTS("7!", case_insensitive = True)
gts.remove_command("help") # there is no help, motherfucker








class CommandConverter(Converter):
    async def convert(self, ctx, argument):
        command = gts.get_command(argument)
        if command is None:
            raise BadArgument
        return command








# trivia: this command was used in debugging
@gts.command (
    brief = "adds 2 numbers",
    examples = {
        "1 1": "and u get 2",
        "89 256": "and u should get something between 300 and 350"
    }
)
async def add(ctx, a:int, b:int) -> formatting.codeblock:
    ctx.rt = f"{a} + {b} = {11 if a == b == 1 else 'idk'}"









@gts.command (
    name = "help",
    brief = "offers u help / the command u just entered",
    examples = {
        "add": "and u get help on the add command",
        "scan": "and u get help on the scan command"
    }
)
async def help_(ctx, command:CommandConverter = None):
    """
    u can do 7!help on any command 2 get help on it

    anythin not provided by 7!help is learned thru immersion
    """

    if command is None:
        command = help_

    ctx.rt = command.full_help









@gts.command (
    brief = "scans the server",
    restrictions = ("can only be used by niggas with role managing permissions",)
)
@has_permissions(manage_roles = True)
@guild_only()
async def scan(ctx, *, save_file = "recent"):
    """
    scans the server and stores all roles that every member has
    so when u use the 7!rerole command i will look at the most recent scan n try to give em the roles back

    if u don't want the scan to be overwritten into the same file, you can set the save file name
    but rly the only file i give a shit about when reroling is the one called "recent"
    so yeah the only way to recover the contents of the old save file is to ask dad for it
    """

    storage = ctx.global_database[ctx.guild.id].scans
    for member in ctx.guild.members:
        del storage[save_file]
        storage = storage[save_file]
        storage[member.id] = " ".join(role.id for role in member.roles)









@gts.command (
    name = "omegatest77",
    brief = "ur fucking gay",
    restrictions = (
        "u must be admin to use this command",
        "u must b in a server to use this command",
        "basically forget everything because you need to be dad to use this command, so fuck you."
    ),
    examples = {
        "u2": "and u get me3",
        "u1 0": "distortion",
        "v8 6": "and u get me4",
    }
)
@has_permissions(administrator = True)
@guild_only()
@is_owner()
async def xyzzz(ctx, a:int, b:bool, member:Member, ur_gayness_level:formatting.strikethru_bold_italics = None):
    """
    this is the command description

    2 b cute

    ur like dis
    """
    print(a, b, member.id, ur_gayness_level)

















































































































#
