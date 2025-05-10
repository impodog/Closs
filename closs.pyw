from core import*
import calca.pysp as pysp
BUTSIZE=(200,100)
levelname_checker=pysp.SubType(list,(int,int))
def get_website():return "http://dogsocute.icu/game/Closs/solution/c%d/%d.html"%tuple(get_profile()["progress"])
def is_avalevel(string:str):return levelname_checker.check(string) and len(string) == 2 and string <= get_profile()["unlock"]
def is_truelevel(string:str):return levelname_checker.check(string) and len(string) == 2
def get_nextperf()->"list[int,int]":
    ls_perf=get_profile()["perfection"]
    for chapter in range(1,11):
        for levnum in range(1,11):
            levname=[chapter,levnum]
            if levname not in ls_perf:return levname
    return None
def get_pagenum_str(page:int,max:int):
    if lang == "en":return "Page %d / %d    Left/Right to Switch    ESC to Quit"%(page,max)
    elif lang == "zh-cn":return "页数 %d / %d    左/右键切换    按ESC退出"%(page,max)
def twice(string:str):return (string,string)
def pref_lang()->str:return "language:"+LANG_AND_NAME[get_profile()["language"]]
def get_steps_str(used:int,perf:int=None):
    if perf is None:
        if lang == "en":return "Steps Used %d"%used
        elif lang == "zh-cn":return "步数 %d"%used
    else:
        if lang == "en":return "Steps Used %d / %d"%(used,perf)
        elif lang == "zh-cn":return "步数 %d / %d"%(used,perf)
