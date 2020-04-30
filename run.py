import discord as d
from components import gts



with open('token.txt') as token_file:
    token = token_file.read().split()



gts.run(*token)



gts.logs.log_asleep()
