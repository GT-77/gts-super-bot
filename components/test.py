from asyncio import get_event_loop as gel
from importlib import reload
import commands as c
class Message:
    def __init__(self, content):
        self.content = content
loop = gel()
ruc = loop.run_until_complete
