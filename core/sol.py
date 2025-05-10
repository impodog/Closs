from .ips import*
from .key import*
from .res import*
from .save import*
def invert(d:dict)->dict:
    r:dict=dict()
    for k,v in d.items():r[v]=k
    return r
def rep_signs(string:str):
    for sign,rep in REP_SIGNS.items():
        string=string.replace("\\"+sign,rep)
    return string
def return_signs(string:str):
    string=string.replace("_"," ")
    for sign,rep in REP_SIGNS.items():
        string=string.replace(rep,sign)
    return string
PATTERN_CL=r"c([\d]+)\/([\d]+)\.lev"
def get_levelname(path:str):
    group=re.search(PATTERN_CL,path)
    return [int(group.group(1)),int(group.group(2))]
def get_path(levelname:"list[int,int]"):return LEVEL%tuple(levelname)
def is_trueind(ind:"tuple[int,int]")->bool:return 0 <= ind[0] < lo.shape[0] and 0 <= ind[1] < lo.shape[1]
def draw_warparrow(start:"tuple[int,int]",end:"tuple[int,int]"):
    pygame.draw.line(lo.foreground,WHITE,start,end,3)
    d=vr.dire(start,end,1)
    tmp_arrow=pygame.transform.rotate(pic_arrow,-d.angle)
    tmp_size=tmp_arrow.get_size()
    pos=(end[0]-tmp_size[0]//2,end[1]-tmp_size[1]//2)
    lo.foreground.blit(tmp_arrow,pos)
def neg(t:"tuple[int,int]"):return (-t[0],-t[1])
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
    direct_win:bool
    is_winning:bool
    level_name:str
    level_name_surf:pygame.Surface
    level_name_surf_pos:"tuple[int,int]"
    def init(self,shape,custom:bool=False):
        self.objs=list()
        self.win_sign=dict()
        self.maxind=(shape[0]-1,shape[1]-1)
        self.moved=list()
        self.force_moved=list()
        self.steps_used=0
        self.perfect_steps=None
        self.player_activity=False
        self.stop_moving_sign=False
        self.direct_win=False
        self.is_custom=custom
        self.gravity=DOWN
        self.level_name=None
        self.next_level=None
        self.is_winning=False
        self.level_name_surf=None
        self.reshape(shape)
        self.refresh()
    def reshape(self,shape):
        self.shape=shape
        self.background_size=(LENGTH*self.shape[0],LENGTH*self.shape[1])
        self.background_start=((SCR_LENGTH-self.background_size[0])//2,(SCR_WIDTH-self.background_size[1])//2)
        self.background=pygame.Surface(self.background_size)
        self.foreground=pygame.Surface(self.background_size)
        self.foreground.set_colorkey(BLACK)
        self.old_foreground=self.foreground.copy() 
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                self.background.blit(pic_empty,(x*LENGTH+EMPTY_START,y*LENGTH+EMPTY_START))
        for i in range(shape[1]):
            self.objs.append(list())
            for p in range(shape[0]):
                self.objs[-1].append(list())
        self.refresh()
    def refresh(self):
        if self.player_activity:
            self.moved=list()
            self.force_moved=list()
            self.player_activity=False
            self.stop_moving_sign=False
            self.old_foreground=self.foreground.copy()
            self.foreground=pygame.Surface(self.background_size)
            self.foreground.set_colorkey(BLACK)
        if self.level_name_surf is None and self.level_name is not None:
            self.level_name_surf=fonttextlar.render(self.level_name,True,WHITE)
            self.level_name_surf_pos=(5,SCR_WIDTH-self.level_name_surf.get_size()[1]-5)
    def init_winsigns(self):
        for aobj in get_lo().objs:
            for lobj in aobj:
                for obj in lobj:
                    if isinstance(obj,dest):self.win_sign[obj.tag]=False
    def is_forced(self,obj:"Closs_Object"):return obj in self.force_moved
    def is_moved(self,obj:"Closs_Object"):return obj in self.moved
    def check_winning(self):self.is_winning = self.is_winning or all(self.win_sign.values()) or self.direct_win
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
        self.existing:bool=True
        self.appsize=((LENGTH-size[0])//2,(LENGTH-size[1])//2)
    def get_showpos(self):return (self.ind[0]*LENGTH+self.appsize[0]+lo.background_start[0],self.ind[1]*LENGTH+self.appsize[1]+lo.background_start[1])
    def getrel_showpos(self):return (self.ind[0]*LENGTH+self.appsize[0],self.ind[1]*LENGTH+self.appsize[1])
    def get_center(self):return (self.ind[0]*LENGTH+LENGTH//2+lo.background_start[0],self.ind[1]*LENGTH+LENGTH//2+lo.background_start[1])
    def getrel_center(self):return (self.ind[0]*LENGTH+LENGTH//2,self.ind[1]*LENGTH+LENGTH//2)
    def __pycrput__(self):screen.blit(self.picture,self.get_showpos())
    def receive(self,sign:"tuple[Closs_Object,tuple[int,int],bool]"):return True
    def receivepull(self,sign:"tuple[Closs_Object,tuple[int,int],bool]"):return True
    def send(self,sign:"tuple[int,int]",rec:"list[Closs_Object]",*exclude:"Closs_Object",must_not_move:bool=True,send_pull:bool=False):
        result=True
        for obj in rec.copy():
            if obj not in exclude and (not lo.is_moved(obj) or not must_not_move):
                if send_pull:record=obj.receivepull((self,sign,must_not_move,exclude))
                else:record=obj.receive((self,sign,must_not_move,exclude))
                result=result and record
        return result
    def request_move(self,direction:object,must_not_move:bool=True,*exclude,do_pull:bool=True):
        self.last_move=None
        direction1=direction
        direction2=neg(direction)
        target1=vr.overlap2(self.ind,direction1)
        target2=vr.overlap2(self.ind,direction2)
        res1=False
        res2=True
        if is_trueind(target1):
            tar_obj=get_indobj(target1)
            res1=self.send(direction1,tar_obj,*exclude,must_not_move=must_not_move)
        else:return False
        if is_trueind(target2) and res1 and do_pull:
            tar_obj2=get_indobj(target2)
            res2=self.send(direction1,tar_obj2,*exclude,must_not_move=must_not_move,send_pull=True)
        if not self.existing:return True
        res=res1 and res2
        if res:
            self.perform_move(target1,tar_obj,direction1)
            for obj in tar_obj:
                if isinstance(obj,ice):
                    obj.skate(self)
            return True
        return False
    def perform_move(self,target:"tuple[int,int]",tar_obj:"list[Closs_Object]",direction:"tuple[int,int]"):
        cur_obj=self.get_cur_obj()
        self.remove()
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
    def remove(self)->bool:
        try:self.get_cur_obj().remove(self);return True
        except:return False
    def destroy(self)->bool:
        if self.existing:
            self.existing=False
            return self.remove()
    def __str__(self):return self.__class__.__name__
    @classmethod
    def get_dest_name(cls):return cls.__name__
class transfer():
    def __init__(self,b:bool):self.b=b
    def __bool__(self):return self.b
class void():...
class solid():...
class weak():...
class stop(Closs_Object,solid):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return False
class space(Closs_Object,void):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return True
class pull(Closs_Object,solid):
    def receivepull(self,sign:"tuple[Closs_Object,tuple[int,int],bool]"):return self.request_move(sign[1],sign[2],*sign[3],self,do_pull=True)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],player):return False
        else:return self.request_move(sign[1],sign[2],*sign[3],self,do_pull=False)
class push(Closs_Object,solid):
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return self.request_move(sign[1],sign[2],*sign[3],self,do_pull=False)
    def receivepull(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],player):return True
        else:return self.request_move(sign[1],sign[2],*sign[3],self,do_pull=True)
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
        if isinstance(sign[0],conveyor):return self.request_move(sign[1],sign[2],*sign[3])
        else:return True
class empty():
    @classmethod
    def get_dest_name(cls):return "empty"
class cyan(player):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_cyan,CYAN_SIZE,ind)
class boxtype():...  
class box(push,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_box,box_size,ind)
class bluebox(push,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_bluebox,bluebox_size,ind)
class weakbox(push,boxtype,weak):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_weakbox,weakbox_size,ind)
    def request_move(self,*args,**kwargs):
        reqresult=super().request_move(*args,**kwargs)
        if not reqresult:
            if self.remove():
                get_profile()["weakbox-destroy"]+=1
        return True
