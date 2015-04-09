#!/usr/bin/env python2

import sys
import os
import json
import re
import hashlib
import shutil

import build
import buildfiles
import metabuild

def main():
    filelist = list()
    
    configPath = "build.json"
    buildSetting = "debug"
    
    configFile = open(configPath)
    configParsed = json.load(configFile)
    configFile.close();
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "rebuild":
            clean(configParsed)
        elif sys.argv[1] == "clean":
            clean(configParsed)
            sys.exit(0)
        else:
            buildSetting = sys.argv[1]
        if len(sys.argv) > 2:
            buildSetting = sys.argv[2]
    
    
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
        createMetaFile();
    if os.path.exists(".buildmeta"):
        metafile = open(".buildmeta", "r+")
    
    metajson = None
    #Clears the metafile if it's invalid.
    try:
        metajson = json.load(metafile)
    except ValueError, e:
        createMetaFile()
        metajson = json.load(metafile)
    
    sourcelist = metabuild.getSourceList(filelist, configParsed)
    includelist = metabuild.getIncludeList(filelist, configParsed)
    
    print str(len(sourcelist)) + " source files found, " + str(len(includelist)) +  " additional tracked files.\n"
    
    recompilelist = metabuild.getRebuildList(sourcelist, includelist, metajson, configParsed)
    
    print "Starting compilation for option " + buildSetting + "..."
    
    args = build.getCommandTemplate(buildSetting, configParsed)
    
    build.build(recompilelist, args, configParsed)
    
    metabuild.finalizeFile(metajson)
    
    print "Linking output..."

    dirtree = os.walk("./" + configParsed["output"]["interbuild"])

    outputList = list()
    
    for dirname, dirnames, filenames in dirtree:
        for filename in filenames:
            outputList.append(os.path.join(dirname, filename))
            
    build.link(outputList, buildSetting, configParsed)
    
    return "Build finished."


print main()
