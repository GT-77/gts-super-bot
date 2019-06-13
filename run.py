from components import gts



@gts.event
async def on_ready():

    gts.logs.log_awoken() # .log_ready() works too but log_awoken looks / sounds cooler



with open('token.txt') as token_file:

    token = token_file.read().split()



while True:

    try:

        gts.run(*token)

    except Exception as exc:

        gts.logs.log_fatal_uncaught_exception(exc)

    else:

        break



gts.logs.log_asleep()