class wall(stop):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_wall,wall_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):return False
class dest(space):
    def __init__(self,ind:"tuple[int,int]",req:type):
        self.req=req
        img=font.render(self.req.get_dest_name(),True,WHITE if self.req is empty else GREEN)
        super().__init__(img,img.get_size(),ind)
    def final_detect(self):
        cur_obj = self.get_cur_obj()
        sign=self.req is empty and len(cur_obj) == 1
        for obj in cur_obj:
            sign = sign or isinstance(obj,self.req)
        lo.win_sign[self.tag]=sign
    def analyze_parse(self):
        lo.win_sign[self.tag]=False
    def destroy(self):
        res=super().destroy()
        if res:lo.win_sign.pop(self.tag)
        return res
class nameof(space):
    def __init__(self,ind:"tuple[int,int]",req:type):
        self.req=req
        img=font.render(self.req.__name__,True,GREEN)
        super().__init__(img,img.get_size(),ind)
class text(space):
    def __init__(self,ind:"tuple[int,int]",*string:str):
        self.string=''
        for s in string:self.string+=str(s)
        self.string=return_signs(self.string)
        img=fonttext.render(self.string,True,WHITE)
        super().__init__(img,img.get_size(),ind)
    def get_showpos(self):return (self.ind[0]*LENGTH+5+lo.background_start[0],self.ind[1]*LENGTH+self.appsize[1]+lo.background_start[1])
