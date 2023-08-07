import json

def scriptContext(filename) :
    version = json.load(open(".config.json"))["scriptsVersion"]
    return "../../data_flow/" + version + "/" +filename

def dayContext(m, filename) :
    day = json.load(open(".config.json"))["day"]
    return "../Day" + (day - m) + "/" + filename