##############################################
#######   Author : Chris Mack         ########
#######   Date   : 15/03/16           ########
#######   Name   : MultiFileDownload  ########
##############################################

import os
import json
import urllib
import urllib.request
from shutil import copyfile

# Get the location the script is being ran from
def currentDir():
    return os.getcwd()

# Parse json file
# inputData : path to file
def readJson(inputData):
    return json.load(inputData)

# Downloads a file from a url to a specific name
def download(url, fileName):
    with open(fileName, 'wb') as out_file:
        try:
            print("downloading : " + fileName)
            result = urllib.request.urlopen(url).read()
            out_file.write(result)
        except:
            print("Couldn't download : " + str(url))
            
# Download all files in the common folder
def downloadCommonPlugins(files):
    if not os.path.exists(currentDir() + "\\common"):
        os.makedirs(currentDir() + "\\common")
    for i in range(len(files)):
        download(files[i]["fileURL"], currentDir() + "\\common\\" + files[i]["fileName"] + ".jar")

# Download the files for each location
def downloadSpecificPlugins(locations, files):
    for location in locations:
        directory = locations[location]
        #directory = currentDir() + "\\" + location + "\\plugins\\"

        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(len(files[location])):
            download(files[location][i]["fileURL"], directory + files[location][i]["fileName"] + ".jar")

# copy all common files to the locations
def copyCommons(locations):
    print("copy commons")
    commonDir = currentDir() + "\\common"
    if os.path.exists(commonDir):
        commonFiles = os.listdir(commonDir)
        for location in locations:
            for i in range(len(commonFiles)):
                dest = locations[location]
                copyfile(commonDir + "\\" + commonFiles[i], dest + commonFiles[i])

def main():
    with open(currentDir() + '\\FileList.json') as json_data:
        data = readJson(json_data)

        #locations<locationName, location>
        locations={}
        for i in range(len(data["locations"])):
            locations[data["locations"][i]["locationName"]] = data["locations"][i]["location"]
            
        #files<locationName, fileInfo<fileName, fileURL>
        files={}
        for location in locations:
            files[location] = data["files"][location]
        files["common"] = data["files"]["common"]

        downloadCommonPlugins(files["common"])
        downloadSpecificPlugins(locations, files)
        copyCommons(locations)
        
main()
