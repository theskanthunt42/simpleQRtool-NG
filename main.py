#Main stuff goes here
#Importing some stuff that will be use in here
from _typeshed import NoneType
from ctypes import util
import os
import sys
import json
import ui
import libs.utils
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
        self.main_exec.clicked.connect(self.ConvertTrigger)
        self.import_exec.clicked.connect(self.ImportTrigger)
        self.export_exec.clicked.connect(self.ExportTrigger)
        self.export_exec_2.triggered.connect(self.ExportTrigger)
        self.size_auto_button.toggled.connect(self.SizeModeAuto)
        self.size_manual_button.toggled.connect(self.SizeModeManual)
        self.size_slider.valueChanged.connect(self.SliderChangedHandler)
        self.action_exit.trigger.connect(self.exit)

#Use to handle mode switch

    def InfoOutput(self, logs, terminal, stat_bar, stat_bar_time):
        self.all_logs = self.all_logs + str(logs) +'\n'
        if terminal == True:
            print(logs)
        else:
            pass
        if stat_bar == True and stat_bar_time != None or 0:
            self.statusBar.showMessage(logs, stat_bar_time)
        else:
            pass
    
#Exit handler

    def exit(self):
        self.InfoOutput(logs='Exit triggered.', terminal=True,
                        stat_bar=False, stat_bar_time=0)
        with open(f'{self.current_path}{self.os_seprator}logs.txt', 'w') as f:
            f.write(self.all_logs)
        raise SystemExit


    def mode_q2t(self):
        #Disable all widgets that wont need
        radio_button = self.sender()
        if radio_button.isChecked():
            self.current_mode = 'q2t'
            self.export_exec.setEnabled(False)
            self.main_exec.setEnabled(False)
            self.import_exec.setEnabled(False)
            self.encoding_utf8.setEnabled(False)
            self.encoding_ascii.setEnabled(False)
            self.encoding_shift.setEnabled(False)
            self.size_auto_button.setEnabled(False)
            self.size_manual_button.setEnabled(False)
            self.size_slider.setEnabled(False)
        return None
    
#Same as up

    def mode_t2q(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.current_mode = 't2q'
            self.main_exec.setEnabled(True)
            self.import_exec.setEnabled(False)
            self.export_exec(True)
            self.encoding_shift.setEnabled(True)
            self.encoding_utf8.setEnabled(True)
            self.encoding_ascii.setEnabled(True)
            self.size_auto_button.setEnabled(True)
            self.size_manual_button.setEnabled(True)
            self.size_slider.setEnabled(True)
        return None

    def EncodingModeUnicode(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.text_encoding = 'utf-8'
        return None
    
    def EncodingModeASCII(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.text_encoding = 'ascii'
        return None

    def EncodingModeJIS(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.text_encoding = 'shift-jis'
        return None

#Using QFileDialog to import PNGs

    def ImportTrigger(self):
        self.FileDialog = QFileDialog.getOpenFileName(
            self, 'Open file', self.current_path, 'PNG files (*.png)')
        self.full_path = self.FileDialog[0]
        self.file_imported_stats = True
        self.InfoOutput(f'Selected file: {self.full_path}',
                        terminal=True, stat_bar=True, stat_bar_time=1500
        )
        self.MainDecoder(self.full_path)
        return None

    def SliderChangedHandler(self, value):
        self.image_size = value
        self.InfoOutput(
            logs=f'Size changed to {self.image_size}', terminal=True, stat_bar=True, stat_bar_time=1500)
        return None
    
    def SizeAutoMode(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.auto_mode_stats = True
            self.size_slider.setEnabled(True)
        return None
    
    def SizeModeManual(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.auto_mode_stats = False
            self.size_slider.setEnabled(True)
        return None

    def MainDecoder(self, file_path):
        if self.file_imported_stats:
            self.pixmap_label.setPixmap(QPixmap(file_path))
            data = libs.utils.Decoder(file_path)
            if type(data) != NoneType:
                self.text_box.setText(data)
            else:
                self.InfoOutput("Can't decode QR Code!", True, True, 1500)
        else:
            self.InfoOutput('Please import QR Code first!', True, True, 2000)
        return None

    def MainEncoder(self, text):
        #print('Place holder.')
        size = None
        #JSON stuff goes here
        loaded_config = libs.utils.Config_Loader('config.json')
        if loaded_config != NoneType:
            pass
        else:
            self.InfoOutput("Can't load the config.json as a config file!", True, True, 2000)
        raise SystemError
    if self.auto_mode_stats != True:
        size = None
    else:
        size = self.size_slider.value()
    try:
        self.saved_file_name = libs.utils.Encoder(loaded_config, size, text, self.text_encoding)
        self.pixmap_label.setPixmap(QPixmap(self.saved_file_name))
        self.generated_stats = True
    except SystemError:
        self.InfoOutput("Error when generating QR Code.", True, True, 2000)

    def ConvertTrigger(self):
        self.text_in_box = self.text_box.toPlainText()
        if self.text_in_box != '' or None:
            self.MainEncoder(self.text_in_box)
        else:
            self.InfoOutput('Please at least fill some text to the box.', True, True, 2000)
        return None


