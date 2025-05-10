from .sol import*
PATTERN_MULSPACE=r" [ ]+"
PATTERN_MULRETURN=r"\n[\n]+"
PATTERN_MULSTRING=r"\(([\w ]+)\*([\d]+)\)"
PATTERN_STRINGEND=r" \n"
PATTERN_PLUS=r"\(([\d]+)\+([\d]+)\)"
PATTERN_MINUS=r"\(([\d]+)\-([\d]+)\)"
PATTERN_TRAILSPACE=r"\n[ \t]+"
DIRECTION_DECODE={
    "up":UP,
    "dw":DOWN,
    "lt":LEFT,
    "rt":RIGHT
}
inlevel_images:"dict[str,pygame.Surface]"=dict()
def get_image(ind,name:str):
    result = inlevel_images.get(name)
    if result is None:printwarn(WarnTypes.error,"unknown image resource alias : %s"%name);return pic_none
    else:return result
CLASS_DECODE={
    "cy":cyan,
    "wa":wall,
    "bx":box,
    "--":empty,
    "ds":dest,
    "tx":text,
    "sp":spike,
    "bb":bluebox,
    "wk":weakbox,
    "cv":conveyor,
    "wp":warp,
    "gw":greenwarp,
    "ic":ice,
    "cr":crusher,
    "lf":leaf,
    "sw":switch,
    "nm":nameof,
    "hk":hookbox,
    "ad":antidest,
    "ky":ikey,
    "lk":lock,
    "wptp":warptype,
    "bxtp":boxtype,
    "pic":pictureof,
    "levsw":level_switcher,
    "dl":destroy_lasergun,
    "tl":transform_lasergun,
    "rf":reflector,
    "hd":hide,
    "in":instanceof,
    "getpic":getpicture,
    "none":getnone,
    "get_image":get_image
}
PYTHON_OBJECT_DECODE={
    "false":False,
    "true":True
}
decode_strs=dict()
decode_strs.update(DIRECTION_DECODE)
decode_strs.update(CLASS_DECODE)
decode_strs.update(PYTHON_OBJECT_DECODE)
ENCODE=invert(decode_strs)
SPLITHERE="[splithere]"
def get_decode(string:str):
    global decode_strs
    return decode_strs[string]
def refresh_decode():
    global decode_strs,warps
    decode_strs=dict()
    decode_strs.update(DIRECTION_DECODE)
    decode_strs.update(CLASS_DECODE)
    decode_strs.update(PYTHON_OBJECT_DECODE)
    warps=list()
def get_dirdecode(string:str):return DIRECTION_DECODE[string]
def rep_splithere(match:re.Match):return match.group(1)+SPLITHERE
def unbsl_split(string:str,s:str,repl:bool=True)->"list[str]":
    split =re.sub(r"([^\\])%s"%s,rep_splithere,string).split(SPLITHERE)
    if repl:
        for i in range(len(split)):
            split[i] = split[i].replace("\\"+s,s)
    return split
def pat_split(pattern:str,string:str)->"list[str]":return re.sub(pattern,rep_splithere,string).split(SPLITHERE)
temp_typedefcode=0
def get_next_temp()->str:
    global temp_typedefcode
    temp_typedefcode+=1
    return "_TMP%d"%temp_typedefcode
class TypeDef_Closs_Object:
    def __init__(self,cls:"type[Closs_Object]",args:"list[str]"):
        self.cls=cls
        self.args=args
    def __call__(self,ind:"tuple[int,int]",*args:"list[str]")->"Closs_Object":
        sargs=list()
        for a in self.args:
            if isinstance(a,TypeDef_Closs_Object):sargs.append(a(ind))
            else:sargs.append(a)
        return self.cls(ind,*sargs,*args)
def analyze_object(string:str):
    l=unbsl_split(string,'<')
    args=list()
    for s in l:
        if s.startswith('$'):
            args.append(re.sub(REP_SIGN_PATTERN,get_rep_sign,s[1:]))
        else:
            try:
                args.append(get_decode(s))
            except KeyError:
                args.append(re.sub(REP_SIGN_PATTERN,get_rep_sign,s))
    return args
class WarnTypes:
    error = "ERROR"
    warning = "WARNING"
    suggestion = "SUGGESTION"
warps:"list[warptype]"=list()
global_levelname:"list[int,int]"=None
global_path:str
def printwarn(warn_action:str,warn_msg:str):
    print("(%s)%s"%(warn_action,warn_msg))
