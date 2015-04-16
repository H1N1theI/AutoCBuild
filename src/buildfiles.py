import os
import subprocess
import shutil

def clean(configParsed):
    if os.path.exists(".buildmeta"):
        os.remove(".buildmeta")
    
    if os.path.exists("./" + configParsed["output"]["interbuild"]):
        shutil.rmtree("./" + configParsed["output"]["interbuild"])
    
    if os.path.exists("./" + configParsed["output"]["bindir"]):
        shutil.rmtree("./" + configParsed["output"]["bindir"])
        
    if os.path.exists("./deps"):
        shutil.rmtree("./deps")
        
def createDirs(configParsed):
    cdir = os.getcwd()
    
    if not os.path.exists("./" + configParsed["output"]["bindir"]):
        os.makedirs(configParsed["output"]["bindir"])
    
    if not os.path.exists("./" + configParsed["output"]["interbuild"]):
        os.makedirs(configParsed["output"]["interbuild"])
        subprocess.check_output("cd " + configParsed["build"]["srcdir"] + "; " + "find -type d -exec mkdir -p \"" + cdir + "/obj/{}\" \\;", shell=True)
    
    if not os.path.exists("./deps"):
        os.makedirs("./deps")
        subprocess.check_output("cd " + configParsed["build"]["srcdir"] + "; " + "find -type d -exec mkdir -p \"" + cdir + "/deps/{}\" \\;", shell=True)