import sys
import subprocess

#Construct the command template
def getCommandTemplate(buildSetting, configParsed):
    args = ""
    for argument in configParsed["build"]["flags"]:
        args += "-" + argument[0] 
        if(argument[1] != ""):
            args += "=" + argument[1]
        args += " "
    
    for argument in configParsed[buildSetting]["flags"]:
        args += "-" + argument[0] 
        if(argument[1] != ""):
            args += "=" + argument[1] + " "
        args += " "
    
    return args

#This constructs the compile command.
def build(recompilelist, arguments, configParsed):
    for file in recompilelist:
        output = "./" + configParsed["output"]["interbuild"] + os.path.splitext(file)[0][(len(configParsed["build"]["srcdir"]) + 2):] + ".obj"
        
        command = configParsed["build"]["command"] + " " + arguments + "-c " + file 
        
        for dir in configParsed["build"]["includedirs"]:
            command += " -I" + dir
        
        command += " -o " + output
        
        print "Compiling \"" + output + "\""
        
        sys.stdout.write(subprocess.check_output(command, shell=True))

#Links the output.
def link(outputList, buildSetting, configParsed):
    command = configParsed["build"]["command"] + " -o " + "./" + configParsed["output"]["bindir"] + "/" + configParsed["output"]["binname"] + " "
    for file in outputList:
        command += file + " "
    for library in configParsed["build"]["libs"]:
        command += "-l" + library + " "
    for library in configParsed[buildSetting]["libs"]:
        command += "-l" + library + " "
    
    for library in configParsed["build"]["extlibs"]:
        command += "-L" + library + " "
    for library in configParsed[buildSetting]["extlibs"]:
        command += "-L" + library + " "
    sys.stdout.write(subprocess.check_output(command, shell=True))