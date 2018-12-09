import furthersubcomponents as fur
import constants
client = None
rd = lambda num: randint(0, num - 1)
def randomitem(subscriptable):
    return subscriptable[rd(len(subscriptable))]
def utfopen(*args, **args):
    return open(*args, encoding = "UTF-8", **args)
def quickread(filepath):
    with _utfopen(filepath) as file:
        return file.read()
def quickwrite(filepath, writing):
    with _utfopen(filepath, "w") as file:
        return file.write(writing)
def message(*args, **kwargs):
    client.send_message(*args, **kwargs)
async def log(commandname, type, server = None, channel = None):
    servermsg = "at {}".format(server), "somewhere at {}".format(server), "somewhere???"
    channelmsg = "'s {}".format(channel), "", ""
    typemsg = "succeeded", "went invalid", "failed", "triggered {}"
    index0 = (server and channel, server, True).index(True)
    index1 = (type == "SUCCESS", type == "INVALID", type == "FAIL", True).index(True)
    _quickwrite(constants.logFile, "<<{} {} {}{}>>\n".format(commandname, typemsg[index2], servermsg[index], channelmsg[index]))
async def replylog(user, word):
    usermsg = "", "", "recognized {}", "recognized {}"
    midmsg = "defaulty replied to someone", "defaultly replied to someone","but still talked to them like they were just some stranger" , "and replied to them"
    wordmsg = "", "recognizing the word \"{}\"", "", "recognizing the word \"{}\""
    index = (user == "DEFAULT" and word == "DEFAULT", user == "DEFAULT", word == "DEFAULT", True)
    _quickwrite(constants.logFile, "話{} {} {}話\n".format(usermsg[index], midmsg[index], wordmsg[index]))
