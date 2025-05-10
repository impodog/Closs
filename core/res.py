import pygame
from .const import*
from .save import*
import PygameCrew as pycr
import sys,os
font=pygame.font.SysFont("Courier",15)
check_profile()
load_profile()
lang=get_profile()["language"]
if lang == "en":
    fonttext=pygame.font.SysFont("Calibri",25)
    fonttextlar=pygame.font.SysFont("Calibri",40)
    fonttextsuper=pygame.font.SysFont("Calibri",60)
    fontlar=pygame.font.SysFont("Courier",40)   
elif lang == "zh-cn":
    fonttext=pygame.font.SysFont("NSimSun",25)
    fonttextlar=pygame.font.SysFont("NSimSun",40)
    fonttextsuper=pygame.font.SysFont("NSimSun",60)
    fontlar=pygame.font.SysFont("SimHei",40)  
pic_empty=pygame.Surface(EMPTY_SIZE)
pic_empty.fill(WHITE)
pic_empty.set_alpha(30)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', '/'.join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split('\\')[:-1]))
    return base_path+'/'+relative_path
class get_respath():
    def __init__(self,rel:str):self.rel=rel
    def __mod__(self,p:str):return resource_path(self.rel%p)
RES=get_respath("resource/%s")
GALLERY=get_respath("gallery/%s")
LEVEL=get_respath("level/c%d/%d.lev")
LEVELROOT=get_respath("level/%s")
pic_cyan=pygame.Surface(CYAN_SIZE)
pic_cyan.fill(CYAN)

pic_box=pygame.image.load(RES%"box.png").convert()
pic_box.set_colorkey(WHITE)
box_size=pic_box.get_size()
pygame.display.set_icon(pic_box)

pic_bluebox=pygame.image.load(RES%"bluebox.png").convert()
pic_bluebox.set_colorkey(WHITE)
bluebox_size=pic_bluebox.get_size()

pic_wall=pygame.image.load(RES%"wall.jpg").convert()
wall_size=pic_wall.get_size()

pic_spike=pygame.image.load(RES%"spike.png").convert()
pic_spike.set_colorkey(WHITE)
spike_size=pic_spike.get_size()

pic_weakbox=pygame.image.load(RES%"weakbox.png").convert()
pic_weakbox.set_colorkey(WHITE)
weakbox_size=pic_weakbox.get_size()

pic_convup=pygame.image.load(RES%"conv_up.png").convert()
pic_convup.set_colorkey(WHITE)
conv_size=pic_convup.get_size()
pic_convdown=pygame.transform.rotate(pic_convup,180)
pic_convleft=pygame.transform.rotate(pic_convup,90)
pic_convright=pygame.transform.rotate(pic_convup,-90)

pic_warp=pygame.image.load(RES%"warp.png").convert()
pic_warp.set_colorkey(WHITE)
warp_size=pic_warp.get_size()

pic_greenwarp=pygame.image.load(RES%"greenwarp.png").convert()
pic_greenwarp.set_colorkey(WHITE)
greenwarp_size=pic_greenwarp.get_size()

pic_ice=pygame.image.load(RES%"ice.png").convert()
pic_ice.set_colorkey(WHITE)
pic_ice.set_alpha(100)
ice_size=pic_ice.get_size()

pic_crusher=pygame.image.load(RES%"crusher.png").convert()
pic_crusher.set_colorkey(WHITE)
crusher_size=pic_crusher.get_size()

pic_leaf=pygame.image.load(RES%"leaf.png").convert()
pic_leaf.set_colorkey(WHITE)
leaf_size=pic_leaf.get_size()

pic_switchup=pygame.image.load(RES%"switch.png").convert()
pic_switchup.set_colorkey(WHITE)
switch_size=pic_switchup.get_size()

pic_hookbox=pygame.image.load(RES%"hookbox.png").convert()
pic_hookbox.set_colorkey(WHITE)
hookbox_size=pic_hookbox.get_size()

pic_key=pygame.image.load(RES%"key.png").convert()
pic_key.set_colorkey(WHITE)
key_size=pic_key.get_size()

pic_lock=pygame.image.load(RES%"lock.png").convert()
pic_lock.set_colorkey(WHITE)
lock_size=pic_lock.get_size()

pic_lasergun_down=pygame.image.load(RES%"lasergun.png").convert()
pic_lasergun_down.set_colorkey(WHITE)
lasergun_size=pic_lasergun_down.get_size()
pic_lasergun_left=pygame.transform.rotate(pic_lasergun_down,-90)
pic_lasergun_right=pygame.transform.rotate(pic_lasergun_down,90)
pic_lasergun_up=pygame.transform.rotate(pic_lasergun_down,180)