def get_instance(string:str,index:"tuple[int,int]"):
    l=analyze_object(string)
    if l[0] is empty:return None
    try:
        obj=l[0](index,*l[1:])
        if isinstance(l[0],type) and issubclass(l[0],warptype):
            warps.append(obj)
        return obj
    except:
        printwarn(WarnTypes.error,"unhandled error due to object : '%s'"%string)
        traceback.print_exc()
def analyze_line(string:str,linenum:int):
    l=string.split(' ')
    line=list()
    for i in range(len(l)):
        parts = unbsl_split(l[i],',')
        line.append(list())
        for part in parts:
            instance=get_instance(part,(i,linenum))
            if instance is not None:line[i].append(instance)
    return line
def analyze_game(string:str):
    l=string.split('\n')
    objs=list()
    max_line_len=0
    for i in range(len(l)):
        line=analyze_line(l[i],i)
        length = len(line)
        if length > max_line_len:
            max_line_len=length
        objs.append(line)
    for line in objs:
        for i in range(max_line_len-len(line)):
            line.append(list())
    for line in objs:
        for list_obj in line:
            for obj in list_obj:
                obj.analyze_parse()
    return objs
def sub_excess(string:str):return re.sub(PATTERN_STRINGEND,'\n',re.sub(PATTERN_TRAILSPACE,'\n',re.sub(PATTERN_MULSPACE,' ',re.sub(PATTERN_MULRETURN,'\n',string))))
def split_filestring(string:str)->"list[str]":
    content1=sub_excess(string).split('\n')
    content2=list()
    for t in content1:content2.extend(unbsl_split(t,';'))
    return content2
def get_rule_and_game():
    global global_path
    rule_string=str()
    game_string=str()
    with open(global_path,'r',encoding="utf-8") as game:
        for line in split_filestring(game.read()):
            if line.startswith("#"):
                rule_string+=line+'\n'
            elif not line.startswith("//"):
                game_string+=line+'\n'
    return rule_string+"\n#import langs\n#import attr",game_string[:-1]
def get_rep_sign(match:re.Match):
    return REP_SIGNS[match.group(1)]
def is_obj_code(string:str):
    global ENCODE
    return ENCODE.get(string) is not None
def match_brackets(string:str,bracket_scheme:str="()"):
    value=0
    start,end=bracket_scheme
    result=str()
    ls_notbs=string[0] != '\\'
    for s in string:
        if ls_notbs:
            if s == start:value+=1
            elif s == end:
                value-=1
                if value == 0:return result[1:]
                elif value < 0:return None
        if value > 0:result+=s
        ls_notbs= s != '\\'
    return None
IF_STATEMENT=("if","ifdef","iflang","iflev","ifndef")
def is_statements(s:str,stm:"str|tuple[str]"):
    s = s.rstrip('*').rstrip('&')
    if isinstance(stm,str):return s == stm
    else:return s in stm