class spike(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_spike,spike_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        return True
    def detect2(self):
        for obj in self.get_cur_obj():
            if isinstance(obj,cyan) and obj.ind == self.ind:
                obj.destroy()
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
class warptype(push,weak):
    def __init__(self,picture,size:"tuple[int,int]",ind:"tuple[int,int]"):
        self.next:warp=self
        super().__init__(picture,size,ind)
    def detect(self):
        if self.next is not self:
            cur=self.get_cur_obj()
            tar=self.next.get_cur_obj()
            for obj in cur.copy():
                if obj is not self and not lo.is_forced(obj):
                    obj.remove()
                    obj.ind=self.next.ind
                    tar.append(obj)
                    lo.force_moved.append(obj)
                    draw_warparrow(self.getrel_center(),self.next.getrel_center())
    def destroy(self):
        res=super().destroy()
        if res and self.next is not self:
            last_warp:warptype=self
            while last_warp.next is not self:
                last_warp = last_warp.next
            last_warp.next = self.next
        return res
class warp(warptype):
    def __init__(self,ind:"tuple[int,int]"):
        self.next:warp=None
        super().__init__(pic_warp,warp_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if not isinstance(sign[0],player):return super().receive(sign)
        else:return True
class greenwarp(warptype):
    def __init__(self,ind:"tuple[int,int]"):
        self.next:warp=None
        push.__init__(self,pic_greenwarp,warp_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],warptype):get_profile()["warp-warp"]=True;return super().receive(sign)
        elif not isinstance(sign[0],player):return True
        else:return super().receive(sign)
class ice(space):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_ice,ice_size,ind)
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
        super().__init__(pic_crusher,crusher_size,ind)
    def detect2(self):
        cur=self.get_cur_obj()
        for obj in cur.copy():
            if isinstance(obj,boxtype):
                obj.remove()
class leaf(push,weak):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_leaf,leaf_size,ind)
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
        super().__init__(pic_none,switch_size,ind)
    def cg_grav(self,direction:"tuple[int,int]"):
        lo.gravity=direction
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        self.cg_grav(sign[1])
        return super().receive(sign)
    def final_detect(self):
        self.picture=SWITCH_DIRS[lo.gravity]
    def analyze_parse(self):
        self.final_detect()
