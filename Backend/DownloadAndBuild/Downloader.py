import os
import shutil
import subprocess
import json

from pathlib import Path

from Backend.DownloadAndBuild.Config import *
from Backend.DownloadAndBuild.ProfileTemplate import *

class Downloader:

    def __init__(self) -> None:
        self.absConfigPath: str
        self.config: Config
        self.installJsons: list[str] = []

        self.results: Result = Result()
        self.jsonResult: str

    def Setup(self, configPath: str):
        self.absConfigPath = configPath

        currentDir = os.getcwd()
        tempDir = ".\Temp"
        
        if os.path.isdir(tempDir):
            shutil.rmtree(tempDir)
        os.mkdir(tempDir)
        os.chdir(tempDir)

        self.Work(configPath)
        
        os.chdir(currentDir)


    def Work(self, configPath: str):

        with open(configPath, 'r') as file:
            j = file.read().replace('\n', '')
            d = json.loads(j)
            self.config = Config(**d)

        with open("./profile", 'w') as file:
            profile = ProfileTemplate.Get(self.config.profile)
            file.write(profile)

        if not self.AccumulatePackageInfo():
            return

        if not self.InstallPackages():
            return

        self.AccumulateResults()
        self.ConvertToResultObject()
        self.SaveResults()
 
    def AccumulatePackageInfo(self) -> bool:
        for p in self.config.packages:
            cmd = ["conan", "graph", "info", "-pr", "./profile", f"--requires={p.name}/{p.version}"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE)

            if result.returncode != 0:
                return False
        return True
        
    def InstallPackages(self) -> bool:
        for p in self.config.packages:
            cmd = ["conan", "install", "--build=missing", "-pr", "./profile", f"--requires={p.name}/{p.version}", "--format=json"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE)

            if result.returncode != 0:
                return False
            
            jsonData: str = result.stdout.decode("utf-8").replace('\r', '')
            self.installJsons.append(jsonData)

            ###
            # with open(f"./install_{p.name}_{p.version}.json", 'w') as file:
                # file.write(jsonData)
            ###
        return True
            
    def AccumulateResults(self):
        for j in self.installJsons:
            d = json.loads(j)

            nodes = d["graph"]["nodes"]
            for node in nodes:
                if node["label"] == "cli":
                    continue

                label = node["label"]

                cpp_info = node["cpp_info"]
                root = cpp_info["root"]
                includedirs = root["includedirs"]
                libdirs = root["libdirs"]
                bindirs = root["bindirs"]

                packageResult = PackageResult()
                if len(bindirs) > 0:
                    packageResult.binDir = bindirs[0]
                if len(includedirs) > 0:
                    packageResult.includeDir = includedirs[0]
                if len(libdirs) > 0:
                    packageResult.libDir = libdirs[0]
                self.results.packages[label] = packageResult

    def ConvertToResultObject(self):    
        self.jsonResult = json.dumps(self.results.__dict__, default=lambda o: o.__dict__, indent=4, sort_keys=True)

    def SaveResults(self):
        resultAbsFileName = self.config.resultFileName

        if not os.path.isabs(resultAbsFileName):
            absConfigDirPath = Path(self.absConfigPath).parent.absolute().__str__()
            resultAbsFileName = os.path.join(absConfigDirPath, resultAbsFileName)

        with open(resultAbsFileName, 'w') as file:
            file.write(self.jsonResult)


