'''

this shit is almost ireversible so i better be careful xyz

'''



from urllib.request import Request as Rq, urlopen as uo

from urllib.error import HTTPError

from bs4 import BeautifulSoup as BS

from components.utilities import Path

from components.database import Pointer as P



im_friendly = {'User-Agent': 'Mozilla/5.0'}



databases = P(Path('databases'))

xyz_mb = databases.xyz.xyz.matthias_bider

jabroni = databases.get_log.ecchi['james_bree-morgan_presents_case_number_87798972__he_has_fun_doin_it']

extracting_tags = ['a', 'span', 'p', 'h1']

added = cleared = 0

jabroni_itr = iter(jabroni)

cleared = 36
for i in range(cleared):
    next(jabroni_itr)

for url in jabroni_itr:

    try:

        rp = uo(Rq(url, headers = im_friendly))

        rd = rp.read()

        soup = BS(rd, 'html.parser')

    except Exception as fuck:

        print(url, 'gives', fuck)

        print('i\'ll keep goin i guess')
        continue



    for tag in extracting_tags:

        for tag_obj in soup.find_all(tag):

            xyz_mb << tag_obj.text

            added += 1

            print(added, '->', tag_obj.text[:20], '...')

    cleared += 1
    print('CLEARED', cleared, '->', rp.url, flush = True)










































# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
