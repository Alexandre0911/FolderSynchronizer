import os
import sys
import time
import hashlib
import filecmp
import datetime



class File:

    def __init__(self, name: str, source: str, hash: str, destination: str):
        self.name = name
        self.source = source
        self.hash = hash
        self.destination = destination



# Printing Headers
def printColor(text: str):
    """
    Args:
        - text - Very straight forward, takes any **string type** text
        
    Output:
        - Prints out the text but in magenta and bold
        
    ---

    WARNING
    - This is not supported natively for the windows cmd (usually), but should work without any issue in any linux dist terminal"""
    print(f'\033[1;35m {text} \033[1;m')



# Logging to both the console and the output file
def logToConsoleAndFile(_time: str, logFile: str, action: str):

    result = _time + " -> " + action

    with open(logFile, 'a') as lf:
        print(result)               # Prints action to console
        lf.write(result)            # Logs action to file



# Remove Last '/' If Found:
def trimSlash(inputSource: str):
    """
    Args:
        - inputLocation - either 'source' or 'target'
    
    Output:
        - As the function name, it only serves to delete the character '/' if it is found in args as an argument on the console

    ---

    Example 1:

    Args:
        - inputLocation - 'C:/Important/Source/'
        
    Output:
        - 'C:/Important/Source'

    ---

    Example 2:

    Args:
        - inputLocation - 'C:/Important/Source'
        
    Output:
        - 'C:/Important/Source'
    """

    if inputSource[-1] == '/':
        inputSource = inputSource[:-1]

    return inputSource



# User Inputs
source = str(sys.argv[1])
target = str(sys.argv[2])

source = trimSlash(source).replace('/', '\\')
target = trimSlash(target).replace('/', '\\')

outputFileName = sys.argv[3]
syncInterval = int(sys.argv[4])



# Directory Comparing - SOURCE Directory with TARGET Directory
def compareFilesDirs(dcmp):
    """
    Output:
        - This function will find every file found in EACH directory and will add those files to a separate list
        - This function will aswell compare the SOURCE directory with the TARGET directory and add to a list the files and dirs which are not the same as the SOURCE ones in TARGET
    """

    # Modified Files:
    for fileName in dcmp.diff_files:

        source = dcmp.left + '/' + fileName
        destination = dcmp.right + '/' + fileName

        file = File(fileName, source, md5(source), destination)

        modifiedFiles.append(file)

    for subdcmp in dcmp.subdirs.values():
        compareFilesDirs(subdcmp)

    
    # Files/Directories Only In SOURCE
    for fileName in dcmp.left_only:

        source = dcmp.left + '/' + fileName
        destination = dcmp.right + '/' + fileName

        if os.path.isfile(source):
            file = File(fileName, source, md5(source), destination)
            filesInSource.append(file)

        else:
            dirsInSource.append(source)
    
    
    # Files/Directories Only In TARGET
    for fileName in dcmp.right_only:
        
        source = dcmp.right + '/' + fileName
        destination = dcmp.left + '/' + fileName

        if os.path.isfile(source):
            file = File(fileName, source, md5(source), destination)
            filesInTarget.append(file)

        else:
            dirsInTarget.append(source)

# Printing Files In TARGET That Are Not Identical To It's SOURCE File
def findModified():
    """
    Output:
        - Prints every file present in TARGET that has is not indentical to it's SOURCE similar file
    """

    # Printing Modified File Names:
    counter = 1
    printColor("Modified Files: ")
    print(f"Modified Files Found: {len(modifiedFiles)}\n")

    for modFile in modifiedFiles:
        print(f"[{counter}]")
        print(f"File Name   : {modFile.name}")
        print(f"Source      : {modFile.source}")
        print(f"Destination : {modFile.destination}")
        print(f"MD5 Hash    : {modFile.hash}\n")

        counter += 1
    print("-=-="*10 + "\n")

# Printing Files Found Only Either In SOURCE **OR** TARGET
def foundFiles(fileList: list, location: str):
    """
    Args:
        - fileList - List of files "filesInSource" or "filesInTarget"
        - location - String which should be either "source" or "target"

    Output:
        - Prints number of files present in the specified list and info relative to each file
    """
    counter = 1

    printColor(f"Files Present Only In {location.upper()}: ")
    print(f"Found: { len(fileList) }\n")

    for file in fileList:
        print(f"[{counter}]")
        print(f"File Name   : {file.name}")
        print(f"Source      : {file.source}")
        print(f"Destination : {file.destination}")
        print(f"MD5 Hash    : {file.hash}\n")

        counter += 1
    print("-=-="*10 + "\n")

# Printing Dirs Found Only Either In SOURCE **OR** TARGET
def foundDirs(dirList: list, location: str):
    """
    Args:
        - dirList - List of files "filesInSource" or "filesInTarget"
        - location - String which should be either "source" or "target"

    Output:
        - Prints number of dirs present in the specified list and it's path
    """
    counter = 1

    printColor(f"Directories Present Only In {location.upper()}: ")
    print(f"Found: {len(dirList)}\n")

    for dir in dirList:
        print(f"[{counter}]")
        print(f"Source    : {dir}\n")

        counter += 1
    print("-=-="*10 + "\n")

# Replace TARGET's file/dir with SOURCE's file/dir:
def replaceSourceTarget(target: str, source: str):
    """
    Args:
        - target - TARGET folder path
        - source - Source file/dir path

    Output:
        - Once more, very straight forward. This function will replace files and directories inside TARGET with files and directories from SOURCE 
    """
    locationWithTarget = source[source.find('/') + 1:]

    return locationWithTarget

