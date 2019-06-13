"""
module dedicated to defining all commands on a GTS instance

run.py will import the instance, bring everything together and make some last touches
before making the bot jump into action
"""



from asyncio import sleep

from datetime import datetime

from random import choice, randrange

from types import SimpleNamespace

from typing import Optional, Union




from discord import (
    Member, TextChannel, Role, User,
    Colour, Emoji,

    File,
)

from discord.ext.commands import (
    Greedy,
    is_owner, is_nsfw, guild_only, has_role, has_permissions,
    cooldown, check,
    Converter,
    BadArgument, CheckFailure, CommandNotFound,
)



from .structure import GTS, type_n_send, global_database, global_db, gdb

from .utilities import (
    formatting,
    initialize_help,
    one_in, randrange, exponential_randrange as exp_rr,
    indent, limit,
    ID_OF,
)



gts = GTS("7!", case_insensitive = True)
gts.remove_command("help") # there is no help, motherfucker








class CommandConverter(Converter):
    async def convert(self, ctx, argument):
        command = gts.get_command(argument)
        if command is None:
            raise BadArgument(argument)
        return command







def only_accept_id(*ids):

    def rt(ctx):

        return ctx.author.id in ids

    return check(rt)








r_txt = restriction_texts = SimpleNamespace (

    is_owner = "u must be dad to use this command so basically forget anything",
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
async def help_(ctx, *, command:CommandConverter = None):
    """
    u can do 7!help on any command 2 get help on it

    anythin not provided by 7!help is learned thru immersion
    """

    if command is None:
        command = help_

    ctx.rt = command.help_obj









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

    if u don't want the scan to be overwritten into the same file, u can set the save file name
    but rly the only file i give a shit about when reroling is the one called "recent"
    so yeah the only way to recover the contents of the old save file is to ask dad for it
    """

    storage = global_database.servers[ctx.guild.id].scans

    if save_file in storage:
        del storage[save_file]

    storage = storage[save_file]

    for member in ctx.guild.members:

        member_roles = storage[member.id]

        ctx.log('scanin', member, member.id, '...')

        for role in member.roles:

            member_roles << role.id




























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
    at the time of scanning. otherwise the command won't do shit

    exceptionally useful for members that left and joined back roleless
    """

    storage = global_database.servers[member.guild.id].scans.recent

    if member.id in storage:
        await member.edit(reason = "4 my homies", roles = filter(bool, map(ctx.guild.get_role, storage[member.id])))




















































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
    spacing = ' ',

    *,
    custom_transition = None
):



    """
    that's pretty much it
    (here's the transitions i mean btw: https://www.youtube.com/watch?v=L2Rc6ie8_TQ)



    jk

    if u're looking at this help message rn u probably saw all those optional parameters
    like "custom_transition" and "speed" and shit
    and thought to urself "wtf holy shit lma ;o can i fuck with this"
    the answer is yes, u can
    this command is not as inoccent as it be seemin

    "length" represents the amount of placeholder dots present.
    if there's more dots than the length of the transition then some dots will remain forever unreplaced xyz

    "speed" is the speed at which the dots get replaced. the default speed of 1 is precisely 2 dots per second

    "dot_style" is the look of each placeholder dot (which is obv ・ in bold by default). u can change dat to anytin

    "spacing" is the spacing between each dot. default is nothing


    last but neva least is "custom_transition". dis is a parameter that eats up the rest of ur command so u can set it to whatev u want
    witout worrying bout quotes n shit. im lazy to explain so find out urself wat that is bout
    """



    if custom_transition is None:

        if "transitions" in ctx.database:
            transition_full_text_choice = (+ctx.database.transitions).split()
        else:
            raise Exception("wtf where my MKDM transitions") # bail out. this is not supposed to happen

    else:
        transition_full_text_choice = custom_transition.split()



    ctx.log('transition:', transition_full_text_choice)



    transition_array = [dot_style] * length

    def array_to_text():
        return formatting.bold(spacing.join(transition_array))

    transition_msg = await ctx.send(array_to_text())

    delay = 0.5 / speed

    for index in range(length):

        if transition_full_text_choice:

            transition_array[index] = transition_full_text_choice.pop(0)

            await sleep(delay)
            await transition_msg.edit(content = array_to_text())

        else:
            break


























































