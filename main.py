#Main stuff goes here
#Importing some stuff that will be use in here
import os
import sys
import json
import ui
#Qt stuff goes here
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QAction, QFileDialog, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap

class SimpleQRTool(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        #Initialize Qt stuff here
        super(SimpleQRTool, self).__init__(parent)
        #Get system platform info here
        self.current_platform = sys.platform
        self.setupUi(self)
        self.current_path = os.getcwd()
        self.os_seprator = os.sep
        self.full_path = ''
        self.logs = '' #Logs that will output as logs.txt
        #Remove logs everytime, Will change this later
        #WORKAROUND
        if os.path.exists(f'{self.current_path}{self.os_seprator}logs.txt'):
            os.remove(f'{self.current_path}{self.os_seprator}logs.txt')
        else:
            print('Clean as fuck, No logs left here.')
        self.generated_stats = False #QR code generated stats
        self.text_encoding = 'utf-8' #Default text encoding
        self.file_imported_stats = False #PNG file imported stats
        self.auto_mode_stats = True #Auto control QR code size stuff
        self.image_size = 1 #QR code size
        #Creating groups for radio buttons
        self.button_group_mode = QButtonGroup()
        self.button_group_encoding = QButtonGroup()
        self.button_group_size = QButtonGroup()
        #Adding buttons to groups
        self.button_group_mode.addButton(self.mode_q2t)
        self.button_group_mode.addButton(self.mode_t2q)
        self.button_group_encoding.addButton(self.encoding_utf8)
        self.button_group_encoding.addButton(self.encoding_ascii)
        self.button_group_encoding.addButton(self.encoding_shift)
        self.button_group_size.addButton(self.size_auto_button)
        self.button_group_size.addButton(self.size_manual_button)
        #Setting default value
        self.size_slider.setEnabled(False)
        self.size_auto_button.setEnabled(True)
        self.mode_t2q.setChecked(True)
        self.encoding_utf8.setChecked(True)
        self.import_exec.setEnabled(False)
        #Toggle connect
        self.mode_t2q.toggled.connect(self.EncodingMode)
        self.mode_q2t.toggled.connect(self.DecodingMode)
        self.encoding_utf8.toggled.connect(self.EncodingModeUnicode)
        self.encoding_ascii.toggled.connect(self.EncodingModeASCII)
        self.encoding_shift.toggled.connect(self.EncodingModeJIS)
        self.action_exit.trigger.connect(self.exit)
        