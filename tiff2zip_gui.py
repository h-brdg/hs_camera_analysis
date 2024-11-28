import os
import zipfile
import shutil
import tqdm
from read_config_info import read_config_info
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar, QComboBox
)


class TiffZipGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # UI Components
        self.setWindowTitle("TIFF to ZIP Converter")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # ComboBox for Camera Prefix
        self.prefix_label = QLabel("Camera Prefix:")
        self.prefix_combo = QComboBox(self)
        self.prefix_combo.addItems(["test-", "ACS-3 M16 1960-", "ACS-1 M60 1773-"])
        layout.addWidget(self.prefix_label)
        layout.addWidget(self.prefix_combo)

        # Input for Start Shot
        self.start_shot_label = QLabel("Start Shot Number:")
        self.start_shot_input = QLineEdit(self)
        layout.addWidget(self.start_shot_label)
        layout.addWidget(self.start_shot_input)

        # Input for End Shot
        self.end_shot_label = QLabel("End Shot Number:")
        self.end_shot_input = QLineEdit(self)
        layout.addWidget(self.end_shot_label)
        layout.addWidget(self.end_shot_input)

        # Process Button
        self.process_button = QPushButton("Process", self)
        self.process_button.clicked.connect(self.process_shots)
        layout.addWidget(self.process_button)
        
        # Progress Bar
        self.progress_bar_label = QLabel("Progress:")
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def tiff2Zip(self, prefix, shot):
        # Target shot dir
        config_dict = read_config_info()
        tiff_dir = config_dict['tiff_dir']

        if os.path.exists(os.path.join(tiff_dir, str(shot) + "_tif.zip")):
            QMessageBox.warning(self, "Warning", f"{str(shot) + '_tif.zip'} already exists.")
            return

        elif not os.path.exists(os.path.join(tiff_dir, str(prefix) + str(shot))):
            QMessageBox.warning(self, "Warning", f"{str(prefix) + str(shot)} does not exist.")
            return

        elif os.path.exists(os.path.join(tiff_dir, str(prefix) + str(shot))):
            img_list = os.listdir(os.path.join(tiff_dir, str(prefix) + str(shot)))
            zip_path = os.path.join(tiff_dir, str(prefix) + str(shot), str(shot) + "_tif.zip")
            zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)

            for i in tqdm.tqdm(range(len(img_list) - 1)):
                img_name = str(prefix) + str(shot) + "_" + str(i).zfill(8) + ".tif"
                zip.write(
                    os.path.join(tiff_dir, str(prefix) + str(shot), img_name),
                    img_name,
                )
                self.progress_bar.setValue((i + 1) / len(img_list) * 100)

            zip.close()
            shutil.move(zip_path, tiff_dir)
            shutil.copy(
                os.path.join(tiff_dir, str(prefix) + str(shot), str(prefix) + str(shot) + "_tif.txt"),
                os.path.join(tiff_dir, str(shot) + "_tif.txt"),
            )
            shutil.rmtree(os.path.join(tiff_dir, str(prefix) + str(shot)))

    def process_shots(self):
        prefix = self.prefix_combo.currentText()
        try:
            start_shot = int(self.start_shot_input.text())
            end_shot = int(self.end_shot_input.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numbers for start and end shot.")
            return

        for shot in range(start_shot, end_shot + 1):
            try:
                self.tiff2Zip(prefix, shot)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        QMessageBox.information(self, "Success", "All shots processed successfully!")
        self.progress_bar.setValue(100)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    gui = TiffZipGUI()
    gui.show()
    sys.exit(app.exec_())