@gts.command (
    brief = 'xyz',
    restrictions = [
        'xyz',
    ],
    examples = {
        '': 'xyz',
    },
    feedback = False,
)
# @cooldown (1, 7.7)
async def xyz(ctx, xyz = 'xyz'):
    'xyz'



    if not ctx.db.xyz:
        raise Exception('xyz')


    #abc txt  |abc img path| abc file obj
    highguard = lil_marco = love_xyz = None



    df_xyz = ctx.db.xyz

    df_xyz_img = df_xyz.xyz
    df_xyz_txt = df_xyz.matthias_bider



    abc = ctx.db[xyz]

    kka = abc.xyz

    _321 = abc.matthias_bider








    def get_xyz_att():

        path = +df_xyz_img

        return File(path, filename = no_filename_to_filename(path.suffix))








    def get_abc_att():

        if kka:

            path = +kka

            return File(path, filename = no_filename_to_filename(path.suffix))









































    def high_to_cyni():

        highguard_l = list(highguard)

        highguard_l.sort()

        max_high = highguard_l[-randrange(min(len(highguard_l), 7)) - 1]



        def insertion():

            for i in range(1, randrange(len(highguard_l))):
                foundation[randrange(len(foundation)):0] = choice(highguard_l).split(' ')
                if len(foundation) > 99:
                    break


        if len(max_high) >= randrange(42, 47) and len(highguard_l) > randrange(0, 7):

            foundation = max_high.split(' ')
            highguard_l.remove(max_high)

            insertion()

        elif len(highguard_l) > randrange(2, len(highguard_l) + 5):

            foundation_txt = choice(highguard_l)
            highguard_l.remove(foundation_txt)
            foundation = foundation_txt.split(' ')

            insertion()

        else:
            return choice(choice(highguard_l).split())

        return ' '.join(foundation)














    def no_filename_to_filename(suffix = None):

        if suffix is None:
            suffix = lil_marco.suffix

        if highguard:

            return choice(choice(list(highguard)).split()) + suffix

        return 'xyz' + suffix















    def lol_heres_a_member():

        if ctx.guild:
            return choice(ctx.guild.members)
        else:
            return ctx.message.author














    def gen_high_marco_lxyz():

        nonlocal highguard, lil_marco, love_xyz






        if kka:
            lil_marco = +kka # xyz
        else:
            lil_marco = None



        highguard = set()

        if _321:
            for i in range(randrange(1, 666)):
                ur_pace_is_leisurely = +_321
                if len(ur_pace_is_leisurely) < 1500:
                    highguard.add(ur_pace_is_leisurely)
        else:
            highguard = None



        if highguard is lil_marco:
            return xyz
            # xyz



        if lil_marco is None:
            love_xyz = None
        else:
            love_xyz = File(lil_marco, filename = no_filename_to_filename())






















































    async def xyz_slapback():
        await ctx.send(ctx.message.content)







    async def xyz_raw():
        await ctx.send(file = get_xyz_att())








    async def xyz_xyz():

        if gen_high_marco_lxyz() is not None:

            ctx.send('xyz')
            return


        if highguard is None:
            dreams_of_cyanide = None
        else:
            dreams_of_cyanide = high_to_cyni()



        return await ctx.send (dreams_of_cyanide, file = love_xyz)










    async def xyz_r_ping():

        await ctx.send(lol_heres_a_member().      mention)




    async def xyz_m_avatar():

        m = lol_heres_a_member()

        await ctx.send (f'{m.display_name}\'s avatar is {m.avatar_url}')






    async def xyz_r_avatar():

        await ctx.send (f'{lol_heres_a_member().display_name}\'s avatar is {lol_heres_a_member().avatar_url}')











    async def xyz_distortion():

        await ctx.send ('distortion')







    async def xyz_r_marco_message():

        if one_in(2):
            async for msg in ctx.channel.history(limit = 700):
                if msg.author.id == ID_OF.MARCO:
                    await ctx.send (msg.content)
                    return


        M_STR = "lö+p#.pö+üjuiolfdsfddsfä+ü#+ä+ä#+"

        r_start = randrange(len(M_STR) - 7)

        await ctx.send (M_STR[r_start: r_start + 7])







    async def xyz_raw_x2():

        db = ctx.db.xyz.xyz

        sd = +df_xyz_img, +df_xyz_img

        await ctx.send (files = [File(sd[0], f'xyz_raw_0_{sd[0].name}'), File(sd[1], f'xyz_raw_1_{sd[1].name}')])









    async def xyz_ultra_swap():

        msg = await xyz_xyz()

        if highguard is not None:

            await sleep(7)

            await msg.edit ( content = high_to_cyni() )







    async def xyz_r_msg():

        async for msg in ctx.channel.history(limit = randrange(5, 100)):
            pass

        await ctx.send (msg.content, file = get_abc_att())



    async def xyz_pure():

        sd = +df_xyz_txt

        if len(sd) > 2000:

            ctx.log('falling back to xyz_r_msg')

            await xyz_r_msg()

        else:

            await ctx.send ( sd )




























    # await vars()[choice([var for var in vars() if var.startswith('xyz_')])]() # dirt dirt DIRT :)

    chosen_xyz = choice([var for var in vars() if var.startswith('xyz_')])

    ctx.log(chosen_xyz)

    await vars()[chosen_xyz]()






























