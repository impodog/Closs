from .sol import*
from .save import*
class ach():
    all_ach:"dict[str,list[bool,str,pygame.Surface,FunctionType]]"
    def __init__(self):
        self.all_ach=dict()
        self.ach_list=list()
    def add_ach(self,name:str,description:str,picture:pygame.Surface,define:FunctionType):
        picture=pygame.transform.scale(picture,ACHPIC_SIZE)
        self.ach_list.append(name)
        self.all_ach[name]=[self.ach_list.index(name) in get_profile()["achievements"],description,picture,define]
    def parse_ach(self):
        i=0
        for a,v in self.all_ach.items():
            if not v[0] and v[3] is not None:
                v[0]=v[3]()
                if v[0]:
                    get_profile()["achievements"].append(i)
            i+=1
    def generate_surf(self):
        pagenum=math.ceil(len(self.all_ach)/EACH_PAGE)
        surfs=list()
        tup_title=tuple(self.all_ach.keys())
        tup_det=tuple(self.all_ach.values())
        for i in range(pagenum):
            surf=pygame.Surface((SCR_LENGTH,SCR_WIDTH))
            cury=0
            cur_title=tup_title[i*EACH_PAGE:(i+1)*EACH_PAGE]
            cur_det=tup_det[i*EACH_PAGE:(i+1)*EACH_PAGE]
            for q in range(EACH_PAGE):
                try:
                    a=cur_title[q]
                    v=cur_det[q]
                    color=GREEN if v[0] else WHITE
                    title=fonttextlar.render(a,True,color)
                    titlesize=title.get_size()
                    des=fonttext.render(v[1],True,color)
                    dessize=des.get_size()
                    title_pos=(ACHPIC_SIZE[0]+5,(ACHPIC_SIZE[1]-titlesize[1])//2+cury)
                    des_pos=(ACH_DES_START,(ACHPIC_SIZE[1]-dessize[1])//2+cury)
                    surf.blit(v[2],(0,cury))
                    surf.blit(title,title_pos)
                    surf.blit(des,des_pos)
                    cury+=ACHPIC_SIZE[1]+ACH_SEP
                except IndexError:break
            surfs.append(surf)
        return surfs
    def complete_ach(self,name:str):
        if not self.all_ach[name][0]:
            self.all_ach[name][0]=True
            get_profile()["achievements"].append(name)
def complete_c1():return get_profile()["unlock"][0]>1
def complete_c2():return get_profile()["unlock"][0]>2
def complete_c3():return get_profile()["unlock"][0]>3
def complete_c4():return get_profile()["unlock"][0]>4
def complete_c5():return get_profile()["unlock"][0]>5
def complete_c6():return get_profile()["unlock"][0]>6
def complete_c7():return get_profile()["unlock"][0]>7
def complete_c8():return get_profile()["unlock"][0]>8
def complete_c9():return get_profile()["unlock"][0]>9
def complete_c10():return get_profile()["unlock"][0]>10
def complete_c11():return get_profile()["unlock"][0]>11
def complete_c12():return get_profile()["unlock"][0]>12
def complete_c13():return get_profile()["unlock"][0]>13
def complete_c14():return get_profile()["unlock"][0]>14
def perfect_c1():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 1:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c2():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 2:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c3():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 3:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c4():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 4:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c5():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 5:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c6():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 6:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c7():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 7:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c8():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 8:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c9():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 9:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c10():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 10:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c11():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 11:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c12():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 12:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c13():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 13:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_c14():
    to_perfect=list(range(1,11))
    for perf in get_profile()["perfection"]:
        if perf[0] == 14:
            try:to_perfect.remove(perf[1])
            except:...
    return len(to_perfect) == 0
def perfect_any():return len(get_profile()["perfection"]) != 0
def perfect_all():
    for f in (perfect_c1,perfect_c2,perfect_c3,perfect_c4,perfect_c5,perfect_c6,perfect_c7,perfect_c8,perfect_c9,perfect_c10):
        if not f():
            get_profile()["all-perf"]=False
            return False
    get_profile()["all-perf"]=True
    return True
def weakbox_dest10():return get_profile()["weakbox-destroy"] >= 10
def finish_gallery():return get_profile()["finish-gallery"]
def tele_warp():return get_profile()["tele-warp"]
def warp_warp():return get_profile()["warp-warp"]
def is_hidden_level():return get_profile()["progress"][0] == 0
def whereseverybody():return get_profile()["wheres"]
def noway():return get_profile()["noway"]
def outoflimits():return get_profile()["outoflimits"]
check_profile()
load_profile()
achs=ach()
if lang == "en":
    achs.add_ach("Newcomer","Complete Chapter 1",pic_box,complete_c1)
    achs.add_ach("Boxes As You See","Complete Chapter 2",pic_bluebox,complete_c2)
    achs.add_ach("Cooperate","Complete Chapter 3",pic_cyan,complete_c3) 
    achs.add_ach("Assembly Line","Complete Chapter 4",pic_convright,complete_c4)
    achs.add_ach("A Good Learner","Complete Chapter 5",pic_ques,complete_c5)
    achs.add_ach("Dark Swirl","Complete Chapter 6",pic_warp,complete_c6)
    achs.add_ach("Into the Zone","Complete Chapter 7",pic_greenwarp,complete_c7)
    achs.add_ach("Dangerous Driving","Complete Chapter 8",pic_ice,complete_c8)
    achs.add_ach("Leaves' Dance","Complete Chapter 9",pic_leaf,complete_c9)
    achs.add_ach("The End?","Complete Chapter 10",pic_quesgr,complete_c10)
    achs.add_ach("Piece of Cake","Complete all Chapter 1 levels perfectly",pic_box,perfect_c1)
    achs.add_ach("This then That","Complete all Chapter 2 levels perfectly",pic_bluebox,perfect_c2)
    achs.add_ach("My Good Mate","Complete all Chapter 3 levels perfectly",pic_cyan,perfect_c3)
    achs.add_ach("Don't Hide Under a Box","Complete all Chapter 4 levels perfectly",pic_convleft,perfect_c4)
    achs.add_ach("Planning Ahead","Complete all Chapter 5 levels perfectly",pic_ques,perfect_c5)
    achs.add_ach("Magician","Complete all Chapter 6 levels perfectly",pic_warp,perfect_c6)
    achs.add_ach("Portal","Complete all Chapter 7 levels perfectly",pic_greenwarp,perfect_c7)
    achs.add_ach("Utter Freeze","Complete all Chapter 8 levels perfectly",pic_ice,perfect_c8)
    achs.add_ach("Golden Fall","Complete all Chapter 9 levels perfectly",pic_leaf,perfect_c9)
    achs.add_ach("Conqueror","Complete all Chapter 10 levels perfectly",pic_quesgr,perfect_c10)
    achs.add_ach("Perfect!","Complete a level perfectly",pic_p,perfect_any)
    achs.add_ach("Completionist","Complete all serie 1 (chapter 1 - 10) levels perfectly",pic_p,perfect_all)
    achs.add_ach("Out of Limits","Complete a level with steps fewer than perfect steps",pic_p,outoflimits)
    achs.add_ach("Where's Everybody?","Kill all players then fail a level",pic_spike,whereseverybody)
    achs.add_ach("No Way","Attempt to open a locked level",pic_cross,noway)
    achs.add_ach("Crack!","Destroy 10 or more weakboxes",pic_weakbox,weakbox_dest10)
    achs.add_ach("Operation Order","Discover the rule of conveyors and warps",pic_warp,tele_warp)
    achs.add_ach("But Nothing Special Happens","Find a point when a warp touches a greenwarp",pic_greenwarp,warp_warp)
    achs.add_ach("Finish Gallery","See through all pictures",pic_greendog,finish_gallery)
    achs.add_ach("Dogs Are Cute","The truth of dogs",pic_empty,None)
    achs.add_ach("Hooked","Complete Chapter 11",pic_hookbox,complete_c11)
    achs.add_ach("Dummy Danger","Complete Chapter 12",pic_antidest,complete_c12)
    achs.add_ach("And...Click!","Complete Chapter 13",pic_lock,complete_c13)
    achs.add_ach("Yet Released","Complete all Chapter 11 levels perfectly",pic_hookbox,perfect_c11)
    achs.add_ach("Cyantist","Complete all Chapter 12 levels perfectly",pic_antidest,perfect_c12)
    achs.add_ach("What I Called Precision","Complete all Chapter 13 levels perfectly",pic_key,perfect_c13)
    achs.add_ach("It's Fake!","Find a hidden level",pic_wall,is_hidden_level)
elif lang == "zh-cn":
    achs.add_ach("新人","完成章节1",pic_box,complete_c1)
    achs.add_ach("可视箱","完成章节2",pic_bluebox,complete_c2)
    achs.add_ach("合作","完成章节3",pic_cyan,complete_c3) 
    achs.add_ach("流水线","完成章节4",pic_convright,complete_c4)
    achs.add_ach("好学的人","完成章节5",pic_ques,complete_c5)
    achs.add_ach("黑暗漩涡","完成章节6",pic_warp,complete_c6)
    achs.add_ach("来回往返","完成章节7",pic_greenwarp,complete_c7)
    achs.add_ach("危险驾驶","完成章节8",pic_ice,complete_c8)
    achs.add_ach("叶之舞","完成章节9",pic_leaf,complete_c9)
    achs.add_ach("结局？","完成章节10",pic_quesgr,complete_c10)
    achs.add_ach("小菜一碟","完美完成章节1",pic_box,perfect_c1)
    achs.add_ach("按序操作","完美完成章节2",pic_bluebox,perfect_c2)
    achs.add_ach("好伙计","完美完成章节3",pic_cyan,perfect_c3)
    achs.add_ach("别藏箱子下面","完美完成章节4",pic_convleft,perfect_c4)
    achs.add_ach("提前规划","完美完成章节5",pic_ques,perfect_c5)
    achs.add_ach("魔法师","完美完成章节6",pic_warp,perfect_c6)
    achs.add_ach("传送门","完美完成章节7",pic_greenwarp,perfect_c7)
    achs.add_ach("严寒","完美完成章节8",pic_ice,perfect_c8)
    achs.add_ach("金秋","完美完成章节9",pic_leaf,perfect_c9)
    achs.add_ach("征服者","完美完成章节10",pic_quesgr,perfect_c10)
    achs.add_ach("完美！","完美完成任意关卡",pic_p,perfect_any)
    achs.add_ach("完成主义者","完美完成系列1（章节1-10）",pic_p,perfect_all)
    achs.add_ach("超出限制","以少于完美的步数完成一关",pic_p,outoflimits)
    achs.add_ach("大家都去哪了？","杀死所有玩家，并失败",pic_spike,whereseverybody)
    achs.add_ach("没门","尝试打开一个未解锁的关卡",pic_cross,noway)
    achs.add_ach("咔!","摧毁10个以上的弱箱",pic_weakbox,weakbox_dest10)
    achs.add_ach("操作次序","发现传送带与扭曲的规律",pic_warp,tele_warp)
    achs.add_ach("但是什么都没发生！","找到扭曲与绿色扭曲互动的时刻",pic_greenwarp,warp_warp)
    achs.add_ach("看完画廊","看过每一张图片",pic_greendog,finish_gallery)
    achs.add_ach("Dogs Are Cute","狗的真相",pic_empty,None)
    achs.add_ach("上钩","完成章节11",pic_hookbox,complete_c11)
    achs.add_ach("纸老虎","完成章节12",pic_antidest,complete_c12)
    achs.add_ach("然后……开！","完成章节13",pic_lock,complete_c13)
    achs.add_ach("又释放","完美完成章节11",pic_hookbox,perfect_c11)
    achs.add_ach("Cyantist","完美完成章节12",pic_antidest,perfect_c12)
    achs.add_ach("我称这个为“准确”","完美完成章节13",pic_key,perfect_c13)
    achs.add_ach("是假的！","找到一个隐藏关",pic_wall,is_hidden_level)