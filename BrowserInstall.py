import os, shutil, glob
from zipfile import ZipFile
from urllib import request
from Configuration import Configuration

class BrowserInstall:
    def __init__(self, debug=False):
        self.directory = os.getcwd()+"\\browser"
        self.path = self.directory+"\\browser.zip"
        os.makedirs(self.directory, exist_ok=True)
        self.debug = debug

    def DownloadAndExtract(self):
        if not self.debug:
            page = 'https://www.firefox-usb.com/download/FirefoxPortable64-51.0.1.zip'
            with request.urlopen(page) as response, open(self.path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        zip = ZipFile(self.path, 'r')
        zip.extractall(self.directory)
        zip.close()
        if not self.debug:
            os.unlink(self.path)
        locations = glob.glob(self.directory+'\\**\\*.exe', recursive=True)
        if len(locations) == 0:
            raise Exception("Failed to install browser")
        self.browserExe = locations[0]
        Configuration().installBrowser("firefox", ".*Mozilla.*", self.browserExe)
