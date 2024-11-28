import sys
import numpy as np
import matplotlib.pyplot as plt
import configparser
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QFileDialog, QCheckBox)
from PyQt5.QtGui import QPixmap, QImage
from calc_int import calc_int  # Import calc_int from calc_int.py
from calc_ratio import calc_ratio
from read_trim_info import read_trim_info  # Import read_trim_info from read_trim_info.py

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.formLayoutIni = QFormLayout()

        self.shotNoEdit = QLineEdit(self)
        self.frameTgtEdit = QLineEdit(self)
        
        self.formLayoutIni.addRow("Shot No:", self.shotNoEdit)
        self.formLayoutIni.addRow("Frame Target:", self.frameTgtEdit)
        
        self.flagRotate = QCheckBox(self)
        self.flagRotateDesc = QLabel(self)
        
        self.formLayoutIni.addRow("Transform:", self.flagRotate)
        self.formLayoutIni.addRow(" (for the ratio, they are always transformed)", self.flagRotateDesc)
        self.layout.addLayout(self.formLayoutIni)


        self.formLayoutInt = QFormLayout()
        self.lineChEdit = QLineEdit(self)
        
        self.formLayoutInt.addRow("Line Ch:", self.lineChEdit)
        self.layout.addLayout(self.formLayoutInt)

        self.loadButton = QPushButton("Load Sample Image", self)
        self.loadButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.loadButton)
        
        self.formLayoutRatio = QFormLayout()
        
        self.lineChEdit_numer = QLineEdit(self)
        self.lineChEdit_denom = QLineEdit(self)
        
        self.formLayoutRatio.addRow("Line Ch numerator:", self.lineChEdit_numer)
        self.formLayoutRatio.addRow("Line Ch denominator:", self.lineChEdit_denom)
        self.layout.addLayout(self.formLayoutRatio)

        self.loadRatioButton = QPushButton("Load Sample Ratio", self)
        self.loadRatioButton.clicked.connect(self.loadRatioImage)
        self.layout.addWidget(self.loadRatioButton)
        

        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)

        # self.formLayout2 = QFormLayout()
        # self.leftEdit = QLineEdit(self)
        # self.leftLabel = QLabel(self)
        # self.rightEdit = QLineEdit(self)
        # self.rightLabel = QLabel(self)
        # self.topEdit = QLineEdit(self)
        # self.topLabel = QLabel(self)
        # self.bottomEdit = QLineEdit(self)
        # self.bottomLabel = QLabel(self)
        
        # self.formLayout2.addRow("Left:", self.leftEdit)
        # self.formLayout2.addRow("Current Left:", self.leftLabel)
        # self.formLayout2.addRow("Right:", self.rightEdit)
        # self.formLayout2.addRow("Current Right:", self.rightLabel)
        # self.formLayout2.addRow("Top:", self.topEdit)
        # self.formLayout2.addRow("Current Top:", self.topLabel)
        # self.formLayout2.addRow("Bottom:", self.bottomEdit)
        # self.formLayout2.addRow("Current Bottom:", self.bottomLabel)
        # self.layout.addLayout(self.formLayout2)
        
        # self.loadConfigButton = QPushButton("Load Config", self)
        # self.loadConfigButton.clicked.connect(self.loadConfig)
        # self.layout.addWidget(self.loadConfigButton)
        
        # self.saveButton = QPushButton("Save Config", self)
        # self.saveButton.clicked.connect(self.saveConfig)
        # self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)
        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 800, 600)

    def loadImage(self):
        shot_no = int(self.shotNoEdit.text())
        line_ch = self.lineChEdit.text()
        frame_tgt = int(self.frameTgtEdit.text())
        num_frames = 1
        flg_rot = self.flagRotate.isChecked()
        print(flg_rot)

        camera_dict_int = calc_int(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
        data = camera_dict_int['data']

        frames, height, width = data.shape
        data = (data - data.min()) / (data.max() - data.min()) * 255
        data = data.astype(np.uint8)
        
        # Applying colormap
        colormap = plt.cm.viridis  # Change colormap here
        data_colored = colormap(data / 255.0)
        data_colored = (data_colored[:, :, :, :3] * 255).astype(np.uint8)  # Drop the alpha channel
        
        qimg = QImage(data_colored.data, width, height, width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.imageLabel.setPixmap(pixmap)
        
    def loadRatioImage(self):
        shot_no = int(self.shotNoEdit.text())
        line_ch_numer = self.lineChEdit_numer.text()
        line_ch_denom = self.lineChEdit_denom.text()
        line_ch_li = (line_ch_numer, line_ch_denom)
        frame_tgt = int(self.frameTgtEdit.text())
        num_frames = 1

        camera_dict_ratio = calc_ratio(shot_no, line_ch_li, frame_tgt, num_frames, flg_rot=True)
        data = camera_dict_ratio['data']

        frames, height, width = data.shape
        data = data / data[0, int(height/2), int(width/2)] * 255 * 0.8
        data = data.astype(np.uint8)
        
        # Applying colormap
        colormap = plt.cm.viridis  # Change colormap here
        data_colored = colormap(data / 255.0)
        data_colored = (data_colored[:, :, :, :3] * 255).astype(np.uint8)  # Drop the alpha channel
        
        qimg = QImage(data_colored.data, width, height, width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.imageLabel.setPixmap(pixmap)        

    def loadConfig(self):
        shot_no = int(self.shotNoEdit.text())
        line_ch = self.lineChEdit.text()
        tiff_dir = ""  # Assuming tiff_dir is not used in read_trim_info function
        config = read_trim_info(shot_no, line_ch, tiff_dir)
        if config:
            self.leftLabel.setText(f"(Current value: {config.get('left', '')})")
            self.rightLabel.setText(f"(Current value: {config.get('right', '')})")
            self.topLabel.setText(f"(Current value: {config.get('top', '')})")
            self.bottomLabel.setText(f"(Current value: {config.get('bottom', '')})")
            print("Config loaded:", config)
        else:
            print("Failed to load config")

    def saveConfig(self):
        ini_file, _ = QFileDialog.getSaveFileName(self, "Save Config File", "", "INI Files (*.ini);;All Files (*)")
        if ini_file:
            config = configparser.ConfigParser()
            config.read(ini_file)

            section = "new_section"
            if not config.has_section(section):
                config.add_section(section)

            config.set(section, 'left', self.leftEdit.text())
            config.set(section, 'right', self.rightEdit.text())
            config.set(section, 'top', self.topEdit.text())
            config.set(section, 'bottom', self.bottomEdit.text())

            with open(ini_file, 'w') as configfile:
                config.write(configfile)
            print(f"Config saved to {ini_file}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageEditor()
    ex.show()
    sys.exit(app.exec_())