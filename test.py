from asyncio import get_event_loop as gel
loop = gel()
ruc = loop.run_until_complete
from components.database import *
P = Path
path = P(r"files\xyz\abc")
s = Set(path)
class ATTD:
    def __init__(self, name = "unknown.png"):
        self.filename = name
    async def save(self, path):
        print("doing save stuff", path)
        return path
async def main(*args):
    for arg in args:
        await (s << ATTD(arg))
async def main2(arg1, arg2):
    await (s << ATTD(arg1) << ATTD(arg2))

args = "gt.he", "is", "gay.asfuck", "lole.string"
def run_main(): return ruc(main(*args))
p = Database('omega_xyz')
print("fuck you")