class hookbox(pull,boxtype):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_hookbox,hookbox_size,ind)
class antidest(space):
    def __init__(self,ind:"tuple[int,int]",req:type):
        self.req=req
        is_empty=self.req is empty
        img=font.render("any" if is_empty else self.req.get_dest_name(),True,WHITE if is_empty else RED)
        super().__init__(img,img.get_size(),ind)
        lo.win_sign[self.tag]=False
    def final_detect(self):
        cur_obj = self.get_cur_obj()
        sign=True
        for obj in cur_obj:
            sign = sign and not isinstance(obj,self.req)
        sign=sign or (self.req is empty and len(cur_obj)!=1) 
        lo.win_sign[self.tag]=sign
    def analyze_parse(self):
        lo.win_sign[self.tag]=False
    def destroy(self):
        res=super().destroy()
        if res:lo.win_sign.pop(self.tag)
        return res
class ikey(push,weak):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_key,key_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],lock):sign[0].destroy();self.destroy();return True
        else:return super().receive(sign)
    @classmethod
    def get_dest_name(cls):return "key"
class lock(push):
    def __init__(self,ind:"tuple[int,int]"):
        super().__init__(pic_lock,lock_size,ind)
    def receive(self, sign: "tuple[Closs_Object,tuple[int,int],bool]"):
        if isinstance(sign[0],ikey):sign[0].destroy();self.destroy();return True
        else:return super().receive(sign)
class pictureof(space):
    def __init__(self,ind:"tuple[int,int]",pic:pygame.Surface):
        super().__init__(pic,pic.get_size(),ind)
class level_switcher(space):
    def __init__(self,ind:"tuple[int,int]",chapter:str,level:str):
        self.level=[int(chapter),int(level)]
        super().__init__(pic_none,UNDEFINED_SIZE,ind)
    def final_detect(self):
        for obj in self.get_cur_obj():
            if isinstance(obj,player):
                get_profile()["progress"]=self.level
                lo.direct_win=True
                return
class lasergun_type(stop):
    def __init__(self,ind:"tuple[int,int]",laser_type:type,dicts:"tuple[dict,dict]",fixed_direction:"tuple[int,int]"=None):
        self.dicts=dicts
        super().__init__(pic_none if fixed_direction is None else self.dicts[1][fixed_direction],lasergun_size,ind)
        self.laser_type=laser_type
        self.bundled_laser:"list[laser]"=list()
        self.fixed_direction=fixed_direction
        self.grav:"tuple[int,int]"=lo.gravity if self.fixed_direction is None else self.fixed_direction
    def final_detect(self):
        if self.fixed_direction is None:self.picture = self.dicts[0][self.grav]
    def detectpre(self):
        for co in self.bundled_laser:
            co.remove()
    def detect2(self):
        if self.fixed_direction is None:self.grav=lo.gravity
        next_ind=self.ind
        end_loop=False
        flip=False
        tmpgrav=self.grav
        while True:
            next_ind=vr.overlap2(tmpgrav,next_ind)
            if not is_trueind(next_ind):break
            indobj=get_indobj(next_ind)
            for co in indobj:
                if self.next_tile(co):
                    end_loop=True
                    break
            if end_loop:break
            new_laser = self.laser_type(next_ind,tmpgrav,flip)
            self.bundled_laser.append(new_laser)
            indobj.insert(0,new_laser)
            desind=new_laser.destroy_tile()
            if desind is not None:
                if desind[0] is warp:
                    next_ind=desind[1]
                elif desind[0] is reflector:
                    tmpgrav = desind[1]
            flip = not flip
    def next_tile(self,co:Closs_Object):
        return False
    def analyze_parse(self):
        self.final_detect()
class destroy_lasergun(lasergun_type):
    def __init__(self, ind: "tuple[int,int]", fixed_direction: "tuple[int,int]" = None):
        super().__init__(ind, destroy_laser,(LASERGUN_DIRS,FIXED_LASERGUN_DIRS), fixed_direction)
    def next_tile(self, co: Closs_Object):
        return isinstance(co,solid) and not isinstance(co,weak)
