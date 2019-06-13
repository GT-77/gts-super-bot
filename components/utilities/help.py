'''
this is the ugliest module

it's dedicated to handling the ugly stuff of the help command
and wrappting it all up in a function called initialize_help(command)
'''


from discord.ext.commands import is_owner, has_permissions, guild_only, is_nsfw, has_role

from .formatting import formatting

from .functions import takewhile



class Help:


    def __init__(self, command, **options):

        for key, value in {

            'usage_section': f':seven::exclamation:{command.qualified_name} {command.signature}',
            'aliases_section': 'aliases: ' + ', '.join(command.aliases) if command.aliases else None,
            'brief': 'ur gay',
            'restrictions_section': '\n'.join(f'・{restriction}' for restriction in options['restrictions']) if 'restrictions' in options else None,
            'help_section': command.help if command.help else 'basically i have no fucking clue about this command but apparently i have it',

            # the most fuckfest line of code in the entire bot
            'example_section': None if 'examples' not in options else 'here r some example(s)\n\n' + '\n\n'.join(f'u do {formatting.bold_code(f"7!{command.qualified_name} {use}")} {result}' for use, result in options['examples'].items())

        }.items():

            options.setdefault(key, value)


        if options.get('group') and command.commands:

            options.setdefault( 'subcommands_section', formatting.bold('subcommands of this command:\n\n') + '\n'.join(formatting.code('7!' + command.qualified_name) + ' (u can do ' + formatting.code(f'7!help {command.qualified_name}') + ')' for command in command.commands) )

        else:

            options.setdefault( 'subcommands_section', '' )



        self.parsed = list(filter(

            bool,

            [

                formatting.bold_italics(options['usage_section']),
                formatting.italics(options['aliases_section']),
                formatting.bold_underline(options['brief']),
                formatting.italics(options['restrictions_section']),
                formatting.codeblock(options['help_section']),
                options['example_section'],
                options['subcommands_section'],

            ]


        ))





        options.setdefault ( 'full_help', '\n\n'.join(self.parsed) )

        self.__dict__.update(options)



    def __str__(self):

        return self.full_help



    def __len__(self):

        return len(self.full_help)












def initialize_help(command, **extra_options):
    'initializes ur needed help into the command (given command must have an options attribute set with the kwargs of the command decorator)'

    command.help_object = command.help_obj = Help(command, **command.options, **extra_options)
