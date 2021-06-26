#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SchoolSelect import *
from Planner import *

class InitApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):

        # If first run of program, create file for school names and uuids
        if not os.path.isfile("SchoolNames.json"):
            with open("SchoolNames.json", mode = "a+") as f:
                self.data = {"Schools": []}
                f.write(json.dumps(self.data, indent = 2))

        self.openMain()

    def openMain(self):
        self.mainWindow = Planner()


if __name__ == "__main__":

    # Set up main application
    app = QApplication(sys.argv)
    MainApp = InitApp()
    sys.exit(app.exec_())