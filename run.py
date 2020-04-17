from asyncio import sleep, new_event_loop, set_event_loop

import discord as d

from components import gts







@gts.event
async def on_ready():

    gts.logs.awoken_log() # .ready_log() works too but log_awoken looks / sounds cooler

    while True:

        for presence in presences:

            await gts.change_presence(activity = d.Game(presence))
            await sleep(3)





with open('replies/presences.txt', encoding = 'UTF-8') as file:

    presences = list()

    for line in file:

        line = line.strip()

        if line:

            presences.append(line)





with open('token.txt') as token_file:

    token = token_file.read().split()



'''
while True:

        try:

            gts.run(*token)

        except Exception as exc:

            #gts.logs.log_fatal_uncaught_exception(exc)

            print(exc.__class__.__name__ + ':', str(exc))
            print(eval(input('>>> ')))

            set_event_loop(new_event_loop())


        else:

            break
'''

gts.run(*token)



gts.logs.log_asleep()
