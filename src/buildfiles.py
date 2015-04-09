import os
import subprocess

def clean(configParsed):
    if os.path.exists(".buildmeta"):
        os.remove(".buildmeta")
    
    if os.path.exists("./" + configParsed["output"]["interbuild"]):
        shutil.rmtree("./" + configParsed["output"]["interbuild"])
    
    if os.path.exists("./" + configParsed["output"]["bindir"]):
        shutil.rmtree("./" + configParsed["output"]["bindir"])
        
def createDirs(configParsed):
    subprocess.check_output("cd " + configParsed["build"]["srcdir"] + "; " + "find -type d -exec mkdir -p \"../obj/{}\" \\;", shell=True)
        
    if not os.path.exists("./" + configParsed["output"]["bindir"]):
        os.makedirs(configParsed["output"]["bindir"])
    
    if not os.path.exists("./" + configParsed["output"]["interbuild"]):
        os.makedirs(configParsed["output"]["interbuild"])