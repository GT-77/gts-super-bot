import dialogue as d
print(d.passivereplies)
x = input()
while x != "exit":
    x = x.split("| ")
    print(x)
    for i in range(50):
        print("<G!T!S><> ", d.passivereply(x[0], x[1]))
    x = input()
