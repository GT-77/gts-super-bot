import furthersubcomponents as fur
client = None
commands = dict()
def command(name, *parameters):
    for index in range(len(parameters)):
        if not isinstance(parameters[index], tuple):
            parameters[index] = (parameters[index], bool)
    async def functionality(message, *params):
        try:
            try:
                assert len(params) == len(parameters)
                for parameter in parameters:
                    assert parameter[1](parameter[0])
            except AssertionError:
                fur.feedback(name, "INVALID")
                return
            core(message, *params)
        except Exception as ex:
            fur.feedback(name, "FAIL")
            return
            fur.feedback(name, "SUCCESS")
    if core.__doc__:
        functionality.__doc__ = "**{}{}{}```{}```**".format(fur.constants.prefixBIG, name, str(parameters), core.__doc__)
    commands.update({name: functionality})
