from .sol import*
from .analyze import*
PATTERN_MULSPACE=r" [ ]+"
PATTERN_MULSTRING=r"\(([\w ]+)\*([\d]+)\)"
PATTERN_PLUS=r"\(([\d]+)\+([\d]+)\)"
PATTERN_MINUS=r"\(([\d]+)\-([\d]+)\)"
def get_mulstring(match:re.Match):
    string=match.group(1)
    times=int(match.group(2))
    return ((string+" ")*times)[:-1]
def get_plus(match:re.Match):
    a=int(match.group(1))
    b=int(match.group(2))
    return str(a+b)
def get_minus(match:re.Match):
    a=int(match.group(1))
    b=int(match.group(2))
    return str(a-b)
def compile_level(levelname:"list[int,int]"):
    def get_decode_fstring(string:str,ind:"tuple[int,int]",separator:str):
        sec_namearg=string.split(separator)
        for p in range(len(sec_namearg)):
            try:sec_namearg[p]=get_decode(sec_namearg[p])
            except:
                try:
                    sec_namearg[p]=get_decode_fstring(sec_namearg[p],ind,'&')
                except:...
        t=sec_namearg[0]
        sec_arg=None
        if t is not empty:sec_arg = t((ind[0],ind[1]),*sec_namearg[1:])
        return sec_arg
    def decode_string(string:str,ind:"tuple[int,int]"):
        nonlocal warps,object_define
        namearg=string.split("<")
        for i in range(len(namearg)):
            try:namearg[i]=get_decode(namearg[i])
            except:
                try:
                    namearg[i]=get_decode_fstring(namearg[i],ind,'+')
                except:...
        t=namearg[0]
        try:
            if t is not empty:get_lo().objs[ind[1]][ind[0]].append(t((ind[0],ind[1]),*namearg[1:]))
            if isinstance(t,type) and issubclass(t,warptype):warps.append(get_lo().objs[ind[1]][ind[0]][-1])
        except TypeError:
            warnings.warn("(SKIPPED)unknown token '%s'"%t,UserWarning)
    levelpath=get_path(levelname)
    with open(levelpath,'r') as file:
        levstring=file.read()
    levstring=re.sub(PATTERN_MULSPACE,' ',levstring)
    lines=levstring.split('\n')
    preprocessline:"list[str]"=list()
    xlen=1
    rulestring=str()
    leveldir=os.path.dirname(levelpath)+"/"
    rulepath=(leveldir+"rule",leveldir+".rule","level/rule","level/.rule","level/std.rule")
    for rulename in rulepath:
        if os.path.exists(rulename):
            with open(rulename,'r') as rules:
                rulestring+=rules.read()+"\n"
    for line in rulestring.split('\n'):
        if not line.startswith("//"):
            if line.startswith(("#","$")):
                preprocessline.append("rule:"+line)
    for line in lines:
        if line.startswith(('#','$')):preprocessline.append(line)
        else:
            curlen=len(line.split(' '))
            if curlen > xlen:xlen=curlen
    for p in range(len(preprocessline)):
        pre=preprocessline[p]
        if pre.startswith("rule:"):preprocessline[p]=preprocessline[p][5:]
        else:lines.remove(pre)
    ylen=len(lines)
    create_lo()
    get_lo().init((xlen,ylen))
    linenum=0
    warps:"list[warp]"=list()
    replace:"dict[str,str]"=dict()
    object_define:"dict[str,FunctionType]"=dict()
    if get_lo().next_level is None:
        get_lo().next_level=levelname
    ppmode=0
    for pre in preprocessline:
        prams=pre.split(' ')
        aft=' '.join(prams[1:])
        if ppmode == 0:
            if pre.startswith("#next"):
                if len(aft) != 0:get_lo().next_level=list(map(int,aft.split('-')))
                else:
                    get_lo().next_level=levelname.copy()
                    get_lo().next_level[1]+=1
            elif pre.startswith("#perfect"):
                get_lo().perfect_steps=int(aft)
            elif pre.startswith("#defgrav"):
                get_lo().gravity=get_dirdecode(aft)
            elif pre.startswith("#define"):
                rep=unbsl_split(aft,':')
                replace[rep[0]]=rep[1]
    for line in lines:
        lsnum=0
        for _old,_new in replace.items():line=line.replace(_old,_new)
        line=line.replace("[len]",str(xlen))
        line=line.replace("[wid]",str(ylen))
        line=re.sub(PATTERN_PLUS,get_minus,line)
        line=re.sub(PATTERN_MINUS,get_plus,line)
        line=re.sub(PATTERN_MULSTRING,get_mulstring,line)
        for ls in line.split(' '):
            ls=rep_signs(ls)
            for name in ls.split(','):
                decode_string(name,(lsnum,linenum))
            lsnum+=1
        linenum+=1
    try:
        warps[-1].next=warps[0]
        for wi in range(len(warps)-1):
            warps[wi].next=warps[wi+1]
    except IndexError:...
    get_lo().init_winsigns()
    for aobj in get_lo().objs:
        for lobj in aobj:
            for obj in lobj:
                obj.analyze_parse()