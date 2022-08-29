import pygame
from .const import*
import PygameCrew as pycr
import sys,os
font=pygame.font.SysFont("Courier",15)
fonttext=pygame.font.SysFont("Calibri",25)
fonttextlar=pygame.font.SysFont("Calibri",40)
fontlar=pygame.font.SysFont("Courier",40)
fonttextsuper=pygame.font.SysFont("Calibri",60)
pic_empty=pygame.Surface(EMPTY_SIZE)
pic_empty.fill(WHITE)
pic_empty.set_alpha(30)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
    return os.path.join(base_path, relative_path)
class get_respath():
    def __init__(self,rel:str):self.rel=rel
    def __mod__(self,p:str):return resource_path(self.rel%p)
RES=get_respath("resource\\%s")
GALLERY=get_respath("gallery\\%s")
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
pic_switchdown=pygame.transform.rotate(pic_switchup,180)
pic_switchleft=pygame.transform.rotate(pic_switchup,90)
pic_switchright=pygame.transform.rotate(pic_switchup,-90)

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
pic_youwin=fontlar.render("You Win! Press Enter/Return to continue.",True,GREEN)
pic_perfect=fontlar.render("You got perfect steps on this level!!!",True,GREEN)
pic_gotperfect=fontlar.render("You've already got perfect steps on this level!",True,GREEN)
pic_avalevel=fontlar.render("You have't got perfect on this level yet. Enter/Return to start",True,CYAN)
pic_continue=fontlar.render("Continue playing from your unlock progress",True,WHITE)
pic_invlevel=fontlar.render("Level does not exist.",True,RED)
pic_unknown=fontlar.render("Unknown level format",True,LIGHTRED)
pic_truelevel=fontlar.render("You haven't unlocked this level yet",True,YELLOW)
pic_nowgo=fontlar.render("Now, go!",True,GREEN)
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