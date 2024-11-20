import sys
import numpy as np
import matplotlib.pyplot as plt
import configparser
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QFileDialog)
from PyQt5.QtGui import QPixmap, QImage
from calc_int import calc_int  # Import calc_int from calc_int.py

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        self.formLayout = QFormLayout()
        self.shotNoEdit = QLineEdit(self)
        self.lineChEdit = QLineEdit(self)
        self.frameTgtEdit = QLineEdit(self)
        
        self.formLayout.addRow("Shot No:", self.shotNoEdit)
        self.formLayout.addRow("Line Ch:", self.lineChEdit)
        self.formLayout.addRow("Frame Target:", self.frameTgtEdit)
        self.layout.addLayout(self.formLayout)

        self.loadButton = QPushButton("Load Sample Image", self)
        self.loadButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.loadButton)

        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)

        self.formLayout2 = QFormLayout()
        self.leftEdit = QLineEdit(self)
        self.rightEdit = QLineEdit(self)
        self.topEdit = QLineEdit(self)
        self.bottomEdit = QLineEdit(self)
        
        self.formLayout2.addRow("Left:", self.leftEdit)
        self.formLayout2.addRow("Right:", self.rightEdit)
        self.formLayout2.addRow("Top:", self.topEdit)
        self.formLayout2.addRow("Bottom:", self.bottomEdit)
        self.layout.addLayout(self.formLayout2)
        
        self.saveButton = QPushButton("Save Config", self)
        self.saveButton.clicked.connect(self.saveConfig)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)
        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 800, 600)

    def loadImage(self):
        shot_no = int(self.shotNoEdit.text())
        line_ch = self.lineChEdit.text()
        frame_tgt = int(self.frameTgtEdit.text())
        num_frames = 1

        camera_dict_int = calc_int(shot_no, line_ch, frame_tgt, num_frames)
        data = camera_dict_int['data']

        frames, height, width = data.shape
        data = (data - data.min()) / (data.max() - data.min()) * 255
        data = data.astype(np.uint8)
        qimg = QImage(data.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.imageLabel.setPixmap(pixmap)

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