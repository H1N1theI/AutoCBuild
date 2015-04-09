import os
import sys
import json
import hashlib

import deps

def createMetaFile():
    defaultfile = {"src": dict(), "inc" : dict()}
    finalizeFile(defaultfile)

def getHash(path):
    file = open(path)
    blocksize = 65536
    hashfunc = hashlib.sha256()
    buffer = file.read(blocksize)
    while len(buffer) > 0:
        hashfunc.update(buffer)
        buffer = file.read(blocksize)
    return hashfunc.hexdigest()

def getSourceList(filelist, configParsed):
    #Constructs the list of all source files to include.
    
    sourcelist = list()
    
    for name in filelist:
        for extension in configParsed["build"]["srcext"]:
            if(os.path.splitext(name)[1] == '.' + extension):
                sourcelist.append(name.encode('ascii', 'ignore'))
                
    return sourcelist
                
def getIncludeList(filelist, configParsed):
    includelist = list()
    
    #Constructs include files, E.G. any other files to keep a tab on (need full recompile upon changes, simplest way right now.)
    for name in filelist:
        for extension in configParsed["build"]["incext"]:
            if(os.path.splitext(name)[1] == '.' + extension):
                includelist.append(name.encode('ascii', 'ignore'))
        
    return includelist
    
def getRebuildList(sourcelist, includelist, metajson, configParsed):
    changedinc = list()
    recompilelist = list()
    
    for incfile in includelist:
        hashkey = getHash(incfile)
        if incfile in metajson["inc"]:
            if metajson["inc"][incfile] != hashkey:
                metajson["inc"][incfile] = hashkey
                changedinc.append(incfile)
                print "File " + incfile + " has changed, will recompile dependents."
        else:
            metajson["inc"][incfile] = hashkey
            changedinc.append(incfile)
            print "File " + incfile + " is new, will recompile some dependents."
        
    for srcfile in sourcelist:
        hashkey = getHash(srcfile)
        if srcfile in metajson["src"]:
            if metajson["src"][srcfile] != hashkey:
                metajson["src"][srcfile] = hashkey
                recompilelist.append(srcfile)
                print "File " + incfile + " has changed, will partially recompile."
        else:
            metajson["src"][srcfile] = hashkey
            recompilelist.append(srcfile)
            print "File " + incfile + " is new, will partially recompile."
    
    recompilelist.extend(deps.getRecompileTargets(changedinc, configParsed))
    
    return recompilelist
    
def finalizeFile(metajson):
    metafile = open(".buildmeta", "w+")
    metafilestr = json.dumps(metajson)
    metafile.seek(0)
    metafile.write(metafilestr)
    metafile.truncate(len(metafilestr))
    metafile.close()