def analyze_rule(rule:str,game:str,levelname:str):
    global global_path,decode_strs,inlevel_images
    construle="#rawfile\n"
    def get_define(match:re.Match):
        nonlocal args
        return match.group(1)+args[1]+match.group(3)
    def get_import_arg(name:str,default=False):
        nonlocal filename,import_args
        try:
            get = import_args[filename].get(name)
            return default if get is None else get
        except NameError:
            return None
    def set_import_arg(name:str,value):
        nonlocal filename,import_args
        import_args[filename][name]=value
    def delete_import_arg(name:str):
        nonlocal filename,import_args
        import_args[filename].pop(name)
    def insert(line:str,rel_index=1):
        nonlocal linenum,pre_lines
        if rel_index < 1:
            printwarn(WarnTypes.error,"do NOT insert line before current line, it causes unexpected behaviors")
        else:
            pre_lines.insert(linenum+rel_index,line)
    def printwarn(warn_action:str,warn_msg:str,nestnum:int=1):
        nonlocal filename,is_raw_file
        if not is_raw_file:print("(%s in <%s>)%s"%(warn_action,get_import_nest_name(nestnum),warn_msg))
    def define_name(name:str):
        nonlocal defined
        defined.add(name)
    def add_line_to_const():
        nonlocal line,construle,may_add_line_to_raw,line_added
        if may_add_line_to_raw and not line_added:construle+=line+'\n';line_added=True
    def decode_or_exec(string:str,default=0):
        nonlocal get_import_arg,get_define,import_args,import_nest,defined,imported
        global decode_strs
        mode=default
        has_symbol=True
        if string.startswith('?'):mode=0
        elif string.startswith('$'):mode=1
        elif string.startswith('%'):mode=2
        else:has_symbol=False
        can_string = mode != 2
        if has_symbol:string=string[1:]
        bracket_part=match_brackets(string,"{}")
        if bracket_part is None:
            dec = decode_strs.get(string)
            if dec is not None:return dec
        while bracket_part is not None:
            string=string.replace('{'+bracket_part+'}',pycr.stringify(decode_or_exec(bracket_part,default)))
            bracket_part=match_brackets(string,"{}")
        string=string.replace('\\{','{').replace('\\}','}')
        if mode==1:return string
        try:
            def_l=list()
            exec("def_l.append(%s)"%string)
            return def_l[0]
        except:
            if can_string:return string
            else:printwarn(WarnTypes.error,"name \"%s\" does not exist(forced not string)"%string)
    def get_lines_string():
        nonlocal pre_lines
        result = str()
        for line in pre_lines:
            result += line + "\n"
        return result
    def get_rel_line(rel:int=-1):
        nonlocal pre_lines,linenum
        return pre_lines[linenum+rel]
    def get_import_nest_name(nestnum:int=1):
        nonlocal import_nest
        if len(import_nest) >= nestnum:
            return import_nest[-nestnum]
        else:
            return "$MAIN"
    def ll_is_if():return get_rel_line().startswith(("#else","#if","#ifdef"))
    def new_if(b:bool):
        if_tags.append([b])
    def push_if(b:bool=None):
        nonlocal if_tags,else_serie
        if b is None:b=not if_tags[-1]
        if else_serie:
            if_tags[-1].append(if_no_true_exists() and b)
        else:
            new_if(b)
    def pop_if():
        nonlocal if_tags
        return if_tags[-1].pop()
    def end_if():
        nonlocal if_tags
        if_tags.pop()
    def if_no_true_exists():
        nonlocal if_tags
        return not any(if_tags[-1])
    def get_if_status():
        nonlocal if_tags
        for l in if_tags:
            if len(l) > 0 and not l[-1]:return False
        return True
    def inserttoken(token:str,aft:str):
        insert('#'+token+" "+aft)
    get_lo().next_level = global_levelname.copy()
    pre_lines = rule.split('\n')
    linenum=0
    can_define = True
    import_args:"dict[str,dict[str,object]]"=dict()
    imported:"list[str]"=list()
    if_tags:"list[list[bool]]"=list()
    pyexec_string:str=None
    import_nest:"list[str]"=list()
    defined:"set[str]"=set()
    genraw:bool=False
    filename=None
    is_raw_file:bool=False
    save_raw_file_to:str=None
    else_serie:bool=False
    line_added:bool=False
    force_adding:bool=False
    for line in pre_lines:
        can_define = get_if_status()
        prams = line.split(' ')
        token = prams[0][1:] if prams[0].startswith('#') else None
        line_added=False
        if force_adding:add_line_to_const()
        if token is not None:
            may_add_line_to_raw = not token.endswith('*')
            token=token.rstrip('*')
            aft = " ".join(prams[1:])
            if can_define and pyexec_string is None:
                if token == "fadd":force_adding=True
                elif token == "endfadd":force_adding=False
                elif not is_raw_file:
                    if token == "define":
                        args=unbsl_split(aft,":")
                        force_def = len(args)>=3 and decode_or_exec(args[2]) is True
                        if force_def or args[0] not in defined:
                            game=re.sub('(\\b)('+args[0]+')(\\b)',get_define,game)
                            define_name(args[0])
                    elif token == "pymacro":
                        args = unbsl_split(aft,":")
                        funcname = args[0].strip(' ')
                        match=re.match(r"(\w*)\(([\w\,]*)\)",funcname)
                        func:"list[FunctionType]"=list()
                        if match is not None:
                            funcname = match.group(1)
                            formalargs = unbsl_split(match.group(2).replace(' ',''),',')
                            exec("func.append(lambda %s:"%(','.join(formalargs))+':'.join(args[1:])+")")
                            formallen=len(formalargs)
                            while True:
                                match=re.search('\\b'+funcname+r"\(([\w\,]*)\)",game)
                                if match is None:break
                                matchgroup=funcname+"\\(%s\\)"%match.group(1)
                                rargs=unbsl_split(match.group(1).replace(' ',''),',')
                                rarglen=len(rargs)
                                if rarglen != formallen:continue
                                realargs=list()
                                for arg in rargs:realargs.append(decode_or_exec(arg,2))
                                game=re.sub(r"(\b)%s"%matchgroup,r'\1%s'%func[0](*realargs),game)
                        else:
                            exec("func.append(lambda :"+':'.join(args[1:])+")")
                            game=re.sub(r"(\b)%s(\b)"%funcname,r'\1%s\2'%func[0](),game)
                        define_name(funcname)
                    elif token == "import":
                        args = unbsl_split(aft,":")
                        filename = args[0]
                        import_args[filename]=dict()
                        set_import_arg("once",filename not in imported)
                        for arg in args[1:]:
                            match = re.match(r"\((\w*)\)(\w*)",arg)
                            if match is not None:
                                g2=match.group(2)
                                argcont = decode_or_exec(g2)
                                import_args[filename][match.group(1)]=argcont
                            else:
                                printwarn(WarnTypes.error,"import argument error : '%s'"%arg)
                        filename = filename.replace('.','/')
                        paths = (os.path.split(global_path)[0]+"/%s.rule"%filename,LEVELROOT%("%s.rule"%filename))
                        for p in paths:
                            if os.path.exists(p):
                                with open(p,"r",encoding="utf-8") as file:
                                    tmp_linenum = 1
                                    for file_line in split_filestring(file.read()):
                                        if not file_line.startswith('//'):
                                            insert(file_line,tmp_linenum)
                                            tmp_linenum+=1
                                imported.append(filename)
                                import_nest.append(filename)
                                insert("#endimport %s"%filename,tmp_linenum)
                                break
                    elif token == "formdef":
                        define_name(aft)
                    elif token == "printl":
                        if len(aft) > 0:
                            args=unbsl_split(aft,',')
                            print_args=list()
                            for a in args:print_args.append(decode_or_exec(a))
                            print(*print_args,sep=None)
                        else:
                            print(get_lines_string())
                    elif token == "genraw":
                        save_raw_file_to=aft if len(aft) > 0 else "genraw.lev"
                        rawname = "rawname:%s"%save_raw_file_to
                        genraw = True
                    elif token == "rawfile":
                        is_raw_file = True
                    elif token == "warn":
                        args = unbsl_split(aft,":")
                        argc=len(args)
                        if 2 <= argc <= 3:
                            warn_action_l=list()
                            try:exec("warn_action_l.append(WarnTypes.%s)"%args[0]);warn_action=warn_action_l[0]
                            except:warn_action=args[0]
                            nestcount=1
                            if len(args) == 3:
                                try:
                                    nestcount=int(args[2])
                                    if nestcount < 1:raise ValueError
                                except ValueError:
                                    printwarn(WarnTypes.error,"argument 2 in warn statement must be a integer >= 1")
                            printwarn(warn_action,decode_or_exec(args[1]),nestcount)
                        else:
                            printwarn(WarnTypes.error,"must have 2 or 3 args for warn statement, %d given"%argc)
                    elif token == "typedef":
                        args=unbsl_split(aft,":",False)
                        next_typedef = match_brackets(args[1])
                        if next_typedef is None:
                            insert("#type %s"%(":".join(args[:2])))
                        else:
                            next_temp=get_next_temp()
                            insert("#deltype %s"%next_temp)
                            insert(line.replace('('+next_typedef+')',next_temp))
                            insert("#typedef %s:%s"%(next_temp,next_typedef))
                    elif token == "insert":
                        args = unbsl_split(aft,":")
                        try:
                            if len(args) == 1:exec("insert(%s)"%args[0])
                            else:exec("insert(%s,%d)"%(args[0],int(args[1])))
                        except:
                            if len(args) == 1:insert(args[0])
                            else:
                                try:insert(args[0],int(args[1]))
                                except:printwarn(WarnTypes.error,"line insertion with args '%s' failed"%aft)
                    elif token == "loadimg":
                        args = unbsl_split(aft,":",False)
                        tmp_name=get_next_temp()
                        insert(f"#typedef {args[0]}:get_image<{args[0]}:true")
                        insert("#img %s"%aft)
                    elif token == "newpic":
                        args = unbsl_split(aft,":",False)
                        tmp_name=get_next_temp()
                        insert(f"#deltype {tmp_name}")
                        insert(f"#typedef {args[0]}:pic<{tmp_name}:true")
                        insert(f"#loadimg {tmp_name}:{args[1]}")
                    elif token == "del":
                        for t in aft.replace(' ','').split(','):
                            if t in decode_strs.keys():insert("#deltype %s"%t)
                            elif not is_raw_file and t in imported:insert("#import %s:(del)true:(once)false"%t)
                            elif t in defined:insert("#deldef %s"%t)
                            else:printwarn(WarnTypes.error,"trying to delete unknown alias or package '%s'"%t)
                if token == "next":
                    add_line_to_const()
                    if len(aft) == 0:
                        get_lo().next_level[1]+=1
                    else:
                        get_lo().next_level = list(map(int,aft.split('-')))
                elif token == "alias":
                    add_line_to_const()
                    args=unbsl_split(aft,':')
                    decode_strs[args[0]]=decode_or_exec(args[1],2)
                    define_name(args[0])
                elif token == "defgrav":
                    try:get_lo().gravity = DIRECTION_DECODE[aft]
                    except:printwarn(WarnTypes.error,"'%s' must be direction code for defgrav"%aft)
                elif token == "name":
                    add_line_to_const()
                    get_lo().level_name = aft
                elif token == "perfect":
                    add_line_to_const()
                    get_lo().perfect_steps = int(aft)
                elif token == "type":
                    add_line_to_const()
                    args=unbsl_split(aft,":")
                    typedef_args=analyze_object(args[1])
                    decode_strs[args[0]]=TypeDef_Closs_Object(typedef_args[0],typedef_args[1:])
                    define_name(args[0])
                elif token == "pyexec":
                    add_line_to_const()
                    pyexec_string=str()
                elif token == "deltype":
                    add_line_to_const()
                    for t in aft.replace(' ','').split(','):
                        decode_strs.pop(t)
                        try:defined.remove(t)
                        except:...
                elif token == "deldef":
                    add_line_to_const()
                    for t in aft.replace(' ','').split(','):
                        defined.remove(t)
                elif token == "img":
                    add_line_to_const()
                    args = unbsl_split(aft,":")
                    new_pic=pygame.image.load(RES%args[1]).convert()
                    new_pic.set_colorkey(WHITE)
                    inlevel_images[args[0]]=new_pic
            if pyexec_string is not None:
                pyexec_string+=line+'\n'
            elif token == "endif":
                try:
                    if len(aft) > 0 and decode_or_exec(aft,2):
                        if len(if_tags)>0:if_tags.clear()
                        else:raise IndexError
                    else:end_if()
                except IndexError:printwarn(WarnTypes.error,"no more if to end")
            elif token == "else":
                if ll_is_if():printwarn(WarnTypes.error,"else statement after if/else with no code between")
                else:else_serie=True
                insert("#endelse")
                if len(aft) > 0:
                    nline=None
                    for pram in aft.split(' '):
                        if is_statements(pram,IF_STATEMENT):
                            if nline is not None:insert(nline)
                            nline="#"+pram
                        elif nline is not None:
                            nline+=' '+pram
                    if nline is not None:insert(nline)
            elif token == "if":
                push_if(bool(decode_or_exec(aft,2)))
            elif token == "ifdef":
                args = unbsl_split(aft,":")
                try:
                    def_l = list()
                    exec("def_l.append(%s)"%args[0])
                    push_if(isinstance(def_l[0],(type,FunctionType)))
                except NameError:
                    push_if(args[0] in defined)
                if len(args) > 1 and not decode_or_exec(args[1]):
                    push_if()
            elif token == "ifndef":
                insert("#ifdef %s:false"%aft)
            elif token == "iflev":
                iflevelname=aft.split('-')
                if len(iflevelname) == 2:push_if(int(iflevelname[1])==levelname[1] and int(iflevelname[0])==levelname[0])
                else:push_if(int(iflevelname[0])==levelname[1])
            elif token == "iflang":
                if not else_serie:add_line_to_const()
                push_if(aft == lang)
            elif token == "endelse":else_serie=False
            elif not is_raw_file:
                if token == "endimport":
                    import_nest.pop()
                    if len(import_nest) > 0:
                        filename = import_nest[-1]
                    else:filename=None
                    import_args.pop(aft)
            elif token == "endpyexec" and pyexec_string is not None:
                add_line_to_const()
                exec(pyexec_string)
                pyexec_string=None
        linenum+=1
    game=re.sub(REP_SIGN_PATTERN,get_rep_sign,sub_excess(game))
    if genraw and construle is not None:
        with open(os.path.split(global_path)[0]+"/"+save_raw_file_to,'w',encoding="utf-8") as raw:
            raw.write("// raw file generated from %s\n"%global_path+construle+game)
    return game
def get_shape(game:str):
    lines = game.count('\n')+1
    linelen=0
    for line in game.split('\n'):
        length=line.count(' ')+1
        if length > linelen:
            linelen=length
    return (linelen,lines)
def compile_level(levelname:"list[int,int]"):
    global global_levelname,global_path
    refresh_decode()
    global_levelname=levelname
    global_path=get_path(levelname)
    rule,game=get_rule_and_game()
    create_lo()
    get_lo().init(get_shape(game))
    game = analyze_rule(rule,game,levelname)
    get_lo().reshape(get_shape(game))
    objs=analyze_game(game)
    if len(warps) > 0:
        last_warp=warps[-1]
        for w in warps:
            w.next = last_warp
            last_warp = w
    get_lo().objs=objs