# Calculate MD5:
def md5(fileName: str):
    """
    Args:
        - fileName - Name of file to hash

    Output:
        - Generates MD5 from given file if it exists. Otherwise, fileName is inserted into a list of deletedDirs
    """

    try:
        with open(fileName, "rb") as file:
            fileContent = file.read()
            hash = hashlib.md5(fileContent)
    except:
        deletedDirs.append(fileName)

    return hash.hexdigest()



# Copying, from SOURCE, DIRS and FILES missing in TARGET
def windowsCopyDirs():
        
    print("Copying Directory(ies) to TARGET:\n")

    for _dir in dirsInSource:

        _dir = _dir.replace('/', '\\')
        _source = source.replace("/", "\\")
        _target = target.replace("/", "\\")

        os.system(fr'xcopy "{_source}" "{_target}" /q /e /s /t /y')
            
        message = f'Directory "{_dir}" successfully copied to TARGET.\n\n'

        logToConsoleAndFile(currentTime, outputFileName, message)

def windowsCopyFiles():

    print("\nCopying File(s) to TARGET:\n")
        
    for _file in filesInSource:

        _source = _file.source.replace("/", "\\")
        _target = _file.destination.replace("/", "\\")

        os.system(f'copy "{_source}" "{_target}" /y')
            
        message = f'File "{_file.name}" successfully copied to TARGET.\n\n'

        logToConsoleAndFile(currentTime, outputFileName, message)

def windowsUpdateFiles():

    print("\nUpdating File(s) in TARGET:\n")

    for _file in modifiedFiles:

        _source = _file.source.replace("/", "\\")
        _target = _file.destination.replace("/", "\\")

        os.system(f'copy "{_source}" "{_target}" /y')
            
        message = f'File "{_file.name}" successfully updated.\n\n'

        logToConsoleAndFile(currentTime, outputFileName, message)

# Removing, from TARGET, DIRS and FILES missing in SOURCE
def windowsRemoveDirs():

    print("\nRemoving Directory(ies) from TARGET:\n")
        
    for _dir in dirsInTarget:

        _dir = _dir.replace('/', '\\')
        location2 = replaceSourceTarget(target, _dir)
        os.system(f'rmdir /S /Q "{location2}"')

        message = f'Directory "{_dir}" and all the content inside were successfully removed from TARGET.\n\n'

        logToConsoleAndFile(currentTime, outputFileName, message)
    
def windowsRemoveFiles():

    print("\nRemoving File(s) from TARGET:\n")
        
    for file in filesInTarget:
            
        _source = file.source.replace('/', '\\')
        os.system(f'del /f "{_source}"')

        message = f'File "{file.name}" successfully removed from TARGET.\n\n'

        logToConsoleAndFile(currentTime, outputFileName, message)



# Clears all lists so the program doesnt try to run the same commands on the same files over and over again
def clearLists():
    deletedDirs.clear()
    filesInSource.clear()
    dirsInSource.clear()
    filesInTarget.clear()
    dirsInTarget.clear()
    modifiedFiles.clear()



while True:
    
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime('[%d/%m/%y - %H:%M:%S]')

    dcmp = filecmp.dircmp(source, target)   # source path -> dcmp.left | ---  ---  --- | target path -> dcmp.right

    deletedDirs = []
    filesInSource = []
    dirsInSource = []
    filesInTarget = []
    dirsInTarget = []
    modifiedFiles = []



    clearLists()

    compareFilesDirs(dcmp)

    # Printing Files Which Are Common Between SOURCE and TARGET But Have Modified Data
    findModified()

    # Printing Files And Directories Found Only In SOURCE
    foundFiles(filesInSource, 'source')
    foundDirs(dirsInSource, 'source')

    # Printing Files And Directories Found Only In TARGET
    foundFiles(filesInTarget, 'target')
    foundDirs(dirsInTarget, 'target')



    # ------------------------------------------------------------------------------------- #
    #                           CREATING & COPYING - DIRS & FILES                           #
    # ------------------------------------------------------------------------------------- #
    #   Firstly, the program will check for DIRS missing in TARGET                          #
    #   If there are any DIRS missing, the program will copy those DIRS from SOURCE         #
    #   After so, the program will check for FILES missing in TARGET                        #
    #   If there are any FILES missing, the program will copy those FILES from SOURCE       #
    # ------------------------------------------------------------------------------------- #
    #                                REMOVING - DIRS & FILES                                #
    # ------------------------------------------------------------------------------------- #
    #   Firstly, the program will check for DIRS which exist in TARGET but not in SOURCE    #
    #   If there are any, the program will remove those DIRS from TARGET                    #
    #   After so, the program will check for FILES which exist in TARGET but not in SOURCE  #
    #   If there are any, the program will remove those FILES from TARGET                   #
    # ------------------------------------------------------------------------------------- #


                
    if len(dirsInSource) > 0:   # Checks for DIRS present ONLY in SOURCE
        windowsCopyDirs()

    if len(filesInSource) > 0:  # Checks for FILES present ONLY in SOURCE
        windowsCopyFiles()

    if len(dirsInTarget) > 0:   # Check for DIRS present ONLY in TARGET
        windowsRemoveDirs()

    if len(filesInTarget) > 0:  # Check for FILES present ONLY in TARGET
        windowsRemoveFiles()

    if len(modifiedFiles) > 0:  # Checks for modified FILES
        windowsUpdateFiles()



    time.sleep(syncInterval)    # Interval (In Seconds) Between Each Attempt Folder Synchronization