pic_fixed_lasergun_down=pygame.image.load(RES%"fixed_lasergun.png").convert()
pic_fixed_lasergun_down.set_colorkey(WHITE)
pic_fixed_lasergun_up=pygame.transform.rotate(pic_fixed_lasergun_down,180)
pic_fixed_lasergun_left=pygame.transform.rotate(pic_fixed_lasergun_down,-90)
pic_fixed_lasergun_right=pygame.transform.rotate(pic_fixed_lasergun_down,90)

pic_laser_down=pygame.image.load(RES%"laser.png").convert()
pic_laser_down.set_colorkey(WHITE)
laser_size=pic_laser_down.get_size()
pic_laser_left=pygame.transform.rotate(pic_laser_down,90)
pic_laser_up=pygame.transform.rotate(pic_laser_down,180)
pic_laser_right=pygame.transform.rotate(pic_laser_down,-90)
pic_laser_upflip=pygame.transform.flip(pic_laser_up,True,False)
pic_laser_downflip=pygame.transform.flip(pic_laser_down,True,False)
pic_laser_leftflip=pygame.transform.flip(pic_laser_left,False,True)
pic_laser_rightflip=pygame.transform.flip(pic_laser_right,False,True)

pic_switchdown=pygame.transform.rotate(pic_switchup,180)
pic_switchleft=pygame.transform.rotate(pic_switchup,90)
pic_switchright=pygame.transform.rotate(pic_switchup,-90)

pic_reflector_left=pygame.image.load("resource/reflector.png").convert()
pic_reflector_left.set_colorkey(WHITE)
reflector_size=pic_reflector_left.get_size()
pic_reflector_up=pygame.transform.rotate(pic_reflector_left,-90)
pic_reflector_right=pygame.transform.rotate(pic_reflector_left,180)
pic_reflector_down=pygame.transform.rotate(pic_reflector_left,90)
pic_reflector_lighted_left=pygame.image.load("resource/reflector_lighted.png").convert()
pic_reflector_lighted_left.set_colorkey(WHITE)
pic_reflector_lighted_up=pygame.transform.rotate(pic_reflector_lighted_left,-90)
pic_reflector_lighted_right=pygame.transform.rotate(pic_reflector_lighted_left,180)
pic_reflector_lighted_down=pygame.transform.rotate(pic_reflector_lighted_left,90)

pic_ques=pygame.image.load(RES%"ques.png").convert()
pic_ques.set_colorkey(WHITE)

pic_quesgr=pygame.image.load(RES%"quesgr.png").convert()
pic_quesgr.set_colorkey(WHITE)

pic_p=pygame.image.load(RES%"p.png").convert()
pic_p.set_colorkey(WHITE)

pic_arrow=pygame.image.load(RES%"arrow.png").convert()
pic_arrow.set_colorkey(BLACK)

pic_cross=pygame.image.load(RES%"cross.png").convert()
pic_cross.set_colorkey(WHITE)

pic_none=pygame.Surface((1,1))
pic_none.set_colorkey(BLACK)

pic_antidest=font.render("ANTI",True,RED)

CONVEYOR_DIRS={
    UP:pic_convup,
    DOWN:pic_convdown,
    LEFT:pic_convleft,
    RIGHT:pic_convright
}
SWITCH_DIRS={
    UP:pic_switchup,
    DOWN:pic_switchdown,
    LEFT:pic_switchleft,
    RIGHT:pic_switchright
}
LASERGUN_DIRS={
    UP:pic_lasergun_up,
    DOWN:pic_lasergun_down,
    LEFT:pic_lasergun_left,
    RIGHT:pic_lasergun_right
}
LASER_DIRS={
    UP:pic_laser_up,
    DOWN:pic_laser_down,
    LEFT:pic_laser_left,
    RIGHT:pic_laser_right
}
LASER_FLIPPED_DIRS={
    UP:pic_laser_upflip,
    DOWN:pic_laser_downflip,
    LEFT:pic_laser_leftflip,
    RIGHT:pic_laser_rightflip
}
FIXED_LASERGUN_DIRS={
    UP:pic_fixed_lasergun_up,
    DOWN:pic_fixed_lasergun_down,
    LEFT:pic_fixed_lasergun_left,
    RIGHT:pic_fixed_lasergun_right
}
REFLECTOR_DIRS={
    UP:pic_reflector_up,
    DOWN:pic_reflector_down,
    LEFT:pic_reflector_left,
    RIGHT:pic_reflector_right
}
REFLECTOR_LIGHTED_DIRS={
    UP:pic_reflector_lighted_up,
    DOWN:pic_reflector_lighted_down,
    LEFT:pic_reflector_lighted_left,
    RIGHT:pic_reflector_lighted_right
}
def trans_laser(d:"dict[tuple[int,int],pygame.Surface]")->dict:
    res=dict()
    for dir,surf in d.items():
        newsurf=pycr.ReplaceColor(surf,LASER_COLOR,LASERTRANS_COLOR)
        newsurf.set_colorkey(WHITE)
        res[dir]=newsurf
    return res
