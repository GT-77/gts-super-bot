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
    Group,
    BadArgument, UserInputError, MissingRequiredArgument, CommandNotFound, CheckFailure, CommandOnCooldown, ArgumentParsingError
)

from discord import Forbidden



from .database import Database, GlobalDatabase

from .dialogue import command_reply, ping_reply, passive_reply

from .utilities import one_in, initialize_help, formatting, Logs, ID_OF, Path



from . import kintore # 5th of April 2020 8:30 PM
from datetime import datetime, date, time # this too



SITUATION_DICT = { # this dict pairs errors caught by on_command_error with their corresponding command situations
    (CommandNotFound,) : "success",
    (UserInputError, ArgumentParsingError) : "invalid",
    (CheckFailure,) : "denied",
    (CommandOnCooldown,): 'cooldown',
}



global_database = global_db = gdb = GlobalDatabase() # ... yeah i know






async def type_n_send(location, string):
    'types the given string n sends it to the given location (the location must be a Messageable)'

    if not type_n_send.writing:

        type_n_send.writing = True

        async with location.typing():

            await sleep(len(string) / 10) # gts types at a modest and calm speed of 600 CPM

        type_n_send.writing = False

        return await location.send(string)




type_n_send.writing = False












async def feedback(ctx):
    """
    sends gts' really useful feedback to given context.

    the context must have a 'situation' attribute set,
    otherwise the call doesn't even make any sense
    """
    if ctx.command.options["feedback"]:
        await type_n_send(ctx, command_reply(ctx.command.qualified_name, ctx.situation).format(ctx = ctx))














