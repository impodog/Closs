import sys,os,subprocess
My_Repo = "https://gitee.com/impodog/%s.git"
if sys.platform.startswith("win32"):
    INSTALLER = My_Repo%"installer"
    os.mkdir("repos")
    os.chdir("repos")
    subprocess.call(("git","clone",INSTALLER))
    os.chdir("installer")
    subprocess.call(("python","ins.py"))
    os.chdir("../..")
else:
    REPOS={
        "calca":"calca",
        "ver-rect":"VerRect",
        "pygame-crew":"PygameCrew"
    }
    for repo,changed_name in REPOS.items():
        subprocess.call(("git","clone",My_Repo%repo))
        os.rename(repo,changed_name)
        reqpath=os.path.join(changed_name,"requirements.txt")
        if os.path.exists(reqpath):
            subprocess.call(("pip","install","-r",reqpath))
print("Setup complete!")