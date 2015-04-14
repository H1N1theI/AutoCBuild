import os
import sys
import subprocess
import multiprocessing

#Construct the command template
def getCommandTemplate(stage, configParsed):
    args = ""
    for argument in configParsed[stage]["flags"]:
        args += " -" + argument[0] + argument[1] + argument[2]
        
    return args

#This constructs the compile command.
def build(recompilelist, configParsed):
    commandlist = list()
    
    arguments = getCommandTemplate("build", configParsed)
    
    for file in recompilelist:
        output = "./" + configParsed["output"]["interbuild"] + os.path.splitext(file)[0][(len(configParsed["build"]["srcdir"]) + 2):] + ".obj"
        
        depfile = file[len(configParsed["build"]["srcdir"]) +2:]
        
        command = configParsed["build"]["command"] + " -MMD -MF " + "\"./deps" + depfile + ".d" + "\"" + arguments + " -c " + file 
        
        for dir in configParsed["build"]["includedirs"]:
            command += " -I" + dir
        
        command += " -o " + output
        
        print "Compiling \"" + output + "\""
        
        commandlist.append(command)
    
    threads = multiprocessing.cpu_count()
    
    if(threads < 1):
        threads = 1
    result = multiprocessing.Pool(processes = threads).map_async(concurrentBuild, commandlist)
    
    for output in result.get():
        if output != 0:
            print "A file failed to compile! Stopping compilation."
            sys.exit(0)

#Links the output.
def link(outputList, configParsed):
    arguments = getCommandTemplate("link", configParsed)
    
    command = configParsed["build"]["command"] + " -o " + "./" + configParsed["output"]["bindir"] + "/" + configParsed["output"]["binname"] + " "
    for file in outputList:
        command += file + " "
    for library in configParsed["link"]["libs"]:
        command += "-l" + library + " "
    
    for libdir in configParsed["link"]["extlibs"]:
        command += "-L" + libdir + " "
        
    command += arguments
    
    sys.stdout.write(subprocess.check_output(command, shell=True))
    
def concurrentBuild(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        return -1

    return 0