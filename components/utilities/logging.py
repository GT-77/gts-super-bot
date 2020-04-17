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

    DM_COMMAND_LOG = ('<(C)>', 'received log from {ctx.command.qualified_name}) invoked in {ctx.author.display_name}\'s wet #cker candy sugar ({ctx.author.id})'),
    COMMAND_LOG = ('<C>', 'received log from {ctx.command.qualified_name} invoked in {ctx.channel.name} ({ctx.channel.id})'),

    MEMBER_JOIN = ('/MJ/', '{member.display_name} ({member.id}) has joined {member.guild.name} ({member.guild.id})'),

    MESSAGE_EDIT = ('[*MSG]', '{ctx.author.display_name} ({ctx.author.id}) has edited their message'),

    MESSAGE_DELETE = ('[X]MSG]', '{ctx.author.display_name}\'s ({ctx.author.id}) message got deleted'),



    AWOKEN = ('/A\\', 'i have woken up. お久しぶり'),

    ASLEEP = ('\\V/', 'i\'m goin 2 sleep. お休み'),



    SEP = ' ',
    # INDENT = '    ',
    LOG_SEPARATION = '\n\n\n\n\n',
    SUBLOG_SEPARATION = '\n\n',
    BRANCHING_MARKER = ':',
    TIME_SEP = '\n',
)



class DataAttribute:

    def __init__(self, name, value):
        self.string = f'{name}: {value}'

    def  __str__(self):
        return self.string

    @classmethod
    def get_attributes(cls, obj, *attributes):

        return (
            cls(attribute.replace('_', ' '), obj.__getattribute__(attribute))
            for attribute in attributes
        )

    @classmethod
    def uncaught_exception_info(cls, exc):
        return cls(exc.__class__.__name__, exc)






class Sublog:

    def __init__(self, header, *sublogs, **variables):
        self.header = header
        self.sublogs = sublogs
        self.vars = variables



    def __str__(self):
        # print(self.header.header, self.header.sublogs, self.header.vars)
        header = self.header.format(**self.vars)
        branches = LOG_STYLE.SUBLOG_SEPARATION.join(map(indent, self.sublogs))

        if branches:
            header += LOG_STYLE.BRANCHING_MARKER + LOG_STYLE.SUBLOG_SEPARATION

        return header + branches



    @classmethod
    def get_list_attribute(cls, obj, attribute, attr_to_Sublog):
        return cls ( attribute, *map(attr_to_Sublog, obj.__getattribute__(attribute)))



    @classmethod
    def message_info(cls, ctx):

        return (
            *DataAttribute.get_attributes ( ctx.message,
                'content',
                'id',
                'created_at',
                'edited_at',
                'jump_url',
            ),

            cls.get_list_attribute ( ctx.message, 'attachments',
                lambda attachment:
                    cls (
                        attachment.filename,
                        *DataAttribute.get_attributes(attachment, 'url', 'proxy_url')
                    )
            )
        )



    @classmethod
    def member_info(cls, member):

        return DataAttribute.get_attributes ( member,
            'joined_at',
            'status',
            'avatar_url',
        )






class Log(Sublog):

    def __init__(self, tag, header, *sublogs, **variables):
        super().__init__(tag + LOG_STYLE.SEP + header, *sublogs, **variables)

    def __str__(self):
        return str(datetime.now()) + LOG_STYLE.TIME_SEP + super().__str__()



def tag_and_header(log_style):
    selection = LOG_STYLE.__getattribute__(log_style)
    return selection[0], selection[1]

# FATAL UNCAUGHT EXCEPTION will be missing

class _BasicLog(Log):
    def __init__(self, STYLE, *sublogs, **variables):
        super().__init__(*tag_and_header(STYLE), *sublogs, **variables)

class _BasicCtxLog(_BasicLog):
    def __init__(self, STYLE, ctx):
        super().__init__(STYLE, ctx = ctx)

class _BasicMessageLog(_BasicLog):
    def __init__(self, STYLE, ctx):
        super().__init__(STYLE, *Sublog.message_info(ctx), ctx = ctx)


class AwokenLog(_BasicLog):
    def __init__(self):
        super().__init__('AWOKEN')

