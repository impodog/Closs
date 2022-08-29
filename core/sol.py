from .ips import*
from .key import*
from .res import*
from .save import*
def invert(d:dict)->dict:
    r:dict=dict()
    for k,v in d.items():r[v]=k
    return r
REP_SIGNS={
    ",":"[symcomma]",
    "&":"[symand]",
    "<":"[symlowerthan]",
    "-":"[symhyphen]",
    "\\":"[symbackslash]",
    "/":"[symslash]",
    ":":"[symcolon]",
    "%":"[sympercent]",
    "+":"[symadd]",
    "_":"[symunderline]",
    "(":"[symlbracket]",
    ")":"[symrbracket]",
    "[":"[symlsqbr]",
    "]":"[symrsqbr]",
    "?":"[symquestionmark]",
    "@":"[symat]",
    "*":"[symasterisk]",
    "~":"[symtilde]",
    "=":"[symequal]",
    "\"":"[symdoublequote]",
    "'":"[symsinglequote]",
    ">":"[symgreaterthan]",
    ";":"[symsemicolon]",
    "{":"[symlcubr]",
    "}":"[symrcubr]",
    "^":"[symcuret]",
    "$":"[symdollar]"
}
def rep_signs(string:str):
    for sign,rep in REP_SIGNS.items():
        string=string.replace("\\"+sign,rep)
    return string
def return_signs(string:str):
    string=string.replace("_"," ")
    for sign,rep in REP_SIGNS.items():
        string=string.replace(rep,sign)
    return string
PATTERN_CL=r"level\/c([\d]+)\/([\d]+)\.lev"
CL="level/c%d/%d.lev"
CUSL="level/%s/%s.lev"
def get_levelname(path:str):
    group=re.match(PATTERN_CL,path)
    return [int(group.group(1)),int(group.group(2))]
def get_customlevelname(path:str):
    group=re.match(PATTERN_CL,path)
    return [group.group(1),group.group(2)]
def get_path(levelname:"list[int,int]"):
    if isinstance(levelname[0],int):return CL%tuple(levelname)
    else:return CUSL%tuple(levelname)