class transform_lasergun(lasergun_type):
    def __init__(self, ind: "tuple[int,int]", fixed_direction: "tuple[int,int]" = None):
        super().__init__(ind, transform_laser,(LASERGUNTRANS_DIRS,FIXED_LASERGUNTRANS_DIRS), fixed_direction)
    def next_tile(self, co: Closs_Object):
        return isinstance(co,stop) and not isinstance(co,weak)
class laser(space):
    def __init__(self,ind: "tuple[int,int]",direction:"tuple[int,int]",flip:bool=False):
        self.direction=direction
        super().__init__(pic_none,UNDEFINED_SIZE,ind)
    def destroy_tile(self):...
    def find_warp(self):
        for obj in self.get_cur_obj():
            if isinstance(obj,warptype):
                self.destroy()
                return obj.next.ind
        return None
    def find_reflector(self):
        for obj in self.get_cur_obj():
            if isinstance(obj,reflector):
                self.destroy()
                refdir=obj.get_ref_dir(self.direction)
                if refdir is not None:obj.light(isinstance(self,transform_laser))
                return refdir
        return None
class destroy_laser(laser):
    def __init__(self,ind: "tuple[int,int]",direction:"tuple[int,int]",flip:bool=False):
        self.direction=direction
        stop.__init__(self,(LASER_FLIPPED_DIRS if flip else LASER_DIRS)[direction], laser_size, ind)
    def destroy_tile(self):
        curobj=self.get_cur_obj()
        warpind = super().find_warp()
        if warpind is not None:return (warp,warpind)
        refind = super().find_reflector()
        if refind is not None:return (reflector,refind)
        for obj in curobj:
            if not isinstance(obj,(laser, dest)):
                obj.destroy()
        return None
class transform_laser(laser):
    def __init__(self,ind: "tuple[int,int]",direction:"tuple[int,int]",flip:bool=False):
        self.direction=direction
        stop.__init__(self,(LASERTRANS_FLIPPED_DIRS if flip else LASERTRANS_DIRS)[direction], laser_size, ind)
    def destroy_tile(self):
        curobj=self.get_cur_obj()
        to_replace:"dict[Closs_Object,Closs_Object]"=dict()
        warpind = super().find_warp()
        refind = super().find_reflector()
        if warpind is not None:return (warp,warpind)
        elif refind is not None:return (reflector,refind)
        for obj in curobj:
            trans_res=transform(obj)
            if trans_res is not None:
                to_replace[obj]=trans_res
        for obj,trans_res in to_replace.items():
            obj.destroy()
            curobj.append(trans_res)
class reflector(push,weak):
    def __init__(self, ind: "tuple[int,int]", direction:"tuple[int,int]"):
        self.direction=direction
        super().__init__(REFLECTOR_DIRS[direction], reflector_size, ind)
    def get_ref_dir(self,dir:"tuple[int,int]"):
        ccw = get_ccw(self.direction)
        adir = neg(dir)
        if adir == self.direction:return ccw
        elif adir == ccw:return self.direction
        return None
    def detectpre(self):
        self.picture = REFLECTOR_DIRS[self.direction]
    def light(self,use_trans:bool):
        self.picture = (REFLECTOR_LIGHTEDTRANS_DIRS if use_trans else REFLECTOR_LIGHTED_DIRS)[self.direction]
def hide(ind:"tuple[int,int]",co:"Closs_Object"):co.picture=pic_none;return co
def instanceof(ind:"tuple[int,int]",co:"type[Closs_Object]"):return co(ind)
def getpicture(ind:"tuple[int,int]",co:"Closs_Object"):return co.picture
def getnone(ind:"tuple[int,int]"):return None
co_transform:"dict[type,type]"={
    box:bluebox,
    weakbox:hookbox
}
def transform(co:Closs_Object):
    for trans1,trans2 in co_transform.items():
        if isinstance(co,trans1):return trans2(co.ind)
        elif isinstance(co,trans2):return trans1(co.ind)
    return None
def get_ccw(dir:"tuple[int,int]"):return (dir[1],-dir[0])
def get_clockwise(dir:"tuple[int,int]"):return (-dir[1],dir[0])