_dictionary_arranger = lambda rt: formatting.bold(rt[0]) + '\n\n\n' + f'\n\n{formatting.code("/" * 47)}\n\n'.join(rt[1])
_dictionary_necessary_attr = 'number', 'function', 'text', 'examples', 'author.name', 'creation.date'
_can_define = ID_OF.GT, ID_OF.CYNI


def _def_has_attr(ptr, attr):
    'checks if ptr has attr'

    if '.' in attr:

        attr = attr.split('.')

        for move in attr[:-1]:

            ptr = ptr[move]

        return attr[-1] in ptr



    return attr in ptr




def _valid_definition(ptr):
    'checks if it is possible to use the definition ptr points to'

    for attr in _dictionary_necessary_attr:
        if not _def_has_attr(ptr, attr):
            return False

    return True







@gts.group (

    aliases = ['dict'],

    brief = 'the ascended dictionary',

    restrictions = (
        'anyone can read definitions',
        'currently only gt and cyni can add definitions',
    ),

    examples = {

        'definiton xyz': 'and u get the definition of xyz',
        'define ascension 1 noun "a level of humor beyond the understanding of the mortal" "gt\'s discord server is the heartbeat of ascension" "ascension started vaguely around 2016 - 2017"': 'and u just added a noun definition to ascension at position 1',

    },

)

async def dictionary(ctx, word = None) -> _dictionary_arranger:
    '''

    this command is an interface for the ascended dictionary
    the ascended dictionary contains / will contain definitions for most ascended terms
    currently being written by the two seeds of ascension themselves: gt and cyni (but i'm sure more ascended niggas will be allowed soon)

    if u give me the 7!dictionary (7!dict) command by itself i will assume u mean 7!dictionary definition (7!dict def)
    if ur interested in reading from the dictionary check out "7!help dict definition"

    if ur interested in contributing to the dictionary first ask gt for permission and he might say no but still it was worth a try i support u xyz
    if u received permission check out "7!help dict define" on how to add definitions to words. it's ez

    note: a third subcommand "7!dict image" which adds attachments to words might be added in the future sometime

    '''

    await definition.callback(ctx, word)












@dictionary.command (

    aliases = ['def'],

    brief = 'gives u definitions of a word from the ascended dictionary',

    examples = {

        'ascension': 'and u get definitions of the term ascension itself',
        '': 'and u get definitions of a random word from the dictionary',
        'distortion': '',

    }

)

