import subcomponents as sub
import os
client = None
async def reply(message):
    cm = message.content.replace("\n", " ").split(" ")
    user = "DEFAULT"
    if not "love" in cm:
        for id in next(os.walk(sub.fur.constants.replyingPath))[1]:
            if client.id in id:
                user = id
                break
    defaultwords = [word[-4] for word in os.walk("{}/{}".format(sub.fur.constants.replyingPath, "DEFAULT"))]
    userwords = [word[-4] for word in os.walk("{}/{}".format(sub.fur.constants.replyingPath, user))]
    if user == "DEFAULT" or not userwords:
        defaultintersection = [word for word in cm if word in defaultwords]
        if not defaultintersection:
            chosenword = "DEFAULT"
            await sub.fur.message(message.channel, sub.fur.utilities.randomitem(_quickread("{}/{}/{}.txt".format(path[0], "DEFAULT", chosenword))))
            await sub.fur.replylog(user, word)
        else:
            chosenword = sub.fur.utilities.randomitem(defaultintersection))).split("\n")
        await sub.fur.message(message.channel, sub.fur.utilities.randomitem(_quickread("{}/{}/{}.txt".format(path[0], "DEFAULT", chosenword))))
        await sub.fur.replylog(user, word)
    else:
        chosenword = sub.fur.utilities.randomitem(userintersection))).split("\n")
        await sub.fur.message(message.channel, sub.fur.utilities.randomitem(_quickread("{}/{}/{}.txt".format(path[0], user, chosenword))))
        await sub.fur.replylog(user, word)
