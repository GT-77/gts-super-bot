import utilities as u
def _add_dict(dict0, dict1):
    # adds dictionary dict1 into dict0
    for key in dict1:
        if key not in dict0:
            dict0[key] = dict1[key]
        else:
            dict0[key] += dict1[key]
def _understood_word(string, dictionary):
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
def _string_to_replies(string, default):
    # turns given 'string' (what you see in .txt files from the dialogue folders) into a list of replies to actually use, relative to given 'default'
    # the format of what you see in dialogue txt files is the following:
    #   [+ or -]
    #   [possible reply 1]
    #   [possible reply 2]
    #   .
    #   .
    #   .
    #   [last possible reply]
    # this function will just split everything bellow the + or - into a list and removes null strings
    # if there's a + at the top, this function will also add to the list the replies given to the 'default' parameter, else it will add nothing
    # really i just add - because i want to. any character except + would do for a valid dialogue file that doesn't include default
    return list(filter(bool, string[2:].split("\n") + (default if string[0] == "+" else [])))
def _file_address_to_replies(file_address, default):
    # parses the file of the adress 'file_address' into a list of replies to use, relative to given 'default'
    # the function _string_to_replies only handles the contents of the file. this one is the real deal
    return _string_to_replies(u.quickread(file_address), default)
def _add_replies_to_dictionary(dictionary, file_address, default):
    # sets the key with the name being 'file_address' without the '.txt' and address fuss to the parsed contents of the file relative to given 'default'
    # this function handles converting the address to just the raw filename for the key
    dictionary.update({file_address[:-4].split("/")[-1]: _file_address_to_replies(file_address, default)})
def _dictionary_of_replies(folder_address):
    # parses given folder of txt files with the address 'folder_address' to a dictionary with its keys the parsed names of the txt files and values the parsed replies of the corresponding files
    returning = dict()
    _add_replies_to_dictionary(returning, "{}/{}".format(folder_address, "DEFAULT.txt"), []) # i set the '"DEFAULT"' key of the dictionary first because it's not guaranteed that u.filesindir will yield "DEFAULT" first
    for file_address in u.filesindir(folder_address):
        _add_replies_to_dictionary(returning, "{}/{}".format(folder_address, file_address), returning["DEFAULT"])
    return returning
def _dictionary_of_dictionaries_of_replies(folder_address):
    # parses given folder of folders of txt files to a dictionary of dictionaries of replies
    # a folder of the folder has its naming '[+ or -] [name]'. if it has a + it inherits from the '- DEFAULT' folder. you get the gist
    returning = dict()
    returning["DEFAULT"] = _dictionary_of_replies("{}/{}".format(folder_address, "- DEFAULT"))
    for subfolder_name in u.foldersindir(folder_address):
        returning[subfolder_name[2:]] = _dictionary_of_replies("{}/{}".format(folder_address, subfolder_name))
        if subfolder_name[0] == "+":
            _add_dict(returning[subfolder_name[2:]], returning["DEFAULT"])
    return returning

replies = dict()
for typeofreply in ("command", "ping", "passive"):
    replies[typeofreply] = _dictionary_of_dictionaries_of_replies("dialogue/{}".format(typeofreply))

def command_reply(commandname, situation):
    # returns a string of a reply sir gts can give when the command with the name 'commandname' gives out situation 'situation'
    if commandname not in replies["command"][situation]:
        commandname = "DEFAULT"
    return u.randomelement(replies["command"][situation][commandname])

def ping_reply(messagecontent, userid):
    # returns a string of a reply gts can give when he gets pinged, depending by who (userid)
    if userid not in replies["ping"]:
        userid = "DEFAULT"
    return u.randomelement(_understood_word(messagecontent, replies["ping"][userid]))

def passive_reply(messagecontent, userid):
    # returns an uncalled for string that gts would feel like jumping in with according to the messagecontent and who sent it
    if userid not in replies["passive"]:
        userid = "DEFAULT"
    return u.randomelement(_understood_word(messagecontent, replies["passive"][userid]))
