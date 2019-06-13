'''

module dedicated to logging

'''



from datetime import date, datetime

from types import SimpleNamespace



from .path import Path

from .formatting import formatting

from .functions import indent



PATH = 'databases/logs'



LOG_STYLE = SimpleNamespace (

    MESSAGE = ('[MSG]', '{ctx.author.display_name} ({ctx.author.id}) has send a message to {ctx.channel.name} ({ctx.channel.id}) of {ctx.guild.name} ({ctx.guild.id})'),
    INVOKE = ('<7!>', '{ctx.command.qualified_name} has been invoked with args {ctx.args!r} at {ctx.channel.name} ({ctx.channel.id}) of {ctx.guild.name} ({ctx.guild.id})'),

    DM = ('(DM)', 'received a DM from {ctx.author.display_name} ({ctx.author.id})'),
    DM_INVOKE = ('<(7!)>', '{ctx.command.qualified_name} has been invoked with args {ctx.args!r} in {ctx.author.display_name}\'s tight asshole'),

    DETECTED_FUNCTION_CALL = ('<7F!>', 'detected function call from {ctx.author.display_name} ({ctx.author.id})'),

    SENT_MESSAGE = ('|MSG|', 'i sent a message to {ctx.channel.name} ({ctx.channel.id}) of {ctx.guild.name} ({ctx.guild.id})'),
    SENT_DM = ('|DM|', 'i sent a dm to {ctx.channel.recipient.display_name} ({ctx.channel.recipient.id})'),

    UNKNOWN_COMMAND_INVOKE = ('<X>7!>', '{ctx.author.display_name} doesn\'t know what he\'s doing'),
    UNKNOWN_COMMAND_DM_INVOKE = ('<X>(7!)>', '{ctx.author.display_name} doesn\'t know what he\'s doing'),

    FORBIDDEN = ('[X]', 'i got an unhandled Forbidden 403 in {ctx.channel.name} ({ctx.channel.id}) of {ctx.guild.name} ({ctx.guild.id})'),

    UNCAUGHT_EXCEPTION = ('<X>', 'i got an uncaught exception, pls fix me gt'),
    FATAL_UNCAUGHT_EXCEPTION = ('<X _ X>', 'a fatal uncaught exception fucked up the run(...) call entirely. i think i\'m gonna try to try to start it back up.'),

    DM_COMMAND_MSG = ('   ', '(log from {ctx.command.qualified_name}) invoked in {ctx.author.display_name}\'s wet #cker candy sugar ({ctx.author.id})) -> '),
    COMMAND_MSG = ('  ', '(log from {ctx.command.qualified_name} invoked in {ctx.channel.name} ({ctx.channel.id})) -> '),

    MEMBER_JOIN = ('/MJ/', '{member.display_name} ({member.id}) has joined {member.guild.name} ({member.guild.id})'),

    MESSAGE_EDIT = ('[*MSG]', '{ctx.author.display_name} ({ctx.author.id}) has edited their message'),

    MESSAGE_DELETE = ('[X]MSG]', '{ctx.author.display_name} ({ctx.author.id}) has deleted their message'),



    AWOKEN = ('/A\\', 'i have woken up. お久しぶり、ご主人様'),

    ASLEEP = ('\\V/', 'i\'m goin 2 sleep. お休み'),











    SEP = ' ',
    # INDENT = '    ',
    LOG_SEPARATION = '\n\n\n\n\n',
    SUBLOG_SEPARATION = '\n\n',
    BRANCHING_MARKER = ':',


)







