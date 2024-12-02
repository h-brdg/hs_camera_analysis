import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from plot_camera_int_test import plot_camera_int_frame
from plot_camera_ratio_test import plot_camera_ratio_frame
from plot_camera_int_avg_test import plot_camera_int_avg
from plot_camera_ratio_avg_test import plot_camera_ratio_avg

class PlotCameraFrameGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Function Selection for Camera Data Plot')

        # Create layout
        layout = QVBoxLayout()
        
        # Function Selection
        hbox_function = QHBoxLayout()
        lbl_function = QLabel('Function:', self)
        self.combo_function = QComboBox(self)
        self.combo_function.addItems(["plot_camera_int_frame", "plot_camera_int_avg", "plot_camera_ratio_frame", "plot_camera_ratio_avg"])
        hbox_function.addWidget(lbl_function)
        hbox_function.addWidget(self.combo_function)
        layout.addLayout(hbox_function)
        
        # Button to move to plot UI
        self.btn_plot = QPushButton('Proceed', self)
        self.btn_plot.clicked.connect(self.plotUI)
        layout.addWidget(self.btn_plot)
        
        self.setLayout(layout)

    def plotUI(self):
        self.setWindowTitle('Plot Camera Data')    
        
        # # Clear the existing layout and widgets properly
        # while self.layout().count():
        #     child = self.layout().takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()
        #     elif child.layout():
        #         while child.layout().count():
        #             sub_child = child.layout().takeAt(0)
        #             if sub_child.widget():
        #                 sub_child.widget().deleteLater()
    
        # Reuse the existing main layout
        
        self.btn_plot.hide()
        
        layout = self.layout()
    
        # Display chosen function
        chosen_function = self.combo_function.currentText()
        lbl_chosen_function = QLabel(f'Selected Function: {chosen_function}', self)
        layout.addWidget(lbl_chosen_function)
    
        # Shot No
        hbox_shot_no = QHBoxLayout()
        lbl_shot_no = QLabel('Shot No:', self)
        self.txt_shot_no = QLineEdit(self)
        hbox_shot_no.addWidget(lbl_shot_no)
        hbox_shot_no.addWidget(self.txt_shot_no)
        layout.addLayout(hbox_shot_no)
    
        # Line Channel
        hbox_line_ch = QHBoxLayout()
    
        if chosen_function in ["plot_camera_int_frame", "plot_camera_int_avg"]:
            lbl_line_ch = QLabel('Line Channel:', self)
            self.txt_line_ch = QLineEdit(self)
            hbox_line_ch.addWidget(lbl_line_ch)
            hbox_line_ch.addWidget(self.txt_line_ch)
            self.is_ratio = False
        elif chosen_function in ["plot_camera_ratio_frame", "plot_camera_ratio_avg"]:
            lbl_line_ch_numer = QLabel('Line Channel Numerator:', self)
            self.txt_line_ch_numer = QLineEdit(self)
            hbox_line_ch.addWidget(lbl_line_ch_numer)
            hbox_line_ch.addWidget(self.txt_line_ch_numer)
            lbl_line_ch_denom = QLabel('Line Channel Denominator:', self)
            self.txt_line_ch_denom = QLineEdit(self)
            hbox_line_ch.addWidget(lbl_line_ch_denom)
            hbox_line_ch.addWidget(self.txt_line_ch_denom)
            self.is_ratio = True
    
        layout.addLayout(hbox_line_ch)
    
        # Frame Target
        hbox_frame_tgt = QHBoxLayout()
        lbl_frame_tgt = QLabel('Frame Target:', self)
        self.txt_frame_tgt = QLineEdit(self)
        hbox_frame_tgt.addWidget(lbl_frame_tgt)
        hbox_frame_tgt.addWidget(self.txt_frame_tgt)
        layout.addLayout(hbox_frame_tgt)
    
        # Number of Frames
        hbox_num_frames = QHBoxLayout()
        lbl_num_frames = QLabel('Number of Frames:', self)
        self.txt_num_frames = QLineEdit(self)
        hbox_num_frames.addWidget(lbl_num_frames)
        hbox_num_frames.addWidget(self.txt_num_frames)
        layout.addLayout(hbox_num_frames)
        
        # Vmin, Vmax
        hbox_vmin_vmax = QHBoxLayout()
        lbl_vmin = QLabel('Vmin:', self)
        self.txt_vmin = QLineEdit(self)
        hbox_vmin_vmax.addWidget(lbl_vmin)
        hbox_vmin_vmax.addWidget(self.txt_vmin)
    
        lbl_vmax = QLabel('Vmax:', self)
        self.txt_vmax = QLineEdit(self)
        hbox_vmin_vmax.addWidget(lbl_vmax)
        hbox_vmin_vmax.addWidget(self.txt_vmax)
        layout.addLayout(hbox_vmin_vmax)
    
        # Average Time
        if chosen_function in ["plot_camera_int_avg", "plot_camera_ratio_avg"]:
            hbox_avg_time = QHBoxLayout()
            lbl_avg_time = QLabel('Average Time:', self)
            self.txt_avg_time = QLineEdit(self)
            hbox_avg_time.addWidget(lbl_avg_time)
            hbox_avg_time.addWidget(self.txt_avg_time)
            layout.addLayout(hbox_avg_time)
            self.is_avg = True
        else:
            self.is_avg = False
    
        # Plot Button
        self.btn_plot = QPushButton('Plot', self)
        self.btn_plot.clicked.connect(self.call_plot_camera_frame)
        layout.addWidget(self.btn_plot)




    def call_plot_camera_frame(self):
        shot_no = int(self.txt_shot_no.text())
        if self.is_ratio:
            line_ch = (self.txt_line_ch_numer.text(),self.txt_line_ch_denom.text())  
        else:
            line_ch = self.txt_line_ch.text()
        frame_tgt = int(self.txt_frame_tgt.text())
        num_frames = int(self.txt_num_frames.text())
        vmin = float(self.txt_vmin.text()) if self.txt_vmin.text() else None
        vmax = float(self.txt_vmax.text()) if self.txt_vmax.text() else None
        if self.is_avg:
            avg_time = float(self.txt_avg_time.text())
        else:
            avg_time = None
        function_name = self.combo_function.currentText()
        if function_name == "plot_camera_int_frame":
            plot_camera_int_frame(shot_no, line_ch, frame_tgt, num_frames, vmin, vmax)
        elif function_name == "plot_camera_int_avg":
            plot_camera_int_avg(shot_no, line_ch, frame_tgt, num_frames, avg_time)
        elif function_name == "plot_camera_ratio_frame":
            plot_camera_ratio_frame(shot_no, line_ch, frame_tgt, num_frames, vmin, vmax)
        elif function_name == "plot_camera_ratio_avg":
            plot_camera_ratio_avg(shot_no, line_ch, frame_tgt, num_frames, vmin, vmax, avg_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotCameraFrameGUI()
    ex.show()
    sys.exit(app.exec_())