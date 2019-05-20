"""
module dedicated to handling gts' replies

things like
what gts says when succeeding command x
what gts says when receiving invalid parameters on command y
what gts says when someone pings him saying "z"
what gts says when he gets an itch on his metallic ass
the list goes on for a while



behold me trying to explain how this shit works:



the replies folder in this repository is a dummy folder for debugging and illustration
it is not the actual one (which contains a fuckton of stuff)
though by just looking into it, you should get the gist of how gts' words are stored in his head


ignoring the + and - shit for now,
basically each file in these folders (dialogue file) represents a type of reply
a type of reply is triggered by unique circumstances
these unique circumstances can be seen in the files path and name

for example: the dialogue file with the path "replies/ping/(+ or -) <highguards id>/hi.txt"
would contain what gts could say when highguard pings him at the beginning of his message saying something that contains " hi ". (this is in the case where we don't take order and plurals into consideration, i'll explain later)
so you can literally say that when gts sees highguard pinging him, sending something that contains " hi "
his brain goes "beep boop // ping // highguard // hi // beep boop // xyz" (kind of like p0tat).

another example: the dialogue file with the path "replies/command/- invalid/destroy.txt"
would contain what gts would say when he receives the (hypothetical) "7!destroy" command with invalid arguments



anything named DEFAULT or DEFAULT.* is an exception. it is basically a catch for anything that gts has no clue about.
applies both at file level and folder level
for example: if the contents of the folder "replies/ping/- <john smith id>" are "DEFAULT.txt", "hello.txt" and "kitten.txt"
then john smith pinging gts at the beginning of his message and saying something like "Hello."

_NO_COMMAND is also an exception when found in "replies/command/- success".
it's a fake command that does nothing and is always successful at doing nothing (kind of like marco).
it gets pseudo-called (i made that word up) as a placeholder for every command that doesn't exist.
thus, the replies you write

it's funny when you think about it. if you don't look at the source code, when you tell gts "7!_NO_COMMAND" there is actually no way to tell
whether you have called the existant command _NO_COMMAND and it has returned one of its success responses
or _NO_COMMAND doesn't exist and he answered accordingly


that's pretty obvious and all, but now what's up with the + and - shit?

in dialogue files + means "include" or "inherit". anything except + means "exclude" or "be on ur own" (i put - for preference)

what these signs do at a file level (the signs you see at the start of files)
is they make gts treat their contents as also containing what he perceives the DEFAULT.txt file to contain

for example: if the folder "replies/passive/- <jeromes id>" contains the files

"DEFAULT.txt" with the content:
    -
    default reply 1
    default reply 2

"faggot.txt" with the content:
    -
    a
    b
    c

and "gravity.txt" with the content:
    +
    qwerty
    iopa
    zxcv

thanks to that +, gts would treat "gravity.txt"s contents as
    qwerty
    iopa
    zxcv
    default reply 1



there's a lot more to tell, mostly about how + and - behaves at folder level (the ones you see on folders)
but i'm lazy to explain more so yeah good luck figuring it out on your own

one thing that i wanted to mention about order and plurals
in the message content "hi guys my name is josh" if gts knows the words "guys", "name" and "josh" only "guys" will be taken into consideration
and the word should be implemented as "guy.txt" because gts can actually detect plurals and singulars (at a pretty bad level though, he's kind of stupid)



thus, conclusion of everything said is: why are you even reading this
"""




PATH = "replies" # this is the path from run.py to the replies folder



from random import choice

from .utilities import Path, word_in_container



# get ready for a class inception



class ReplyType:
    "interface for a dialogue file"



    def __init__(self, reply_file_path):
        self.name = reply_file_path.stem

        parsed = filter(bool, (line.strip() for line in reply_file_path.lines()))

        self.include = next(parsed) == "+"
        self.replies = list(parsed)



    def get(self, *, collection, default_collection):
        "returns a random reply, relative to the collection it is in and the default collection"
        if self.include:
            adding = collection.default.replies
            if collection.include:
                if self.name in default_collection.reply_types:
                    adding = adding + default_collection.reply_types[self.name].replies
                    if default_collection.reply_types[self.name].include:
                        adding = adding + default_collection.default.replies
                else:
                    adding = adding + default_collection.default.replies
        else:
            adding = list()
        return choice(self.replies + adding)






class CollectionOfReplyTypes:
    "interface for a folder of dialogue files"


    def __init__(self, reply_folder_path):
        self.name = reply_folder_path.name[2:]
        self.include = reply_folder_path.name.startswith("+")

        self.reply_types = dict()
        for file_path in reply_folder_path.files():
            self.reply_types[file_path.stem] = ReplyType(file_path)

        self.default = self.reply_types["DEFAULT"]



    def get(self, reply_type, *, default_collection):
        "returns a random reply of given type from the collection, relative to given default collection"
        if reply_type in self.reply_types:
            rt = self.reply_types[reply_type]
        else:
            rt = self.default

        return rt.get(collection = self, default_collection = default_collection)



class CollectionOfCollectionsOfReplyTypes:
    "interface for a folder of folders of dialogue files"



    def __init__(self, path):
        self.name = path.name

        self.collections = dict()
        for folder_path in path.folders():
            self.collections[folder_path.name[2:]] = CollectionOfReplyTypes(folder_path)

        self.default_collection = self.collections["DEFAULT"]


    def get(self, collection, reply_type):
        "returns a random reply from given collection, of given type"
        if collection in self.collections:
            rt = self.collections[collection]
        else:
            rt = self.default_collection

        return rt.get(reply_type, default_collection = self.default_collection)



    def reply_types(self, collection):
        "yields all reply types of given collection"
        if collection in self.collections:
            yield from self.collections[collection].reply_types
            if not self.collections[collection].include:
                return
        yield from self.default_collection.reply_types



replies = dict()
for subpath in Path(PATH).folders():
    replies[subpath.name] = CollectionOfCollectionsOfReplyTypes(subpath)





def command_reply(command_name, situation):
    "returns a string of a reply that gts would give for given command in given situation"
    return replies["command"].get(situation, command_name)



def reply(kind):
    "returns a replying function that takes who sent the message and what the message contains into consideration"
    def wrapper(author_id, message_content):
        author_id = str(author_id)
        return replies[kind].get(author_id, word_in_container(message_content, set(replies[kind].reply_types(author_id))))
    return wrapper



ping_reply = reply("ping") # returns a string of a reply that gts would give to given pinger and given message content
passive_reply = reply("passive") # returns a string that gts would randomly feel like sending, relative to given author id and message content