LASERGUNTRANS_DIRS=trans_laser(LASERGUN_DIRS)
FIXED_LASERGUNTRANS_DIRS=trans_laser(FIXED_LASERGUN_DIRS)
LASERTRANS_DIRS=trans_laser(LASER_DIRS)
LASERTRANS_FLIPPED_DIRS=trans_laser(LASER_FLIPPED_DIRS)
REFLECTOR_LIGHTEDTRANS_DIRS=trans_laser(REFLECTOR_LIGHTED_DIRS)

if lang == "en":
    pic_youwin=fontlar.render("You Win! Press Enter/Return to continue.",True,GREEN)
    pic_perfect=fontlar.render("You got perfect steps on this level!!!",True,GREEN)
    pic_gotperfect=fontlar.render("You've already got perfect steps on this level!",True,GREEN)
    pic_avalevel=fontlar.render("You have't got perfect on this level yet. Enter/Return to start",True,CYAN)
    pic_continue=fontlar.render("Continue playing from your unlock progress",True,WHITE)
    pic_invlevel=fontlar.render("Level does not exist.",True,RED)
    pic_unknown=fontlar.render("Unknown level format",True,LIGHTRED)
    pic_truelevel=fontlar.render("You haven't unlocked this level yet",True,YELLOW)
    pic_nowgo=fontlar.render("Now, go!",True,GREEN)
    pic_secret=fontlar.render("You found a secret...",True,WHITE)
    pic_perferences=fonttextlar.render("Restart the game for the preferences to take effect.",True,WHITE)
elif lang == "zh-cn":
    pic_youwin=fontlar.render("你赢了！按Enter/Return继续",True,GREEN)
    pic_perfect=fontlar.render("你达成了这关的完美步数！！！",True,GREEN)
    pic_gotperfect=fontlar.render("你已经拿到这关的完美步数了！",True,GREEN)
    pic_avalevel=fontlar.render("你还没拿到完美步数，按Enter/Return开始",True,CYAN)
    pic_continue=fontlar.render("从你的通关进度继续",True,WHITE)
    pic_invlevel=fontlar.render("关卡不存在",True,RED)
    pic_unknown=fontlar.render("未知的关卡格式",True,LIGHTRED)
    pic_truelevel=fontlar.render("你还没有解锁这关",True,YELLOW)
    pic_nowgo=fontlar.render("现在，开始！",True,GREEN)
    pic_secret=fontlar.render("你找到了一个秘密……",True,WHITE)
    pic_perferences=fonttextlar.render("重启游戏以改变偏好设置",True,WHITE)
pic_pref_size=pic_perferences.get_size()
pic_pref_pos=(SCR_LENGTH-pic_pref_size[0])//2,SCR_WIDTH-pic_pref_size[1]
tp_info=pycr.text_part((10,10),INFO_STRING,30,WHITE)

gal_sudo=pygame.image.load(GALLERY%"sudo.png").convert()
gal_doggy=pygame.image.load(GALLERY%"doggy.png")
gal_secretchange=pygame.image.load(GALLERY%"secretchange.png").convert()
gal_rc3=pygame.image.load(GALLERY%"rc3.png").convert()
gal_convdown=pygame.image.load(GALLERY%"convdown.png").convert()
gal_4_6=pygame.image.load(GALLERY%"4-6.png").convert()
gal_leavesgo=pygame.image.load(GALLERY%"leavesgo.png").convert()
gal_arrow=pygame.image.load(GALLERY%"arrow.png").convert()
gal_firstcyan=pygame.image.load(GALLERY%"firstcyan.png").convert()
gal_dogs_cute=pygame.image.load(GALLERY%"dogs-cute.png").convert()
gal_greendog=pygame.image.load(GALLERY%"greendog.png").convert()
gal_2dog=pygame.image.load(GALLERY%"2dog.png")
gal_clossin=pygame.image.load(GALLERY%"clossin.png").convert()
gal_generator=pygame.image.load(GALLERY%"generator.png").convert()
gal_newfile=pygame.image.load(GALLERY%"newfile.png").convert()
gal_c10rule=pygame.image.load(GALLERY%"c10rule.png").convert()
gal_levelcodes=pygame.image.load(GALLERY%"levelcodes.png").convert()
gal_firstspike=pygame.image.load(GALLERY%"firstspike.png").convert()
gal_dog=pygame.image.load(GALLERY%"dog.jpg").convert()

pic_greendog=gal_greendog.copy()
pic_greendog.set_colorkey(WHITE)