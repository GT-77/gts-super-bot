from random import randint
import constants, os, utilities
client = None
utilities.client = client
async def feedback(message, commandname, type):
    for path in os.walk(constants.feedbackPath):
        if commandname == path[0][len(feedbackPath) + 1:]:
            if type in next(os.walk(path))[2]:
                await utilities.message(message.channel, randomitem(utilities.quickread("{}/{}.txt".format(path, type)).split("\n")))
            else:
                await utilities.message(message.channel, randomitem(utilities.quickread("{}/{}.txt".format(path, "DEFAULT")).split("\n")))
    else:
        await utilities.message(message.channel, randomitem(utilities.quickread("{}/{}/{}.txt".format(feedbackPath, "DEFAULT", type)).split("\n")))
    await utilities.log(commandname, type)
