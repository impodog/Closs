import json,os
profile:dict=None
def get_profile():
    global profile
    return profile
def load_profile():
    global profile
    with open("profile/user.json",'r') as user:
        profile=json.load(user)
def rm_repeat(l:list):
    res=list()
    for o in l:
        if o not in res:res.append(o)
    return res
def save_profile():
    global profile
    profile["perfection"]=rm_repeat(profile["perfection"])
    profile["perfection"].sort()
    with open("profile/user.json",'w') as user:
        json.dump(profile,user)
def check_profile():
    if not os.path.exists("profile/user.json"):
        with open("profile/user.json",'w') as user:
            with open("profile/def.json",'r') as default:
                user.write(default.read())