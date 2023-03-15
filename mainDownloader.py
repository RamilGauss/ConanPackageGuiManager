import os
import sys

import shutil

from Backend.DownloadAndBuild.Downloader import *

if __name__ == '__main__':

    if len(sys.argv) != 1:
        absPath = os.path.abspath(sys.argv[1])

        downloader = Downloader()
        downloader.Setup(absPath)
    else:
        print("Not have enough args. Example: xxx ./p.json\n")
