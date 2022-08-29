from .sol import*
DIRECTION_DECODE={
    "up":UP,
    "dw":DOWN,
    "lt":LEFT,
    "rt":RIGHT
}
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
    "hd":hide,
    "in":instanceof
}
DECODE=dict()
DECODE.update(DIRECTION_DECODE)
DECODE.update(CLASS_DECODE)
ENCODE=invert(DECODE)
SPLITHERE="[splithere]"
NOT_PREPROCESS=("#python","#endpy")
def get_decode(string:str):return DECODE[string]
def get_dirdecode(string:str):return DIRECTION_DECODE[string]
def rep_splithere(match:re.Match):return match.group(1)+SPLITHERE
def unbsl_split(string:str,s:str)->"list[str]":return re.sub(r"([^\\])%s"%s,rep_splithere,string).split(SPLITHERE)
def pat_split(pattern:str,string:str)->"list[str]":return re.sub(pattern,rep_splithere,string).split(SPLITHERE)
def is_not_preprocess(string:str)->bool:
    for p in NOT_PREPROCESS:
        if string.startswith(p):return True
    return False