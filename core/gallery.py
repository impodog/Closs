from .sol import*
from .save import*
gallery:"dict[str,tuple[pygame.Surface,str]]"={
    "Welcome":(pic_box,"Browse the pictures about or not about the game!"),
    "Doggy":(gal_doggy,"A cute doggy!!!!"),
    "Secret Change":(gal_secretchange,"No one's gonna know..."),
    "1.0.0rc3":(gal_rc3,"1.0.0rc3 info page"),
    "convdown":(gal_convdown,"First design of a conveyor. Now conveyors have brighter color and is facing up."),
    "4-6":(gal_4_6,"Earlier in the game, players got stuck together in this level due to dynamic deleting in a list."),
    "Sudo":(gal_sudo,"A meme about Linux & Tux."),
    "Leaves Go":(gal_leavesgo,"Early version achievement of completing chapter 9."),
    "Arrow":(gal_arrow,"A picture of an arrow. The first design of conveyors."),
    "First Cyan":(gal_firstcyan,"Red and Black, the first game whose players being a cyan rectangle."),
    "dogs-cute":(gal_dogs_cute,"What will this do?"),
    "Green Dog":(gal_greendog,"I drew this!"),
    "Generator":(gal_generator,"Source code of an empty level generator. (language : C)"),
    "Clossin":(gal_clossin,"Deserted shooting game where you can only move to your mouse direction with flashlight effect and a similar name to this game."),
    "New File":(gal_newfile,"How to create a new file with command again?????"),
    "2 Dog":(gal_2dog,"Dogs are qjut"),
    "Chapter 10 Rule":(gal_c10rule,"First massive use of rule and #define preprocessor line."),
    "Level Codes":(gal_levelcodes,"All analyze codes and their meanings."),
    "First Spike Design":(gal_firstspike,"The first design of spikes."),
    "Dog":(gal_dog,"Let's end with my favourite dog picture!!!")
}
def generate_gallery():
    pagenum=math.ceil(len(gallery))
    surfs=list()
    tup_title=tuple(gallery.keys())
    tup_det=tuple(gallery.values())
    for i in range(pagenum):
        surf=pygame.Surface((SCR_LENGTH,SCR_WIDTH))
        cur_title=tup_title[i]
        cur_det=tup_det[i]
        title=fonttextlar.render(cur_title,True,WHITE)
        titlesize=title.get_size()
        des=fonttext.render(cur_det[1],True,WHITE)
        dessize=des.get_size()
        picture=cur_det[0]
        pic_size=list(picture.get_size())
        trans=1
        if pic_size[0] > SCR_LENGTH:trans=SCR_LENGTH/pic_size[0]
        if pic_size[1] > GAL_TITLEY:
            scale=GAL_TITLEY/pic_size[1]
            if scale < trans:trans=scale
        pic_size[0]*=trans
        pic_size[1]*=trans
        picture=pygame.transform.scale(picture,pic_size)
        title_pos=((SCR_LENGTH-titlesize[0])//2,GAL_TITLEY)
        des_pos=((SCR_LENGTH-dessize[0])//2,GAL_TEXTY)
        pic_pos=((SCR_LENGTH-pic_size[0])//2,(GAL_TITLEY-pic_size[1])//2)
        surf.blit(picture,pic_pos)
        surf.blit(title,title_pos)
        surf.blit(des,des_pos)
        surfs.append(surf)
    return surfs