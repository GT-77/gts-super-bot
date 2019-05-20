"""
module dedicated to defining all commands on a GTS instance

run.py will import the instance, bring everything together and make some last touches
before making the bot jump into action
"""



from asyncio import sleep

from random import choice

from types import SimpleNamespace

from typing import Optional, Union




from discord import (
    Member, TextChannel, Role,
    Colour, Emoji,

    File,
)

from discord.ext.commands import (
    Greedy,
    is_owner, is_nsfw, guild_only, has_role, has_permissions,
    Converter,
    BadArgument,
)



from .structure import GTS, global_database, global_db, gdb

from .utilities import formatting, files, folders



gts = GTS("7!", case_insensitive = True)
gts.remove_command("help") # there is no help, motherfucker








class CommandConverter(Converter):
    async def convert(self, ctx, argument):
        command = gts.get_command(argument)
        if command is None:
            raise BadArgument
        return command









r_txt = restriction_texts = SimpleNamespace (
    is_owner = "you must be dad to use this command so basically forget anything",
    is_nsfw = "u must b in a nsfw channel 2 use this command",
    guild_only = "can only be used in a server",

    manage_roles = "can only be used by niggas with role managing permissions",
    admin = "u must be admin 2 use this",
)



































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
    restrictions = (r_txt.manage_roles, r_txt.guild_only),
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

    storage = global_database[ctx.guild.id].scans

    if save_file in storage:
        del storage[save_file]

    storage = storage[save_file]

    for member in ctx.guild.members:
        storage[member.id] = " ".join(str(role.id) for role in member.roles)




























@gts.command (
    aliases = [
        "give_roles_back",
        "rr"
    ],
    brief = "reroles a member",
    restrictions = (r_txt.manage_roles, r_txt.guild_only),
    examples = {
        "@HighGuard": "to rerole highguard (if it be an actual mention)",
        "285495766179512331": "to rerole member with that id (which happens 2 b mafferozzo)"
    }
)
@has_permissions(manage_roles = True)
@guild_only()
async def rerole(ctx, member:Member):
    """
    if 7!scan was executed in the server while given member was inside
    then this command will role them precisely with the roles the member had
    at the time of scanning

    exceptionally useful for members that left and joined back roleless
    """
    storage = global_database[member.guild.id].scans.recent

    if member.id in storage:
        await member.edit(reason = "4 my homies", roles = filter(bool, (member.guild.get_role(int(id_)) for id_ in storage[member.id].split())))



















































@gts.command (
    name = "set",
    brief = "sets a server setting to a value",
    restrictions = (r_txt.guild_only, r_txt.admin),
    examples = {
        "default_channel #general": "to make me remember that the default channel of this server is #general (if it's an actual channel mention)",
        "default_channel 314400771796107265": "to set default_channel to the channel with the id 314400771796107265 (if it exists)",
    }
)
@has_permissions(administrator = True)
@guild_only()
async def set_(ctx, setting, value:Union[Member, TextChannel, Role, Colour, Emoji, bool, int, str]):
    """
    currently the only possible setting is default_channel so yeah i know that's pretty fucking boring
    """

    approved_settings = dict (
        default_channel = TextChannel,
    )

    if setting in approved_settings and isinstance(value, approved_settings[setting]):
        storage = global_database[ctx.guild.id].settings

        if hasattr(value, "id"):
            storage[setting] = value.id
        else:
            storage[setting] = value

    else:
        raise BadArgument(f"{setting}: {value} pair is invalid")





























@gts.command (
    aliases = [
        "kobayas",
        "koba",
    ],
    brief = "does a miss kobayashi's dragon maid dot transition thingy",
    examples = {
        "": "and u get a normal MKDM transition",
        '4 1 :gay_pride_flag: " " ur really fucking gay': "and u'll c what u get when u try it"
    }
)
async def kobayashi (
    ctx,
    length:int = 5,
    speed:float = 1.0,
    dot_style = '・',
    spacing = '',

    *,
    custom_transition = None
):



    """
    that's pretty much it
    (here's the transitions i mean btw: https://www.youtube.com/watch?v=L2Rc6ie8_TQ)



    jk

    if you're looking at this help message rn u probably saw all those optional parameters
    like "custom_transition" and "speed" and shit
    and thought to urself "wtf holy shit lma ;o can i fuck with this"
    the answer is yes, u can
    this command is not as inoccent as it seems

    "length" represents the amount of placeholder dots present.
    if there's more dots than the length of the transition then some dots will remain forever unreplaced xyz

    "speed" is the speed at which the dots get replaced. the default speed of 1 is precisely 2 dots per second

    "dot_style" is the look of each placeholder dot (which is obv ・ in bold). u can change dat to anythin

    "spacing" is the spacing between each dot. default is nothing


    last but neva least is "custom_transition". this is a parameter that eats up the rest of ur command so u can set it to whatev u want
    witout worrying bout quotes n shit. im lazy to explain so find out urself wat that is bout
    """



    if custom_transition is None:

        if "transitions" in ctx.database:
            transition_full_text_choice = choice(ctx.database.transitions.split()).split('_')
        else:
            raise Exception("wtf where my MKDM transitions") # bail out. this is not supposed to happen

    else:
        transition_full_text_choice = custom_transition.split()



    transition_text = [dot_style] * length

    transition_msg = await ctx.send(formatting.bold(spacing.join(transition_text)))

    for index in range(length):

        if transition_full_text_choice:
            transition_text[index] = transition_full_text_choice.pop(0)

            await sleep(0.5 / speed)
            await transition_msg.edit(content = spacing.join(transition_text))

        else:
            break






































@gts.command (
    brief = "xyz",
    restrictions = [
        "xyz",
    ],
    examples = {
        "": "xyz",
    },
    feedback = False,
)
async def xyz(ctx, xyz = "xyz"):
    "xyz"

    abc = f"files/xyz/{xyz}/"
    jason_brown = list(files(abc))

    for lil_marco in (xyz, "n", "liquid_xyz"):
        if lil_marco not in ctx.db:
            raise BadArgument(lil_marco) # xyz

    if not jason_brown:
        raise BadArgument(abc) # terry davis

    def CHRIS_BROWN(xyz):
        return choice(list(filter(bool, xyz.split("|||")))).strip()

    # xyz
    await ctx.send( CHRIS_BROWN(ctx.db.xyz + '||| ' + ctx.db.liquid_xyz), file = File(choice(jason_brown), CHRIS_BROWN(ctx.db.n)) )














































































































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
