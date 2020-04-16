import discord as d

with open('token.txt') as t_file:

    token = t_file.read().split()[0].strip()


client = d.Client()

@client.event
async def on_ready():



    with open('gts super bot v2.png', 'rb') as new_avatar_file:
        new_avatar = new_avatar_file.read()


    await client.edit_settings (

        convert_emoticons = False,

        explicit_content_filter = d.UserContentFilter.disabled,

    )

    await client.edit (

        avatar = new_avatar # i look 2 cool


    ,   house = d.HypeSquadHouse.bravery

    )



    await client.close()





client.run(token)


































# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