async def definition(ctx, word = None, index:int = 1) -> _dictionary_arranger:

    '''

    usage is kind of self explainatory
    u give it as a parameter the word u desire definition(s) for

    if no word is given it'll give u a random word from the dictionary

    '''

    # rt will be a tuple with the word, and the generator of definition texts

    if word is None:

        if ctx.database.words:
            word = +ctx.database.words
        else:
            raise BadArgument













    word = word.lower()










    def example_parser(ex):

        if '\n' in ex:

            ex = indent('\n' + ex)

        return ex



    def definition_str(ptr):
        'if the the definition ptr points to is valid, this function returns its string'


        return '\n'.join (

            [

                # wtf
                indent ( str(ptr.number) + '. ' + formatting.italics(ptr.function) ),

                '',

                indent ( +ptr.text , amount = 2 ),

                '',

                indent ( 'ex: ' + example_parser(formatting.italics(+ptr.examples)), amount = 2 ),

                '',

                indent ( formatting.italics ( 'written by ' + formatting.bold(ptr.author.name) + ' on ' + ptr.creation.date ) ),

            ]

        )



    def return_definitions(definitions):

        ctx.rt = word, map(definition_str, definitions)














    MAX_SHOW = 3








    storage = ctx.database.words[word].definitions

    definitions = [storage[definition] for definition in set(storage) if _valid_definition(storage[definition])]

    definitions.sort(key = lambda ptr: int(ptr.number))








    if not definitions:

        raise BadArgument







    if len(definitions) <= MAX_SHOW:

        return_definitions(definitions)
        return


    selection = exp_rr(len(definitions) - MAX_SHOW + 1)



    return_definitions(definitions[selection: selection + MAX_SHOW])






























@dictionary.command (

    aliases = ['add'],

    brief = 'adds a word definition to the ascended dictionary',

    restrictions = (
        'currently only gt and cyni can do dis',
    ),

    examples = {

        '''some_word 2 verb "dis word means ur ass
u move dat ass
ur highguard's furry persona" "mark: u suck!
jim: some_word !
mark: oh shit" "i will some_word u!"''': 'and u just added a new definition for some_word',

    },

)

@only_accept_id(*_can_define)

async def define(ctx, word, number:int, grammatical_function, definition_text, *examples):

    '''

    adding a definition is extremely ez, u just have to fill out all parameters

    let's walk thru each parameter

    word - obvious one. the word to which u want to add the definition to

    number - must be an integer number bigger than 0
    the rank / slot of the definition
    if the word already has a definition written on the slot u've given (the slot is taken)
    and the definition written there is not written by u, then i will reject u

    grammatical_function - must be one of the following: "noun", "verb", "adjective", "expression". if not then i will refuse 2 take ur definition into consideration
    this is what role the word has gramatically, in the definition u gave. u must be above the age of -2 to understand dis

    definition_text - the body of the definition
    u should almost always surround this in quotes. please for the love of god n jesus surround it in quotes
    ur definition text can span multiple lines. (for idiots: use enter + shift to add new space witout sending ur message)
    like dis:
    7!dict define some_word 3 noun "dis is my definition text
    and dis is the second line
    and dis is the third line" "and dis is my first example" "and dis is my second example"

    examples - u can add as many examples as u want
    and they can also span multiple lines
    if u don't have atleast 1 example i will reject u

    if u add 2 ur own definiton then the definition text 2 b displayed is random, same wit examples

    IMPORTANT: u can't delete definitons, so try 2 not make mistakes
    if u rly want ur definiton 2 b removed u can prolly ask gt 2 do it manually

    '''

    creation_datetime = datetime.now()
    creation_date = creation_datetime.date()
    creation_time = creation_datetime.time()



    if grammatical_function in ('adj', 'adjective'):

        grammatical_function = 'adj.'

    elif grammatical_function in ('expr', 'expression'):

        grammatical_function = 'expr.'



    if (

        ' ' in word or '\n' in word

        or

        number < 1

        or

        grammatical_function not in ('noun', 'verb', 'adj.', 'expr.')

    ):

        raise BadArgument



    storage = ctx.database.words[word].definitions[number]

    if not storage: # if this is a new definition

        storage.number = number
        storage.function = grammatical_function

        storage.author.name = ctx.author.display_name # there u go
        storage.author.id = ctx.author.id
        storage.author.tag = ctx.author.name + '#' + ctx.author.discriminator # storing this is optional. it's just for possible contact purposes

        storage.creation.date = str(creation_date)
        storage.creation.time = str(creation_time)

    elif ctx.author.id != int(storage.author.id):

        raise CheckFailure



    storage.edits << str(creation_datetime)



    storage.text << definition_text

    for example in examples:

        storage.examples << example













