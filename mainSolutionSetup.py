import os
import sys

import shutil

from Backend.DownloadAndBuild.Downloader import *

if __name__ == '__main__':

    # Вход - путь к solution и файл props
    if len(sys.argv) != 1:
        absPath = os.path.abspath(sys.argv[1])

        tempDir = ".\Temp"
        
        if os.path.isdir(tempDir):
            shutil.rmtree(tempDir)
        os.mkdir(tempDir)
        os.chdir(tempDir)

        downloader = Downloader()
        downloader.Setup(absPath)
    else:
        print("Not have enough args. Example: xxx ./p.json\n")