class GTS(Bot):
    "gts is an unique child, so he needs a subclass of his own"












    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)



        @self.before_invoke
        async def before_invoke(ctx):
            # await ctx.trigger_typing()
            ctx.database = ctx.db = Database(ctx.command.qualified_name.split()[0])

            def log(*sending, sep = ' '):

                self.logs.command_log(ctx, sep.join(map(str, sending)))

            ctx.log = log



        self.logs = Logs(Path('databases') / 'logs' / 'logging' / f'{date.today()}.logs')


















    # i wrapped this so i can customize the 7!help command and add some extra parameters
    def command(self, *args, **kwargs):

        def decorator(func):
            rt = super(GTS, self).command(*args, **kwargs)(func)

            rt.options = kwargs
            rt.options.setdefault("feedback", True)

            initialize_help(rt)

            return rt

        return decorator







    # same here
    def group(self, *args, **kwargs):

        def decorator(func):
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            kwargs.setdefault('invoke_without_command', True)
            kwargs.setdefault('case_insensitive', True)
            rt = super(GTS, self).group(*args, **kwargs)(func)

            rt.options = kwargs
            rt.options.setdefault("feedback", True)



            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            def command(*args, **kwargs):
                # # # # # # # # # # # # # # # # # # # # # # # # # # #
                def decorator(func):
                    rt_ = Group.command(rt, *args, **kwargs)(func)
                    rt_.options = kwargs
                    rt_.options.setdefault('feedback', True)
                    initialize_help(rt_)
                    return rt_
                # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                return decorator
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



            rt.command = command
            return rt
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        return decorator




















    async def reply(self, ctx):
        "makes gts take the thought of replying to the given message in the given context into consideration"

        if ctx.message.content.startswith(self.user.mention) or ctx.message.content.startswith(f"<@!{self.user.id}>"):
            reply_type = ping_reply
        else:
            reply_type = passive_reply
            if not one_in(77):
                return

        await type_n_send(ctx, reply_type(ctx.message.author.id, ctx.message.content).format(ctx = ctx))















    async def invoke(self, ctx):

        '''
        if ctx.command is None:

            if await self.is_function_call(ctx):

                self.logs.log_detected_function_call(ctx)

                cmp = ctx.message.content.split()

                cmp = ['7!function call', cmp[0].split('!')[1]] + cmp[1:]

                msg = ctx.message

                msg.content = ' '.join(cmp)

                ctx = await self.get_context(msg)

                self.logs.log(f'message content evaluated to {ctx.message.content!r}')

            else:

                return False
        '''

        if not ctx.message.content.startswith(self.command_prefix): # not doing `if ctx.command is None` because that surpresses the CommandNotFound exception

            return False



        self.logs.invoke_log(ctx)

        await super().invoke(ctx)

        return True



































    async def evaluate(self, message_content, location, loading_text = "...", guild_owner = False):
        "makes gts evaluate given message content at given location, like it's an actual message / given command"

        self.logs.log(f'evaluating {message_content} at {location}...')
        leech = await location.send(formatting.code(loading_text))
        leech.content = message_content
        if guild_owner:
            leech.author = location.guild.owner

        await self.invoke(await self.get_context(leech))

        await leech.delete()












    function_prefixes = ['F7!', '7F!']

    async def is_function_call(self, ctx):

        for prefix in self.function_prefixes:

            if ctx.message.content.startswith(prefix):

                self.logs.log('func check returning true...')
                return True

        return False


































    async def on_command_completion(self, ctx):

        if hasattr(ctx, "rt"):
            # the return value of every command will be saved into ctx.rt
            # and will be converted by the function in the returning annotation
            # if it doesn't exist then it defaults to str
            await ctx.send(ctx.command.callback.__annotations__.setdefault("return", str)(ctx.rt))

        ctx.situation = "success"
        await feedback(ctx)



























    async def on_command_error(self, ctx, error):

        def set_situation(situation):
            ctx.situation = situation

        def error_is(*error_types):
            for error_type in error_types:
                if isinstance(error, error_type):
                    return True



        if ctx.command is None:
            ctx.command = type("DummyCommand", (), dict(qualified_name = "_NO_COMMAND", options = {'feedback': True})) # set the command to a dummy object. bless duck typing

        ctx.error = error



        for error_types, situation in SITUATION_DICT.items():
            if error_is(*error_types):
                set_situation(situation)
                break
        else:
            set_situation("fail") # not supposed to happen but could happen. if control reaches this point then the bot has some bugs that need to be fixed or it lacks something in its folder environment
            self.logs.uncaught_exception_log(error)
            await super().on_command_error(ctx, error)



        await feedback(ctx)

















    async def gather_data(self, ctx, *ids, txt_db, file_db):
        '''
        if given context has its message author id in given ids
        then it will put the content of the message in the given txt_db
        and the attachments of the message in given file_db

        if no ids are given then it will always gather data no matter who sent the message
        '''

        if (not ids) or ctx.author.id in ids or ctx.channel.id in ids:

            txt_db << ctx.message.content

            for attachment in ctx.message.attachments:

                await (file_db << attachment)
























    gt_workout = kintore.WorkoutSchedule.for_gt()
    workout_notifications_sent = 0



    async def on_message(self, msg):

        ctx = await self.get_context(msg)



        if msg.author == self.user:
            self.logs.sent_message_log(ctx)
            return



        self.logs.new_message_log(ctx)



        try:

            if not await self.invoke(ctx):

                await self.reply(ctx)
                xyz_database = Database('xyz').xyz

                await self.gather_data (

                    ctx,

                    ID_OF.CYNI,
                    ID_OF.MAWSKEETO,
                    ID_OF.MAFFEROZZO,
                    ID_OF.VALACDI,
                    ID_OF.GREATERTHANGREG,
                    ID_OF.MAWSKEETOBROTHER,
                    ID_OF.HIGHGUARD,
                    ID_OF.XBANANA,
                    ID_OF.MARCO,

                    txt_db = xyz_database.matthias_bider,
                    file_db = xyz_database.xyz

                )

        except Forbidden:

            self.logs.log_forbidden(ctx)



        # \/\/\/ 5th of April 2020 workout update \/\/\/

        wn_sending_times = [tup[0]*60 + tup[1] for tup in ( (0, 0), (18, 30) )]
        if (self.workout_notifications_sent < len(wn_sending_times)):
            rn = datetime.now()
            time_rn = (rn - datetime.combine(date.today(), time(0))).total_seconds() / 60
            if (time_rn >= wn_sending_times[self.workout_notifications_sent]):
                await type_n_send (
                    self.get_user(ID_OF.GT),
                    'nigga my duty 2 manage ur workout schedule thru pure math\nheres ur fuckin workout 4 today:'
                    + '\n・do {challenge.pushups} consecutive pushups, then hold a plank for {challenge.v_hold} secondz\n・do {challenge.pullups} consecutive pullups and hang urself for {challenge.bar_hold} seconds'.format(challenge = self.gt_workout.for_today())
                )
                self.workout_notifications_sent += 1;
























    async def on_member_join(self, member):

        self.logs.member_join_log(member)

        storage = global_database.servers[member.guild.id].settings

        if "default_channel" in storage:
            channel = member.guild.get_channel(int(storage.default_channel))
        else:
            channel = member.guild.system_channel



        if channel is None:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    break

            else:
                return

        if channel is not None:
            await self.evaluate(f"7!rerole {member.id}", channel, guild_owner = True)



















    async def on_message_edit(self, before, after):

        before_ctx = await self.get_context(before)
        after_ctx = await self.get_context(after)

        self.logs.message_edit_log(before_ctx, after_ctx)















    async def on_message_delete(self, msg):

        ctx = await self.get_context(msg)

        self.logs.message_delete_log(ctx)
























#
