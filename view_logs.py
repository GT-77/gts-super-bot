from os import system
from pathlib import Path
from datetime import datetime
from time import sleep



PATH = 'databases/logs/logging'



log_path = Path(PATH) / ( str(datetime.now().date()) + '.logs')



def niggerlicious_decoding(file):

    pos = file.tell()

    while True:

        try:

            rt = file.read()

        except UnicodeDecodeError:

            pos -= 1

        else:
            break

    return rt









def get_latest(display = 2000):

    if log_path.is_file():

        display *= 2

        with log_path.open(encoding = 'UTF-8') as logs:

            logs.seek(0, 2)

            if logs.tell() < display:

                logs.seek(0, 0)

            else:

                logs.seek(logs.tell() - display)



            return niggerlicious_decoding(logs)

    else:

        return log_path.name + ' currently doesn\'t exist. todays logs are empty.'






def refresh_countdown(sec = 10):

    for i in range(sec, 0, -1):

        print('refreshing in', i, 'seconds', end = '\r')

        sleep(1)

    print()



def clear_screen():

    system('cls')



if __name__ == '__main__':

    while True:

        print(get_latest(), end = '\n\n\n')

        refresh_countdown()

        clear_screen()


































#