def is_trueind(ind:"tuple[int,int]")->bool:return 0 <= ind[0] < lo.shape[0] and 0 <= ind[1] < lo.shape[1]
def draw_warparrow(start:"tuple[int,int]",end:"tuple[int,int]"):
    pygame.draw.line(lo.foreground,WHITE,start,end,3)
    d=vr.dire(start,end,1)
    tmp_arrow=pygame.transform.rotate(pic_arrow,-d.angle)
    tmp_size=tmp_arrow.get_size()
    pos=(end[0]-tmp_size[0]//2,end[1]-tmp_size[1]//2)
    lo.foreground.blit(tmp_arrow,pos)
class level_obj():
    objs:"list[list[list[Closs_Object]]]"
    shape:"tuple[int,int]"
    win_sign:"dict[float,bool]"
    moved:"list[Closs_Object]"
    force_moved:"list[Closs_Object]"
    background_size:"tuple[int,int]"
    background_start:"tuple[int,int]"
    foreground:pygame.Surface
    old_foreground:pygame.Surface
    steps_used:int
    perfect_steps:int
    player_activity:bool
    next_level:str
    background:pygame.Surface
    is_custom:bool
    gravity:"tuple[int,int]"
    stop_moving_sign:bool
    def init(self,shape,custom:bool=False):
        self.objs=list()
        self.win_sign=dict()
        self.maxind=(shape[0]-1,shape[1]-1)
        self.moved=list()
        self.force_moved=list()
        self.shape=shape
        self.steps_used=0
        self.perfect_steps=None
        self.player_activity=False
        self.stop_moving_sign=False
        self.is_custom=custom
        self.gravity=DOWN
        for i in range(shape[1]):
            self.objs.append(list())
            for p in range(shape[0]):
                self.objs[-1].append(list())
        self.next_level=None
        self.background_size=(LENGTH*self.shape[0],LENGTH*self.shape[1])
        self.background_start=((SCR_LENGTH-self.background_size[0])//2,(SCR_WIDTH-self.background_size[1])//2)
        self.background=pygame.Surface(self.background_size)
        self.foreground=pygame.Surface(self.background_size)
        self.foreground.set_colorkey(BLACK)
        self.old_foreground=self.foreground.copy()
        for x in range(get_lo().shape[0]):
            for y in range(get_lo().shape[1]):
                self.background.blit(pic_empty,(x*LENGTH+EMPTY_START,y*LENGTH+EMPTY_START))  
    def refresh(self):
        if self.player_activity:
            self.moved=list()
            self.force_moved=list()
            self.player_activity=False
            self.stop_moving_sign=False
            self.old_foreground=self.foreground.copy()
            self.foreground=pygame.Surface(self.background_size)
            self.foreground.set_colorkey(BLACK)
    def init_winsigns(self):
        for aobj in get_lo().objs:
            for lobj in aobj:
                for obj in lobj:
                    if isinstance(obj,dest):self.win_sign[obj.tag]=False
    def is_forced(self,obj:"Closs_Object"):return obj in self.force_moved
    def is_moved(self,obj:"Closs_Object"):return obj in self.moved
    def check_winning(self):return all(self.win_sign.values())
lo:level_obj
tag_num=0
def gene_tag()->int:
    global tag_num
    tag_num+=1
    return tag_num
def get_lo():
    global lo
    return lo
def create_lo():
    global lo
    lo=level_obj()
def get_indobj(ind:"tuple[int,int]"):return lo.objs[ind[1]][ind[0]]
class Closs_Object():
    def __init__(self,picture,size:"tuple[int,int]",ind:"tuple[int,int]"):
        self.picture=picture
        self.size=size
        self.ind=ind
        self.last_move:"tuple[int,int]"=None
        self.tag=gene_tag()
        self.appsize=((LENGTH-size[0])//2,(LENGTH-size[1])//2)
    def get_showpos(self):return (self.ind[0]*LENGTH+self.appsize[0]+lo.background_start[0],self.ind[1]*LENGTH+self.appsize[1]+lo.background_start[1])
    def getrel_showpos(self):return (self.ind[0]*LENGTH+self.appsize[0],self.ind[1]*LENGTH+self.appsize[1])
    def get_center(self):return (self.ind[0]*LENGTH+LENGTH//2+lo.background_start[0],self.ind[1]*LENGTH+LENGTH//2+lo.background_start[1])
    def getrel_center(self):return (self.ind[0]*LENGTH+LENGTH//2,self.ind[1]*LENGTH+LENGTH//2)
    def __pycrput__(self):screen.blit(self.picture,self.get_showpos())
    def receive(self,sign:"tuple[Closs_Object,tuple[int,int],bool]"):return True
    def send(self,sign:"tuple[int,int]",rec:"list[Closs_Object]",*exclude:"Closs_Object",must_not_move:bool=True):
        result=True
        trans=None
        for obj in rec.copy():
            if obj not in exclude and (not lo.is_moved(obj) or not must_not_move):
                record=obj.receive((self,sign,must_not_move))
                if isinstance(record,transfer):trans=record
                else:result=result and record
        if not result:return False
        elif trans is None:return True
        else:return trans
    def request_move(self,direction:object,must_not_move:bool=True):
        self.last_move=None
        target=vr.overlap2(self.ind,direction)
        if is_trueind(target):
            tar_obj=get_indobj(target)
            res=self.send(direction,tar_obj,must_not_move=must_not_move)
            if isinstance(res,transfer):
                return res.b
            elif res:
                self.perform_move(target,tar_obj,direction)
                for obj in tar_obj:
                    if isinstance(obj,ice):
                        obj.skate(self)
                return True
        return False
    def perform_move(self,target:"tuple[int,int]",tar_obj:"list[Closs_Object]",direction:"tuple[int,int]"):
        cur_obj=self.get_cur_obj()
        cur_obj.remove(self)
        self.ind=target
        tar_obj.append(self)
        lo.moved.append(self)
        self.last_move=direction
    def get_cur_obj(self)->"list[Closs_Object]":return lo.objs[self.ind[1]][self.ind[0]]
    def detectpre(self):...
    def detect(self):...
    def detect2(self):...
    def final_detect(self):...
    def analyze_parse(self):...
    def __str__(self):return self.__class__.__name__
class transfer():
    def __init__(self,b:bool):self.b=b
    def __bool__(self):return self.b
class void():...
class solid():...
class stop(Closs_Object,solid):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return False
class space(Closs_Object,void):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return True
class push(Closs_Object,solid):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return self.request_move(sign[1],sign[2])
class player(Closs_Object,void):
    def __init__(self, picture, size: "tuple[int,int]", ind: "tuple[int,int]"):
        super().__init__(picture, size, ind)
    def run(self,keyi:int):
        overlap=False
        for obj in self.get_cur_obj():
            if isinstance(obj,player) and obj is not self:overlap=True
        if not lo.is_moved(self) and not lo.stop_moving_sign:
            res=False
            lo.player_activity=True
            if keyi == pygame.K_UP:res=self.request_move(UP)
            elif keyi == pygame.K_DOWN:res=self.request_move(DOWN)
            elif keyi == pygame.K_LEFT:res=self.request_move(LEFT)
            elif keyi == pygame.K_RIGHT:res=self.request_move(RIGHT)
            else:lo.player_activity=False
            lo.stop_moving_sign=res and overlap
            return res
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],conveyor):return self.request_move(sign[1],sign[2])
        else:return True
class empty():...
class cyan(player):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_cyan.copy(),CYAN_SIZE,ind)
class boxtype():...  
class box(push,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_box.copy(),box_size,ind)
class bluebox(push,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_bluebox.copy(),bluebox_size,ind)
class weakbox(push,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_weakbox.copy(),weakbox_size,ind)
    def request_move(self,direction:object,must_not_move:bool=True):
        reqresult=super().request_move(direction,must_not_move=must_not_move)
        if not reqresult:
            try:
                self.get_cur_obj().remove(self)
                get_profile()["weakbox-destroy"]+=1
            except:...
        return True
class wall(stop):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_wall.copy(),wall_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return False
class dest(space):
    def __init__(self,ind:"tuple[int,int]",req:type):
        self.req=req
        img=font.render(self.req.__name__,True,GREEN)
        super().__init__(img,img.get_size(),ind)
    def final_detect(self):
        sign=False
        for obj in self.get_cur_obj():
            sign = sign or isinstance(obj,self.req)
        lo.win_sign[self.tag]=sign
class nameof(space):
    def __init__(self,ind:"tuple[int,int]",req:type):
        self.req=req
        img=font.render(self.req.__name__,True,GREEN)
        super().__init__(img,img.get_size(),ind)
class text(space):
    def __init__(self,ind:"tuple[int,int]",string:str):
        self.string=string
        self.string=return_signs(self.string)
        img=fonttext.render(self.string,True,WHITE)
        super().__init__(img,img.get_size(),ind)
    def get_showpos(self):return (self.ind[0]*LENGTH+5+lo.background_start[0],self.ind[1]*LENGTH+self.appsize[1]+lo.background_start[1])
class spike(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_spike.copy(),spike_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        return True
    def detect2(self):
        for obj in self.get_cur_obj():
            if isinstance(obj,cyan) and obj.ind == self.ind:
                obj.get_cur_obj().remove(obj)
                return False
class conveyor(space):
    def __init__(self,ind:"tuple[int,int]",direction:"tuple[int,int]"):
        self.direction=direction
        super().__init__(CONVEYOR_DIRS[direction].copy(),conv_size,ind)
    def detect(self):
        all_obj=self.get_cur_obj().copy()
        all_obj_res=list()
        for obj in all_obj:
            if not lo.is_forced(obj) and obj is not self:
                if isinstance(obj,warp):get_profile()["tele-warp"]=True
                all_obj_res.append(obj)
        self.send(self.direction,all_obj_res,must_not_move=False)
        lo.force_moved.extend(all_obj)
class warptype(push):
    def __init__(self,picture,size:"tuple[int,int]",ind:"tuple[int,int]"):
        self.next:warp=None
        super().__init__(picture,size,ind)
    def detect(self):
        cur=self.get_cur_obj()
        tar=self.next.get_cur_obj()
        for obj in cur.copy():
            if obj is not self and not lo.is_forced(obj):
                cur.remove(obj)
                obj.ind=self.next.ind
                tar.append(obj)
                lo.force_moved.append(obj)
                draw_warparrow(self.getrel_center(),self.next.getrel_center())
class warp(warptype):
    def __init__(self,ind:"tuple[int,int]"):
        self.next:warp=None
        super().__init__(pic_warp.copy(),warp_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if not isinstance(sign[0],player):return super().receive(sign)
        else:return True
class greenwarp(warptype):
    def __init__(self,ind:"tuple[int,int]"):
        self.next:warp=None
        push.__init__(self,pic_greenwarp.copy(),warp_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],warptype):get_profile()["warp-warp"]=True;return super().receive(sign)
        elif not isinstance(sign[0],player):return True
        else:return super().receive(sign)
class ice(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_ice.copy(),ice_size,ind)
    def skate(self, iobj:Closs_Object):
        curind=vr.overlap2(self.ind,iobj.last_move)
        if is_trueind(curind):
            tar_obj=get_indobj(curind)
            next_ice=None
            for obj in tar_obj:
                if isinstance(obj,ice):next_ice=obj
            if iobj.send(iobj.last_move,tar_obj,self,next_ice,must_not_move=False):
                iobj.perform_move(curind,tar_obj,iobj.last_move)
                if next_ice is not None:next_ice.skate(iobj)
        else:return
class crusher(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_crusher.copy(),crusher_size,ind)
    def detect2(self):
        cur=self.get_cur_obj()
        for obj in cur.copy():
            if isinstance(obj,boxtype):
                cur.remove(obj)
class leaf(push):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_leaf.copy(),leaf_size,ind)
    def fall(self):
        curind=vr.overlap2(self.ind,lo.gravity)
        if is_trueind(curind):
            tar_obj=get_indobj(curind)
            next_ice=None
            if self.send(lo.gravity,tar_obj,self,next_ice,must_not_move=False):
                self.perform_move(curind,tar_obj,lo.gravity)
                self.fall()
        else:return
    def detectpre(self):
        self.fall()
class switch(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_switchdown.copy(),switch_size,ind)
    def cg_grav(self,direction:"tuple[int,int]"):
        lo.gravity=direction
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        self.cg_grav(sign[1])
        return super().receive(sign)
    def final_detect(self):
        self.picture=SWITCH_DIRS[lo.gravity]
    def analyze_parse(self):
        self.final_detect()
def hide(ind:"tuple[int,int]",co:"Closs_Object"):co.picture=pic_none;return co
def instanceof(ind:"tuple[int,int]",co:"type[Closs_Object]"):return co(ind)