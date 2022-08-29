from .ips import*
class _key():
    loop:bool
    game:bool
    level:"list[int,int]"
    has_perfect:bool
    def init(self):
        self.loop=True
        self.game=False
        self.level=[1,1]
        self.has_perfect=False
    def end(self):
        self.loop=self.game=False
    def __getattr__(self,attr:str):
        raise AttributeError("attribute %s not initiallized"%attr)
key=_key()