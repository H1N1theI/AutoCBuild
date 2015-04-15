#!/usr/bin/env python2

import sys
import os
import json

import build
import buildfiles
import metabuild
import config

def main():
    filelist = list()
    
    configPath = "build.json"
    
    validate = False;
    
    configParsed = None
    
    clean = False
    
    exit = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "rebuild":
            clean = True
            if len(sys.argv) > 2:
                configPath = sys.arg[2] + ".json"
        elif sys.argv[1] == "clean":
            clean = True
            exit = True
        else:
            configPath = sys.argv[1] + ".json"
            
    configParsed = config.loadConfig(configPath)
        
    if clean:
        buildfiles.clean(configParsed)
        if exit:
            sys.exit(0)
    
    
    #Creates folders if not already present.
    buildfiles.createDirs(configParsed)
    
    dirtree = os.walk("./" + configParsed["build"]["srcdir"])
    
    #Construct the full directory tree
    for dirname, dirnames, filenames in dirtree:
        for filename in filenames:
            filelist.append(os.path.join(dirname, filename))
    
    #Creates the build metafile
    metafile = None
    if not os.path.exists(".buildmeta"):
        metabuild.createMetaFile();
    if os.path.exists(".buildmeta"):
        metafile = open(".buildmeta", "r+")
    
    metajson = None
    #Clears the metafile if it's invalid.
    try:
        metajson = json.load(metafile)
    except ValueError, e:
        metabuild.createMetaFile()
        metajson = json.load(metafile)
    
    sourcelist = metabuild.getSourceList(filelist, configParsed)
    includelist = metabuild.getIncludeList(filelist, configParsed)
    
    print str(len(sourcelist)) + " source files found, " + str(len(includelist)) +  " additional tracked files.\n"
    
    recompilelist = metabuild.getRebuildList(sourcelist, includelist, metajson, configParsed)
    
    print "Starting compilation..."
    
    build.build(recompilelist, configParsed)
    
    metabuild.finalizeFile(metajson)
    
    if configParsed["link"]["link"] == False:
        print "Build finished."
        sys.exit(0)
    
    print "Linking output..."

    dirtree = os.walk("./" + configParsed["output"]["interbuild"])

    outputList = list()
    
    for dirname, dirnames, filenames in dirtree:
        for filename in filenames:
            if filename.endswith(".obj"):
                outputList.append(os.path.join(dirname, filename))
            
    build.link(outputList, configParsed)
    
    return "Build finished."

print main()