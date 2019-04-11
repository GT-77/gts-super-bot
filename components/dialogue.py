import utilities as u
def _adddict(dict0, dict1):
    # adds dictionary dict1 into dict0
    for key in dict1:
        if key not in dict0:
            dict0[key] = dict1[key]
        else:
            dict0[key] += dict1[key]
def _understoodword(string, dictionary):
    # determines whether gts super bot  has any clue what one word in that 'string' means, and returns replies of that dictionary according to the word
    # if gts is completely clueless about what he is seeing, this function returns replies to '"DEFAULT"'
    # in gts language, '"DEFAULT"' means "i don't fucking know"
    for line in string.split("\n"):
        for word in line.split(" "):
            word = word.lower()
            if word in dictionary:
                return dictionary[word]
    return dictionary["DEFAULT"]
# get ready for the biggest inception of functions ever
def _stringtoreplies(string, default):
    # turns given 'string' (what you see in dialogue.txt files) into a list of replies to actually use, relative to given 'default'
    # the format of what you see in dialogue.txt files is the following:
    #   [+ or -]
    #   [possible reply 1]
    #   [possible reply 2]
    #   .
    #   .
    #   .
    #   [last possible reply]
    # this function will just split everything bellow the + or - into a list
    # if there's a + at the top, this function will also add to the list the replies given in the 'default' parameter, else it will add nothing
    # really i just add - because i want to. any character except + would do for a valid dialogue file
    return list(filter(bool, string[2:].split("\n") + (default if string[0] == "+" else [])))
def _fileaddresstoreplies(fileaddress, default):
    # parses the file of the adress 'fileaddress' into a list of replies to use, relative to given 'default'
    # the function _stringtoreplies only handles the contents of the file. this one is the real deal
    return _stringtoreplies(u.quickread(fileaddress), default)
def _addrepliestodictionary(dictionary, fileaddress, default):
    # sets the key with the name being 'fileaddress' without the '.txt' and address fuss to the parsed contants of the file relative to given 'default'
    # this function handles converting the address to a just the raw filename for the key
    dictionary.update({fileaddress[:-4].split("/")[-1]: _fileaddresstoreplies(fileaddress, default)})
def _dictionaryofreplies(folderaddress):
    # parses given folder of txt files with the address 'folderaddress' to a dictionary with its keys the parsed names of the txt files and values the parsed replies of the corresponding files
    returning = dict()
    _addrepliestodictionary(returning, "{}/{}".format(folderaddress, "DEFAULT.txt"), [])
    for fileaddress in u.filesindir(folderaddress):
        _addrepliestodictionary(returning, "{}/{}".format(folderaddress, fileaddress), returning["DEFAULT"])
    return returning
def _dictionaryofdictionariesofreplies(folderaddress):
    # parses given folder of folders of txt files to a dictionary of dictionaries of replies
    # a folder of the folder has its naming '[+ or -] [name]', if it has a + it inherits from the '- DEFAULT' folder. you get the gist
    returning = dict()
    returning["DEFAULT"] = _dictionaryofreplies("{}/{}".format(folderaddress, "- DEFAULT"))
    for subfoldername in u.foldersindir(folderaddress):
        returning[subfoldername[2:]] = _dictionaryofreplies("{}/{}".format(folderaddress, subfoldername))
        if subfoldername[0] == "+":
            _adddict(returning[subfoldername[2:]], returning["DEFAULT"])
    return returning

commandreplies = _dictionaryofdictionariesofreplies("dialogue/command") # dictionary containing dictionaries of replies for every given command situation
def commandreply(commandname, situation):
    # returns a string of a reply sir gts can give when the command with the name 'commandname' gives out situation 'situation'
    if commandname not in commandreplies[situation]:
        commandname = "DEFAULT"
    return u.randomelement(commandreplies[situation][commandname])

pingreplies = _dictionaryofdictionariesofreplies("dialogue/ping") # dictionary with its keys being user ids and values being subscriptables containing possible replies to those users
def pingreply(messagecontent, userid):
    # returns a string of a reply gts can give when he gets pinged, depending by who (userid)
    if userid not in pingreplies:
        userid = "DEFAULT"
    return u.randomelement(_understoodword(messagecontent, pingreplies[userid]))

passivereplies = _dictionaryofdictionariesofreplies("dialogue/passive")
def passivereply(messagecontent, userid):
    # returns an uncalled for string that gts would feel like jumping in with according to the messagecontent and who sent it
    if userid not in passivereplies:
        userid = "DEFAULT"
    return u.randomelement(_understoodword(messagecontent, passivereplies[userid]))