@dictionary.command (

    brief = 'shows u random words with atleast 1 definition in the ascended dictionary',

)

async def words(ctx, display:int = 13) -> lambda rt: ', '.join(map(formatting.bold_code, rt[0])) + ' ' + rt[1]:
    '''
    by default shows 13 random words, but u can set dat 2 whatever u desire between 0 and 77
    (i'm talkin bout the display parameter)
    and yeah if u set the display parameter to 0 then i'll tell u how many words there r in the dictionary


    if what u set dat 2 is a bigger or equal number the total words in the dictionary then it'll just show u all

    but the dict won't stay dat short 4 long
    '''

    # returns a tuple with a word set and the appended message

    if not ctx.database.words:
        raise Exception('no words 2 choose from')

    if not (0 <= display <= 77):
        raise BadArgument



    def check_word(ptr):
        'checks if the word ptr points to inside the database is valid'

        definitions = ptr.definitions

        for definition in set(definitions):
            if _valid_definition(definitions[definition]):
                return True

        return False



    words = ctx.database.words

    def _words_gen():
        'returns a generator wit all words wit atleast 1 valid definition'

        for word in (+words for i in range(display)):
            if check_word(words[word]):
                yield word



    def message():

        if not display:
            return f'there are currently {len(words)} words in the ascended dictionary'

        other_words = len(words) - display

        if other_words > 0:

            if other_words == 1:

                return 'are all dictionary words and dere is 1 word missin'

            return f'... and {other_words} more words in da dictionary'

        return 'n dese r all wordz'



    ctx.rt = set(_words_gen()), message()

















initialize_help(dictionary, group = True)
# # # # # # # DICT END # # # # # # # # # # # # # # # # # # # # #










































