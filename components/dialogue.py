import utilities as u
def _replysituation(situation):
    # returns a dictionary with its keys being all txt file names in dialogue/'situation' without the .txt
    # and its values being tuples
    # with their first values being the replies contained in that txt file
    # excluding the first line, which will contain a + or something else
    # if it contains a plus, the replies will include those of DEFAULT.txt
    returning = dict()
    returning["DEFAULT"] = u.quickread("dialogue/command/{}/{}".format(situation, "DEFAULT.txt"))[2:].split("\n") # setting this one separately to avoid key errors (it's not guaranteed that the loop will start with "DEFAULT.txt")
    for commandname in u.filesindir("dialogue/command/{}".format(situation)):
        content = u.quickread("dialogue/command/{}/{}".format(situation, commandname))
        returning[commandname[:-4]] = content[2:].split("\n") + (content["DEFAULT"] if content[0] == "+" else [])
    return returning
commandreplies = dict( # dictionary containing all possible situations of a command
    success = _replysituation("success"),
    fail = _replysituation("fail"),
    invalid = _replysituation("invalid"),
)
def commandreply(commandname, situation):
    # returns a string of a reply sir gts can give when the command with the name 'commandname' has succeeded
    if commandname in commandreplies[situation]:
        return u.randomelement(commandreplies[situation][commandname])
    else:
        return u.randomelement(commandreplies[situation]["DEFAULT"])
