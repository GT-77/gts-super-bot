'''
this is the ugliest module

it's dedicated to handling the ugly stuff of the help command
and wrappting it all up in a function called initialize_help(command)
'''


from discord.ext.commands import is_owner, has_permissions, guild_only, is_nsfw, has_role

from .formatting import formatting



def initialize_help(command):
    'initializes ur needed help into the command (given command must have an options attribute set with the kwargs of the command decorator)'

    op = command.options.copy()

    for key, value in {
        'usage': f':seven::exclamation:{command.name} {command.signature}',
        'brief': 'ur gay',
        'restrictions_section': '\n'.join(f'・{restriction}' for restriction in op['restrictions']) if 'restrictions' in op else '',
        'help_section': command.help if command.help else 'basically i have no fucking clue about this command but apparently i have it',

        # the most fuckfest line of code in the entire bot
        'example_section': '' if 'examples' not in op else 'here r some example(s)\n\n' + '\n\n'.join(f'u do {formatting.bold_code(f"7!{command.name} {use}")} {result}' for use, result in op['examples'].items())
    }.items():
        op.setdefault(key, value)

    op.setdefault (
        'full_help',
        '\n\n'.join ( [
            formatting.bold_italics(op['usage']),
            formatting.bold_underline(op['brief']),
            formatting.italics(op['restrictions_section']),
            formatting.codeblock(op['help_section']),
            op['example_section'],
        ] )
    )

    command.__dict__.update(full_help = op['full_help'])