class MemberJoinLog(_BasicLog):
    def __init__(self, member):
        super().__init__('MEMBER_JOIN', member = member, *Sublog.member_info(member))

class UncaughtExceptionLog(_BasicLog):
    def __init__(self, exc):
        super().__init__('UNCAUGHT_EXCEPTION', DataAttribute.uncaught_exception_info(exc))

class MessageEditLog(_BasicLog):
    def __init__(self, before_ctx, after_ctx):
        super().__init__ (
            'MESSAGE_EDIT',
            Sublog('before', *Sublog.message_info(before_ctx)),
            Sublog('after', *Sublog.message_info(after_ctx)),
            ctx = before_ctx,
        )

class CommandLog(_BasicCtxLog):
    def __init__(self, ctx, sending):
        super().__init__('DM_COMMAND_LOG' if ctx.guild is None else 'COMMAND_LOG', ctx, sending)



def _basic_message_log_class(STYLE):
    class rt(_BasicMessageLog):
        def __init__(self, ctx):
            super().__init__(STYLE, ctx)
    return rt

def _basic_log_class(STYLE):
    class rt(_BasicCtxLog):
        def __init__(self, ctx):
            super().__init__(STYLE, ctx)
    return rt

# DM = direct message
# IM = indirect message (sent thru server)

_NewIMLog = _basic_message_log_class('MESSAGE')

_NewDMLog = _basic_message_log_class('DM')

_SentIMLog = _basic_message_log_class('SENT_MESSAGE')

_SentDMLog = _basic_message_log_class('SENT_DM')

MessageDeleteLog = _basic_message_log_class('MESSAGE_DELETE')

ForbiddenLog = _basic_log_class('FORBIDDEN')

ReadyLog = AwokenLog

AsleepLog = _basic_log_class('ASLEEP')

DetectedFunctionCallLog = _basic_log_class('DETECTED_FUNCTION_CALL')

_UnknownCommandDMInvoke = _basic_log_class('UNKNOWN_COMMAND_DM_INVOKE')

_UnknownCommandIMInvoke = _basic_log_class('UNKNOWN_COMMAND_INVOKE')

_KnownCommandDMInvoke = _basic_log_class('DM_INVOKE')

_KnownCommandIMInvoke = _basic_log_class('INVOKE')



def NewMessageLog(ctx):
    if ctx.guild is None:
        return _NewDMLog(ctx)
    return _NewIMLog(ctx)

def SentMessageLog(ctx):
    if ctx.guild is None:
        return _SentDMLog(ctx)
    return _SentIMLog(ctx)

def InvokeLog(ctx):
    if ctx.command is ctx.guild is None:
        return _UnknownCommandDMInvoke(ctx)
    if ctx.command is None:
        return _UnknownCommandIMInvoke(ctx)
    if ctx.guild is None:
        return _KnownCommandDMInvoke(ctx)
    return _KnownCommandIMInvoke(ctx)






def logging_function(log_cls):

    def rt(self, *args, **kwargs):
        return self.write(log_cls(*args, **kwargs))

    return rt



BUFFER_SIZE = 7

class Logs:

    def __init__(self, log_file):
        self.log_file = log_file # Path(PATH) / 'logging' / f'{date.today()}.logs'
        self.log_file.assure()
        self.buffer = list()

    def write(self, obj):

        self.buffer.append(obj)
        self.log_file.append(str(obj) + LOG_STYLE.LOG_SEPARATION)

        if len(self.buffer) > BUFFER_SIZE:
            self.buffer.pop(0)

    def __str__(self):
        return LOG_STYLE.LOG_SEPARATION.join(formatting.codeblock('python\n' + str(log)) for log in self._buffer)

    def __iter__(self):
        yield from self.buffer[::-1]



    command_log = logging_function(CommandLog)
    invoke_log = logging_function(InvokeLog)
    log = logging_function(str)
    member_join_log = logging_function(MemberJoinLog)
    uncaught_exception_log = logging_function(UncaughtExceptionLog)
    message_edit_log = logging_function(MessageEditLog)
    message_delete_log = logging_function(MessageDeleteLog)
    awoken_log = logging_function(AwokenLog)
    ready_log = logging_function(ReadyLog)
    new_message_log = logging_function(NewMessageLog)
    sent_message_log = logging_function(SentMessageLog)























































#
