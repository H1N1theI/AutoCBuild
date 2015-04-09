import os

def getRecompileTargets(changedfiles, config):
    dirtree = os.walk("./deps")
    
    recompiletargets = list()
    
    for dirname, dirnames, filenames in dirtree:
        for filename in filenames:
            file = open(os.path.join(dirname, filename)).read()
            for target in changedfiles:
                if target[2:] in file:
                    recompiletargets.append("./" + config["build"]["srcdir"] + os.path.join(dirname, filename)[6:-2])
    
    return recompiletargets