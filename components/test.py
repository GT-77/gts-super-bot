import dialogue as d
from pprint import pprint
pprint(d.passivereplies)
x = input()
while x != "exit":
    x = x.split("| ")
    for i in range(50):
        print(d.passivereply(x[0], x[1]))
    x = input()
