"""
module dedicated to defining the fundamental structure of gts

like the handling of commands,
the handling of command errors,
the handling replies,
the handling of databases (todo), etc

this module defines all this stuff on the GTS subclass (of Bot)
which commands.py will import, and define all commands on an instance of it
"""



from asyncio import sleep

from discord.ext.commands import (
    Bot,
    BadArgument, UserInputError, MissingRequiredArgument, CommandNotFound, CheckFailure
)

from .database import Database, GlobalDatabase

from .dialogue import command_reply, ping_reply, passive_reply

from .utilities import one_in, initialize_help, formatting



SITUATION_DICT = { # this dict pairs received errors received by on_command_error with corresponding command situations
    (CommandNotFound,) : "success",
    (MissingRequiredArgument, BadArgument, UserInputError) : "invalid",
    (CheckFailure,) : "denied",
}



global_database = global_db = gdb = GlobalDatabase() # ... yeah i know



async def type_n_send(location, string):
    "types the given string n sends it to the given location (the location must be a Messageable)"
    async with location.typing():
        await sleep(len(string) / 10) # gts types at a modest and calm speed of 600 CPM
    return await location.send(string)



async def feedback(ctx):
    """
    sends gts' really useful feedback to given context.

    the context must have a 'situation' attribute set,
    otherwise the call doesn't even make any sense
    """
    await type_n_send(ctx, command_reply(ctx.command.name, ctx.situation).format(ctx = ctx))



class GTS(Bot):
    "gts is an unique child, so he needs a subclass of his own"



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.before_invoke
        async def before_invoke(ctx):
            await ctx.trigger_typing()
            ctx.database = ctx.db = Database(ctx.command.name)



    # i wrapped this so i can customize the 7!help command
    def command(self, *args, **kwargs):

        def decorator(func):
            rt = super(GTS, self).command(*args, **kwargs)(func)

            rt.options = kwargs

            initialize_help(rt)

            return rt

        return decorator



    async def reply(self, ctx):
        "makes gts take the thought of replying to the given message in the given context into consideration"
        if ctx.message.content.startswith(self.user.mention):
            reply_type = ping_reply
        else:
            reply_type = passive_reply
            if not one_in(37):
                return

        await type_n_send(ctx, reply_type(ctx.message.author.id, ctx.message.content).format(ctx = ctx))



    async def evaluate(self, message_content, channel, loading_text = "..."):
        "makes gts evaluate given message content at given channel, like it's an actual given command"

        leech = await channel.send(formatting.code(loading_text))
        leech.content = message_content
        leech.author = channel.guild.owner

        await self.invoke(await self.get_context(leech))

        await leech.delete()





    async def on_command_completion(self, ctx):
        if hasattr(ctx, "rt"):
            # the return value of every command will be saved into ctx.rt
            # and will be converted by the function in the returning annotation
            # if it doesn't exist then it defaults to str
            await ctx.send(ctx.command.callback.__annotations__.setdefault("return", str)(ctx.rt))

        ctx.situation = "success" # yeah didn't bother to write a set_situation for this one, i mean it's just one statement
        await feedback(ctx)



    async def on_command_error(self, ctx, error):

        def set_situation(situation):
            ctx.situation = situation

        def error_is(*error_types):
            for error_type in error_types:
                if isinstance(error, error_type):
                    return True



        if ctx.command is None:
            ctx.command = type("DummyCommand", (), dict(name = "_NO_COMMAND")) # set the command to a dummy object. bless duck typing



        for error_types, situation in SITUATION_DICT.items():
            if error_is(*error_types):
                set_situation(situation)
                break
        else:
            set_situation("fail") # not supposed to happen but could happen. if control reaches this point then the bot has some bugs that need to be fixed
            print("wtf", type(error), error)



        await feedback(ctx)



    async def on_message(self, msg):
        if msg.author == self.user:
            return

        ctx = await self.get_context(msg)

        if msg.content.startswith(self.command_prefix):
            await self.invoke(ctx)
        else:
            await self.reply(ctx)



    async def on_member_join(self, member):
        storage = global_database[member.guild.id].settings

        if "default_channel" in storage:
            channel = member.guild.get_channel(storage.default_channel)
        else:
            channel = member.guild.default_channel

        if channel is None:
            return

        await self.evaluate(f"7!rerole {member.id}", channel)























#
