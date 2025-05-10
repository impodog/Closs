import pygame,math
import calca.pysp as pysp
__version__="1.1.0dev4.0"
__release_date__="9/24/2022"
CLL_VERSION="1"
GAME_VERSION=__version__
SCR_LENGTH=1680
SCR_WIDTH=945
CYAN=(0,255,234)
WHITE=(255,255,255)
BLACK=(0,0,0)
CYAN_SIZE=(30,30)
EMPTY_SIZE=(50,50)
PURPLE=(200,0,200)
BLUE=(0,100,255)
GREEN=(0,200,0)
YELLOW=(200,200,0)
RED=(200,0,0)
LIGHTRED=(255,100,100)
ACHPIC_SIZE=(50,50)
ACH_SEP=20
EACH_PAGE=math.floor((SCR_WIDTH-50)/(ACHPIC_SIZE[1]+ACH_SEP))
ACH_DES_START=600
GAL_TITLEY=800
GAL_TEXTY=850
UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)
NOGRAV=(0,0)
UNDEFINED_SIZE=(1,1)
LASER_COLOR=(50,111,177)
LASERTRANS_COLOR=(60,135,16)
LENGTH=55
EMPTY_START=(LENGTH-EMPTY_SIZE[0])//2
PLAYER_KEYS=(pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT)
dir_t = pysp.SubType(tuple,(int,int))
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
REP_SIGN_PATTERN = r"\\([\\"+'\\'.join(REP_SIGNS.keys())+"])"
LANG_AND_NAME={
    "en":"English",
    "zh-cn":"Chinese Simplified"
}
PREF_LANGS=tuple(LANG_AND_NAME.keys())
LANGLEN=len(PREF_LANGS)
INFO_STRING="""Closs Information
Version : %s
Release Date : %s

Press ESC to quit."""%(__version__,__release_date__)