# @gts.group (
#
#     aliases = ['func'],
#
#     breif = 'base command for function usage',
#
#     examples = {
#
#         'add xyz_emj 7!koba 5 1 ・ " " :slight_frown: :neutral_face: :slight_smile: :smile: :smiley:': 'and u created the new function `xyz_emj` 4 urself',
#
#         'call xyz_emj': 'and u called ur function',
#
#         'add slow_mo_koba 7!kobayashi 5 0.5 ・ " "': 'and u added another function to which u can have parameters',
#
#         'call slow_mo_koba ur face looks very stupid': 'and dat will b equivalent 2 `7!kobayashi 5 0.5 ・ " " ur face looks very stupid`',
#
#         'add slow_mo_apples F7!slow_mo_koba :apple: :apple: :apple: :apple: :apple:': 'and u made a perfectly valid function out of another function',
#
#     },
#
#     feedback = True,
#
# )
#
# async def function(ctx, func, *, args = ''):
#
#     '''
#     functions r just shortcuts to command calls, so u don't have 2 repeat urself
#
#     u add a function wit "7!func add <name of ur function> [command it is equivalent to]"
#     and u call it wit "7!func call <name of ur function> [extra arguments]"
#
#     if u do "7!func <name of ur func> [extra arguments]" i'll just assume u mean "7!func call (...)"
#
#     if u call a function that u haven't declared i just won't do shit, and won't even say shit. i'll ignore u
#
#     important: u can shortcut "7!function call ur_function [args]" to just "7F!ur_function [args]" or "F7!ur_function [args]"
#
#     more important: as of now the command you set to a function cannot span multiple lines. so don't do dat
#     '''
#
#     gts.logs.log('entering function code...')
#
#     await func_call.callback(ctx, func, args = args)
#
#
#
#
#
#
#
#
#
#
#
#
#
# @function.command (
#
#     name = 'call',
#
#     brief = 'calls a function',
#
#     examples = {
#
#         'ass': 'and u called the function `ass`',
#
#     },
#
#     feedback = True,
#
# )
#
# async def func_call(ctx, func, *, args = ''):
#
#     '''
#     "7!function call func" can be shortcuted to "7F!func" or "F7!func"
#     same thing with args and shit blah blah blah
#     '''
#
#     storage = ctx.database.users[ctx.author.id].functions
#
#     gts.logs.log('we\'re inside func_call...')
#     ctx.log('loggin again...')
#
#     if func in storage:
#
#         ev = storage[func] + ' ' + args
#
#         ctx.log('evaluated to', ev)
#
#         await gts.evaluate(ev, location = ctx)
#
#
#
#
#
#
#
#
# @function.command (
#
#     name = 'add',
#
#     brief = 'adds a function for u',
#
#     restrictions = ('', '・', '・・'),
#
# )
#
# async def func_add(ctx, func, *, command):
#
#     '''
#     distortion
#     '''
#
#     ctx.database.users[ctx.author.id].functions[func] = command
#
#
#
#
#
#
#
#
# @function.command (
#
#     name = 'all',
#
#     aliases = ['functions', 'funcs', 'my_functions', 'my_funcs', 'all_functions', 'all_funcs'],
#
#     feedback = False,
#
# )
#
# async def func_all(ctx) -> lambda rt: rt[0] + '\n\n' + '\n'.join(formatting.bold_code(func[0]) + ' = ' + formatting.code(func[1]) for func in rt[1] ):
#
#     '''
#     shows u all your functions and their respective commands, or atleast the ones that fit
#     '''
#
#     storage = ctx.database.users[ctx.author.id].functions
#
#     ctx.rt = formatting.bold(ctx.author.display_name) + '\'s functions:', ((func_name, storage[func_name]) for func_name in storage)
#
#
#
#
#
#
#
#
#
#
# initialize_help(function, group = True)
# # # # # # # # FUNC END # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

























@gts.command (

    aliases = ['all_commands', 'allcommands'],

    brief = 'shows u all my commands',

)

async def commands(ctx) -> lambda itr: ' '.join(map(formatting.bold_code, itr)):

    '''

    nuttin more 2 really say

    '''

    ctx.rt = (command.name for command in gts.commands if not command.name.startswith('_'))






















@gts.command (

    aliases = ['kys', 'kill_yourself', 'die', 'kill_urself', 'shut_down'],

    brief = 'makes me go 2 sleep',

    restrictions = (r_txt.is_owner, 'i don\'t listen 2 strangers on the internet, but i know that if it is gt he\'s doin sometin')

)

async def shutdown(ctx):
    '''
    zzz
    '''

    await gts.close()













@gts.command (

    aliases = ['ver'],

    brief = 'shows u my version',

    feedback = False,

)

async def version(ctx):

    '''
    i'm currently under testin
    '''

    ctx.rt = '`2.0.0` (expect to find glitches and b ready 2 report)'






























@gts.command (

    aliases = ['send_message', 'sendmessage', 'send_msg', 'sendmsg', 'msg'],

    restrictions = ['no'],

)

@is_owner()

async def _send_message(ctx, location:Union[TextChannel, User], *, content):

    if 'sends' in ctx.database:

        sends = int(ctx.database.sends)

    else:

        sends = ctx.database.sends = 0



    for attachment in ctx.message.attachments:

        await (ctx.database.attachments[sends] << attachment)



    await location.send(content, files = [File(path) for path in ctx.database.attachments[sends]])

    if ctx.message.attachments:
        
        ctx.database.sends = sends + 1





















#
