import json

def loadConfig (configPath):
    configFile = open("acb-config/" + configPath)
    configParsed = json.load(configFile)
    configFile.close();
    
    return configParsed