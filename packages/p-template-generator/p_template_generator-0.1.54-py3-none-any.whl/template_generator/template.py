import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
from template_generator import binary

def getCommandResult(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            return result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            return ""
    except subprocess.CalledProcessError as e:
        return ""

def getBinary(searchPath):
    binaryPath = ""
    if sys.platform == "win32":
        binaryPath = os.path.join(os.path.join(binary.skymediaPath(searchPath), "win"), "TemplateProcess.exe")
    elif sys.platform == "linux":
        binaryPath = os.path.join(binary.skymediaPath(searchPath), "linux", "TemplateProcess.out")
        if os.path.exists(binaryPath):
            cmd = subprocess.Popen(f"chmod 755 {binaryPath}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while cmd.poll() is None:
                print(cmd.stdout.readline().rstrip().decode('utf-8'))
        #check env
        if os.path.exists("/usr/lib/libskycore.so") == False:
            setupShell = os.path.join(binary.skymediaPath(searchPath), "linux", "setup.sh")
            if os.path.exists(setupShell):
                print(f"=================== begin Initialize environment : sh {setupShell} ==================")
                try:
                    cmd = subprocess.Popen(f"sh {setupShell}", stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
                    while cmd.poll() is None:
                        print(cmd.stdout.readline().rstrip().decode('utf-8'))
                except subprocess.CalledProcessError as e:
                    raise e
                print("===================             end              ==================")
            if os.path.exists("/usr/lib/libskycore.so") == False:
                raise Exception("linux environment error")
        if len(getCommandResult("echo $XDG_SESSION_TYPE")) <= 0:
            #no x11 or wayland
            if len(getCommandResult("echo $DISPLAY")) <= 0:
                displayShell = os.path.join(binary.skymediaPath(searchPath), "linux", "display.sh")
                if os.path.exists(displayShell):
                    getCommandResult(f"sh {displayShell}")

            
    if os.path.exists(binaryPath):
        return binaryPath
    return ""
    
def resetTemplate(data, searchPath):
    template_path = data["template"]
    if os.path.exists(template_path):
        return
    randomEffectPath = binary.randomEffectPath(searchPath)
    template_path = os.path.join(randomEffectPath, template_path)
    if os.path.exists(template_path):
        data["template"] = template_path
        return
    raise Exception(f"template {template_path} not found")
    
def isAdaptiveSize(data):
    template_path = data["template"]
    templateName = os.path.basename(template_path)
    if "template" in templateName or templateName == "AIGC_1":
        return True
    return False

def maybeMesa():
    if sys.platform == "linux":
        if len(getCommandResult("echo $XDG_SESSION_TYPE")) <= 0 and len(getCommandResult("echo $DISPLAY")) <= 0:
            #no (x11 or wayland) and (xvfb not found)
            return True
        else:
            return False
    else:
        return False

def executeTemplate(data, searchPath, useAdaptiveSize):        
    binaryPath = getBinary(searchPath)
    if len(binaryPath) <= 0:
        raise Exception("binary not found")

    output_path = ""
    if isinstance(data, (dict)):
        output_path = data["output"]
        resetTemplate(data, searchPath)
        useAdaptiveSize = useAdaptiveSize or isAdaptiveSize(data)
    elif isinstance(data, (list)):
        for it in data:
            output_path = it["output"]
            resetTemplate(it, searchPath)
            useAdaptiveSize = useAdaptiveSize or isAdaptiveSize(it)

    inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{random.randint(100,99999999)}.in")
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w') as f:
        json.dump(data, f)

    extArgs = ""
    #--adaptiveSize
    if useAdaptiveSize:
        extArgs += "--adaptiveSize true "
    #--fontDir
    fontPath = binary.fontPath(searchPath)
    if os.path.exists(fontPath):
        extArgs += f"--fontDir {fontPath} "
    #--subEffectDir
    subPath = binary.subEffectPath(searchPath)
    if os.path.exists(subPath):
        extArgs += f"--subEffectDir {subPath} "
    #--gpu
    if maybeMesa():
        extArgs += f"--call_mesa "

    command = f'{binaryPath} --config {inputArgs} {extArgs}'
    print(f"=== executeTemplate => {command}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode == 0:
        os.remove(inputArgs)
        #check one output
        if os.path.exists(output_path) == False:
            raise Exception("output file not found")
        print(result.stdout.decode(encoding="utf8", errors="ignore"))
    else:
        print(result.stderr.decode(encoding="utf8", errors="ignore"))
        raise Exception(f"template process exception!")
    
    
def generateTemplate(config, output, searchPath):        
    binaryPath = getBinary(searchPath)
    if len(binaryPath) <= 0:
        raise Exception("binary not found")
    
    if os.path.exists(config) == False:
        raise Exception("input config not exist")

    if os.path.exists(output) == False:
        os.makedirs(output)

    command = f'{binaryPath} --project {config} -y {output}'
    print(f"=== generateTemplate => {command}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        print(result.stderr.decode(encoding="utf8", errors="ignore"))
        raise Exception(f"generate template exception!")