def main():
    key.init()
    key.level=get_profile()["progress"]
    but_newgame=pycr.button((0,0),(200,100),("New Game","New Game"))
    but_continue=pycr.button((0,0),(200,100),("Continue","Continue"))
    but_choose=pycr.button((200,0),(400,100),("Play Previous","Play Previous"))
    but_ach=pycr.button((400,0),(600,100),("Achievements","Achievements"))
    but_info=pycr.button((600,0),(800,100),("Information","Information"))
    but_gallary=pycr.button((800,0),(1000,100),("Gallery","Gallery"))
    but_preferences=pycr.button((0,100),(200,200),("Preferences","Preferences"))
    but_quit=pycr.button((200,100),(400,200),("Quit","Quit"))
    but_startnext=pycr.button((1200,0),(1400,100),("Start the Sequel","Start the Sequel"))
    ipt_choose=pycr.inputbox((0,0),(1000,100),limit=10,default_text="Type Level Code    Examples: 1-2 2-8    ESC to quit",textsize=40,terminate_on_return=True)
    txt_unlocked:pygame.Surface=None
    txt_playing:pygame.Surface=None
    is_secondplay:bool=False
    perfect:int=None
    ach_page:int=1
    ach_max:int=0
    txt_next_level:pygame.Surface=None
    last_has_player:bool=True
    has_player:bool=True
    ach_pagenum:pygame.Surface=None
    ach_surf:"list[pygame.Surface]"=None
    gal_pagenum:pygame.Surface=None
    gal_page:int=1
    gal_max:int=0
    gal_surf:"list[pygame.Surface]"=None
    buts_pref:"list[pycr.button]"=None
    is_secondperfect:bool=False
    PREFERENCES=(pref_lang,)
    choose=0
    def start_keylevel():
        nonlocal txt_unlocked,txt_playing,choose,perfect,is_secondplay,is_secondperfect,has_player,last_has_player,txt_next_level
        txt_next_level=txt_unlocked=txt_playing=None
        last_has_player=True
        has_player=True
        choose=0
        key.level=get_profile()["progress"]
        compile_level(key.level)
        perfect=get_lo().perfect_steps
        is_secondplay=get_profile()["progress"]<get_profile()["unlock"]
        is_secondperfect=get_profile()["progress"] in get_profile()["perfection"]
        key.game=True
    get_profile()["all-perf"]=perfect_all()
    while key.loop:
        screen.fill(BLACK)
        pycr.PyCr_Value.get_interact()
        for event in pycr.PyCr_Value.event:
            if event.type == pygame.QUIT:key.end()
            elif event.type == pygame.KEYDOWN:
                if pycr.PyCr_Value.mod & pygame.KMOD_ALT:
                    if pycr.PyCr_Value.key == pygame.K_F4:key.end()
                elif pycr.PyCr_Value.key == pygame.K_r and key.game:
                    compile_level(key.level)
                elif pycr.PyCr_Value.key == pygame.K_ESCAPE:
                    if choose != 0:choose=0
                    ach_surf=None
                    buts_pref=None
                    key.init()
                elif pycr.PyCr_Value.key == pygame.K_RETURN and choose != 1:
                    key.init()
                    start_keylevel()
                elif pycr.PyCr_Value.key == pygame.K_LEFT:
                    if choose == 2:
                        if ach_page>1:ach_page-=1
                    elif choose == 4:
                        if gal_page>1:gal_page-=1
                elif pycr.PyCr_Value.key == pygame.K_RIGHT:
                    if choose == 2:
                        if ach_page<ach_max:ach_page+=1
                    elif choose == 4:
                        if gal_page<gal_max:
                            gal_page+=1
                            if gal_page == gal_max:
                                get_profile()["finish-gallery"]=True
        if key.game:    
            if get_lo().is_winning:
                if get_lo().direct_win:screen.blit(pic_secret,(5,0))
                else:
                    if perfect is not None and get_lo().steps_used<=perfect and is_secondplay:
                        key.has_perfect=True
                        get_profile()["perfection"].append(key.level)
                        if get_lo().steps_used<perfect:get_profile()["outoflimits"]=True
                    get_profile()["progress"]=get_lo().next_level
                    levelname=get_lo().next_level
                    if levelname is not None and levelname > get_profile()["unlock"]:
                        get_profile()["unlock"]=levelname
                    if key.has_perfect:screen.blit(pic_perfect,(5,50))
                    screen.blit(pic_youwin,(5,0))
            else:
                if pycr.PyCr_Value.key in PLAYER_KEYS:
                    has_player=False
                    for aobj in get_lo().objs.copy():
                        for lobj in aobj.copy():
                            for obj in lobj.copy():
                                if obj not in get_lo().moved:
                                    if isinstance(obj,player):
                                        has_player=True
                                        obj.run(pycr.PyCr_Value.key)
                    if not has_player and not last_has_player:get_profile()["wheres"]=True
                    last_has_player=has_player
                    if get_lo().player_activity:
                        for aobj in get_lo().objs.copy():
                            for lobj in aobj.copy():
                                for obj in lobj.copy():
                                    obj.detectpre()#pre-movements
                        for aobj in get_lo().objs.copy():
                            for lobj in aobj.copy():
                                for obj in lobj.copy():
                                    obj.detect()#movements
                        for aobj in get_lo().objs.copy():
                            for lobj in aobj.copy():
                                for obj in lobj.copy():
                                    obj.detect2()#add/remove objects
                        for aobj in get_lo().objs.copy():
                            for lobj in aobj.copy():
                                for obj in lobj.copy():
                                    obj.final_detect()#signals
                        get_lo().steps_used+=1   
                    get_lo().refresh()
                    get_lo().check_winning()
                screen.blit(get_lo().background,get_lo().background_start)   
                for aobj in get_lo().objs:
                    for lobj in aobj:
                        for obj in lobj:
                            pycr.put(obj)
                used=get_lo().steps_used
                screen.blit(get_lo().old_foreground,get_lo().background_start)
                if perfect is not None and is_secondplay:
                    if used<perfect-1:steps_color=CYAN
                    elif used<perfect:steps_color=YELLOW
                    elif used==perfect:steps_color=GREEN
                    else:steps_color=RED
                    txt_steps=get_steps_str(used,perfect)
                else:
                    steps_color=WHITE
                    txt_steps=get_steps_str(used)
                surf_steps=fonttextlar.render(txt_steps,True,steps_color)
                steps_size=surf_steps.get_size()
                screen.blit(surf_steps,(SCR_LENGTH-steps_size[0],SCR_WIDTH-steps_size[1]))
                if get_lo().level_name_surf is not None:
                    screen.blit(get_lo().level_name_surf,get_lo().level_name_surf_pos)
        else:
            if choose == 0:
                if txt_unlocked is None and get_profile()["unlock"] != [1,1]:
                    if lang == "en":
                        txt_unlocked=fontlar.render("Progress Unlocked %d-%d"%tuple(get_profile()["unlock"]),True,WHITE)
                        txt_playing=fontlar.render("Current Level %d-%d"%tuple(get_profile()["progress"]),True,WHITE)
                    elif lang == "zh-cn":
                        txt_unlocked=fontlar.render("已解锁 %d-%d"%tuple(get_profile()["unlock"]),True,WHITE)
                        txt_playing=fontlar.render("当前关卡 %d-%d"%tuple(get_profile()["progress"]),True,WHITE)
                elif txt_next_level==None and get_profile()["unlock"][0]>=11:
                    nextperf=get_nextperf()
                    if nextperf is None:
                        if lang == "en":
                            if get_profile()["all-perf"]:txt_next_level=fontlar.render("You've solved serie 1 perfectly!",True,GREEN)
                            else:txt_next_level=fontlar.render("Check your achievements and go back here!",True,GREEN)
                        elif lang == "zh-cn":
                            if get_profile()["all-perf"]:txt_next_level=fontlar.render("你已完美完成系列1！",True,GREEN)
                            else:txt_next_level=fontlar.render("看看你的成就，再回来！",True,GREEN)
                    else:
                        if lang == "en":
                            txt_next_level=fontlar.render("Play %d-%d for Perfection"%tuple(nextperf),True,GREEN)
                        elif lang == "zh-cn":
                            txt_next_level=fontlar.render("接下来玩 %d-%d，获得完美"%tuple(nextperf),True,GREEN)
                if txt_next_level is not None:screen.blit(txt_next_level,(10,350))
                if txt_unlocked is None:
                    if pycr.put(but_newgame):start_keylevel()
                else:
                    screen.blit(txt_playing,(10,250))
                    screen.blit(txt_unlocked,(10,300))
                    if pycr.put(but_continue):start_keylevel()
                if pycr.put(but_choose):choose=1
                elif pycr.put(but_ach):choose=2
                elif pycr.put(but_info):choose=3
                elif pycr.put(but_preferences):choose=6
                elif pycr.put(but_quit):key.loop=False
                elif get_profile()["all-perf"] and pycr.put(but_gallary):choose=4
                elif get_profile()["unlock"] == [11,0] and pycr.put(but_startnext):choose=5
            elif choose == 1:
                result=pycr.put(ipt_choose)
                if result is None:
                    try:
                        sp=list(map(int,ipt_choose.inputing.split('-')))
                        if sp in get_profile()["perfection"]:
                            ipt_choose.colors=(pycr.WHITE,pycr.INPUTBOX_OUTLINE_GREY,GREEN)
                            screen.blit(pic_gotperfect,(5,100))
                        elif not os.path.exists(get_path(sp)): 
                            ipt_choose.colors=(pycr.WHITE,pycr.INPUTBOX_OUTLINE_GREY,RED)
                            screen.blit(pic_invlevel,(5,100))
                        elif is_avalevel(sp):
                            ipt_choose.colors=(pycr.WHITE,pycr.INPUTBOX_OUTLINE_GREY,CYAN)
                            if sp == get_profile()["unlock"]:screen.blit(pic_continue,(5,100))
                            else:screen.blit(pic_avalevel,(5,100))
                        elif is_truelevel(sp):
                            ipt_choose.colors=(pycr.WHITE,pycr.INPUTBOX_OUTLINE_GREY,YELLOW)
                            screen.blit(pic_truelevel,(5,100))
                        else:raise
                    except:
                        ipt_choose.colors=(pycr.WHITE,pycr.INPUTBOX_OUTLINE_GREY,BLACK)
                        screen.blit(pic_unknown,(5,100))
                else:
                    if result == "dogs-cute":achs.complete_ach("Dogs Are Cute")
                    try:
                        sp=list(map(int,result.split('-')))
                        if is_avalevel(sp) and os.path.exists(get_path(sp)):
                            screen.blit(pic_nowgo,(5,100))
                            get_profile()["progress"]=sp
                            start_keylevel()
                        elif is_truelevel(sp) and os.path.exists(get_path(sp)):
                            get_profile()["noway"]=True
                    except:...
            elif choose == 2:
                if ach_surf == None:
                    achs.parse_ach()
                    ach_surf=achs.generate_surf()
                    ach_max=len(ach_surf)
                screen.blit(ach_surf[ach_page-1],(0,0))
                ach_pagenum=fonttext.render(get_pagenum_str(ach_page,ach_max),True,WHITE)
                pagenum_size=ach_pagenum.get_size()
                screen.blit(ach_pagenum,((SCR_LENGTH-pagenum_size[0])//2,SCR_WIDTH-pagenum_size[1]))
            elif choose == 3:
                pycr.put(tp_info)
            elif choose == 4:
                if gal_surf == None:
                    gal_surf=generate_gallery()
                    gal_max=len(gal_surf)
                screen.blit(gal_surf[gal_page-1],(0,0))
                gal_pagenum=fonttext.render(get_pagenum_str(gal_page,gal_max),True,WHITE)
                pagenum_size=gal_pagenum.get_size()
                screen.blit(gal_pagenum,((SCR_LENGTH-pagenum_size[0])//2,SCR_WIDTH-pagenum_size[1]))
            elif choose == 5:
                choose=1
                get_profile()["unlock"]=get_profile()["progress"]=[11,1]
                key.init()
                start_keylevel()
            elif choose == 6:
                if buts_pref is None:
                    buts_pref=list()
                    curx,cury=0,0
                    for pref in PREFERENCES:
                        if pref != "":buts_pref.append(pycr.button((curx,cury),(curx+400,cury+100),twice(pref())))
                        cury+=100
                        if cury+100 > SCR_WIDTH:
                            curx+=400
                            cury=0
                for prefbut in buts_pref:
                    if pycr.put(prefbut):
                        txt=prefbut.text[0]
                        option=':'.join(txt.split(':')[1:])
                        if txt.startswith("language:"):
                            get_profile()["language"]=PREF_LANGS[(PREF_LANGS.index(get_profile()["language"])+1)%LANGLEN]
                        buts_pref=None
                        break
                screen.blit(pic_perferences,pic_pref_pos)
        pygame.display.flip()
        pycr.clock.tick(30)
if __name__ == "__main__":
    try:main()
    finally:save_profile()