class Log:



    def __init__(self, tag, header = '', *sublogs, **variables):

        if not isinstance(header, str):

            sublogs = (header,) + sublogs
            header = ''



        self.tag = tag
        self.header = header
        self.sublogs = sublogs
        self.vars = variables

        if 'root_log' in variables:
            self.datetime = datetime.now()
        else:
            self.datetime = None



    def __str__(self):

        if self.datetime is None:
            time = str()
        else:
            time = str(self.datetime) + '\n'

        tag = self.tag

        header = self.header.format(**self.vars)



        root = tag

        if header:
            root += LOG_STYLE.SEP + header



        branches = LOG_STYLE.SUBLOG_SEPARATION.join(map(indent, self.sublogs))

        if branches:
            root += LOG_STYLE.BRANCHING_MARKER + LOG_STYLE.SUBLOG_SEPARATION

        return time + root + branches








    @classmethod
    def message_info(cls, ctx):

        return (

            cls('content:', repr(ctx.message.content)),
            cls('ID:', str(ctx.message.id)),
            cls('sent at:', str(ctx.message.created_at)),
            cls('edited at:', str(ctx.message.edited_at)),
            cls('jump url:', ctx.message.jump_url),

            cls (
                'attachment(s)',
                * (

                    cls (
                        att.filename,
                        cls('url:', att.url),
                        cls('proxy url:', att.proxy_url)
                    )

                    for att in ctx.message.attachments

                )
            ),

        )















    @classmethod
    def msg(cls, ctx):

        return cls (

            LOG_STYLE.MESSAGE[0],
            LOG_STYLE.MESSAGE[1],

            *cls.message_info(ctx),

            ctx = ctx,
            root_log = True,

        )














    @classmethod
    def dm(cls, ctx):

        rt = cls.msg(ctx)

        rt.tag = LOG_STYLE.DM[0]
        rt.header = LOG_STYLE.DM[1]

        return rt







    @classmethod
    def message(cls, ctx):

        if ctx.guild is None:

            return cls.dm(ctx)

        else:

            return cls.msg(ctx)







    @classmethod
    def sent_message(cls, ctx):

        if ctx.guild is None:

            style = LOG_STYLE.SENT_DM

        else:

            style = LOG_STYLE.SENT_MESSAGE



        return cls (

            style[0],
            style[1],

            *cls.message_info(ctx),

            ctx = ctx,
            root_log = True,

        )


















    @classmethod
    def invoke(cls, ctx):

        if ctx.command is ctx.guild is None:

            style = LOG_STYLE.UNKNOWN_COMMAND_DM_INVOKE

        elif ctx.command is None:

            style = LOG_STYLE.UNKNOWN_COMMAND_INVOKE

        elif ctx.guild is None:

            style = LOG_STYLE.DM_INVOKE

        else:

            style = LOG_STYLE.INVOKE




        return cls (

            style[0],
            style[1],

            ctx = ctx,
            root_log = True,

        )








    @classmethod
    def detected_function_call(cls, ctx):

        style = LOG_STYLE.DETECTED_FUNCTION_CALL

        return cls (

            style[0],
            style[1],

            ctx = ctx,
            root_log = True,

        )













    @classmethod
    def forbidden(cls, ctx):

        return cls (

            LOG_STYLE.FORBIDDEN[0],
            LOG_STYLE.FORBIDDEN[1],

            ctx = ctx,
            root_log = True,

        )



    @classmethod
    def command_log(cls, ctx, sending):

        if ctx.guild is None:

            style = LOG_STYLE.DM_COMMAND_MSG

        else:

            style = LOG_STYLE.COMMAND_MSG



        return cls (

            style[0],
            style[1] + str(sending),

            ctx = ctx,
            root_log = True,

        )



    @classmethod
    def message_edit(cls, before_ctx, after_ctx):

        return cls (

            LOG_STYLE.MESSAGE_EDIT[0],
            LOG_STYLE.MESSAGE_EDIT[1],

            cls('before', *cls.message_info(before_ctx)),
            cls('after', *cls.message_info(after_ctx)),

            ctx = before_ctx,
            root_log = True,

        )



    @classmethod
    def message_delete(cls, ctx):

        return cls (

            LOG_STYLE.MESSAGE_DELETE[0],
            LOG_STYLE.MESSAGE_DELETE[1],

            *cls.message_info(ctx),

            ctx = ctx,
            root_log = True,

        )



    @classmethod
    def member_join(cls, member):

        return cls (

            LOG_STYLE.MEMBER_JOIN[0],
            LOG_STYLE.MEMBER_JOIN[1],

            member = member,
            root_log = True,

        )




    @classmethod
    def awoken(cls):

        return cls (

            LOG_STYLE.AWOKEN[0],
            LOG_STYLE.AWOKEN[1],

            root_log = True,

        )



    @classmethod
    def asleep(cls):

        return cls (

            LOG_STYLE.ASLEEP[0],
            LOG_STYLE.ASLEEP[1],

            root_log = True,

        )







    @classmethod
    def uncaught_exception_info(cls, exc):

        return (

            cls (exc.__class__.__name__ + ':', str(exc)),

        )




    @classmethod
    def uncaught_exception(cls, exc):

        return cls (

            LOG_STYLE.UNCAUGHT_EXCEPTION[0],
            LOG_STYLE.UNCAUGHT_EXCEPTION[1],

            *cls.uncaught_exception_info(exc),

            root_log = True,

        )



    @classmethod
    def fatal_uncaught_exception(cls, exc):

        return cls (

            LOG_STYLE.FATAL_UNCAUGHT_EXCEPTION[0],
            LOG_STYLE.FATAL_UNCAUGHT_EXCEPTION[1],

            *cls.uncaught_exception_info(exc),

            root_log = True,

        )













def basic_log_method(log_type):

    def rt(self, *args, **kwargs):

        self._add_log(log_type(*args, **kwargs))

    return rt


















BUFFER_SIZE = 7


class Logs:



    def __init__(self):

        self. log_file = Path(PATH) / 'logging' / f'{date.today()}.logs'
        self. log_file.assure()

        self._buffer = list()



    def _add_log(self, log):

        self._buffer.append(log)

        self.log_file.append(str(log) + LOG_STYLE.LOG_SEPARATION)

        if len(self._buffer) > BUFFER_SIZE:
            self._buffer.pop(0)



    def __str__(self):

        return LOG_STYLE.LOG_SEPARATION.join(formatting.codeblock('python\n' + str(log)) for log in self._buffer)



    def __iter__(self):

        yield from self._buffer[::-1]





    log_message = basic_log_method(Log.message)

    log_sent_message = basic_log_method(Log.sent_message)

    log_invoke = basic_log_method(Log.invoke)

    log_detected_function_call = basic_log_method(Log.detected_function_call)

    log_forbidden = basic_log_method(Log.forbidden)

    command_log = basic_log_method(Log.command_log)

    log_message_edit = basic_log_method(Log.message_edit)

    log_message_delete = basic_log_method(Log.message_delete)

    log_member_join = basic_log_method(Log.member_join)

    log_awoken = basic_log_method(Log.awoken)

    log_ready = log_awoken

    log_asleep = basic_log_method(Log.asleep)

    log_uncaught_exception = basic_log_method(Log.uncaught_exception)

    log_fatal_uncaught_exception = basic_log_method(Log.fatal_uncaught_exception)



    log = basic_log_method(Log)



















































#
