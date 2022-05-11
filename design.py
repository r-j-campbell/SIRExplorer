from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from canvas_functions import *

def layouts(self):
    self.main_layout = QHBoxLayout()
    self.setLayout(self.main_layout)
    self.left_layout = QVBoxLayout() #control panel
    self.right_layout = QVBoxLayout() #canvas
    self.main_layout.addLayout(self.left_layout,20)
    self.main_layout.addLayout(self.right_layout,80)
    #control panel
    self.tabs = QTabWidget()
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.tabs.addTab(self.tab1,"File manager")
    self.tabs.addTab(self.tab2,"Map options")
    self.tabs.addTab(self.tab3,"Plot options")
    self.left_layout.addWidget(self.tabs)
    #tab1
    self.tab1Layout = QVBoxLayout()
    self.tab1Layout.addWidget(self.btn_folder_search)
    self.tab1Layout.addWidget(self.select_folder)
    self.tab1Layout.addWidget(self.model2_checkbutton)
    self.tab1Layout.addWidget(self.mac1_checkbutton)
    self.tab1Layout.addWidget(self.mac2_checkbutton)
    self.tab1Layout.addWidget(self.chi2_checkbutton)
    self.tab1Layout.addWidget(self.binary_checkbutton)

    self.tab1Layout.addWidget(self.autofill_btn)

    self.tab1Layout.addWidget(self.model1_btn)
    self.tab1Layout.addWidget(self.select_model1)

    self.tab1Layout.addWidget(self.syn_prof_btn)
    self.tab1Layout.addWidget(self.select_syn_prof)

    self.tab1Layout.addWidget(self.obs_prof_btn)
    self.tab1Layout.addWidget(self.select_obs_prof)

    self.tab1Layout.addWidget(self.model2_btn)
    self.tab1Layout.addWidget(self.select_model2)

    self.tab1Layout.addWidget(self.mac1_btn)
    self.tab1Layout.addWidget(self.select_mac1)

    self.tab1Layout.addWidget(self.mac2_btn)
    self.tab1Layout.addWidget(self.select_mac2)

    self.tab1Layout.addWidget(self.chi2_btn)
    self.tab1Layout.addWidget(self.select_chi2)

    self.tab1Layout.addWidget(self.binary_btn)
    self.tab1Layout.addWidget(self.select_binary)

    self.tab1Layout.addStretch(1)
    self.tab1.setLayout(self.tab1Layout)
    #tab2
    self.tab2Layout = QVBoxLayout()
    self.tab2Layout.addWidget(self.Stokes_checkbutton)
    self.tab2Layout.addWidget(self.T_checkbutton)
    self.tab2Layout.addWidget(self.B_checkbutton)
    self.tab2Layout.addWidget(self.V_checkbutton)
    self.tab2Layout.addWidget(self.G_checkbutton)
    self.tab2Layout.addWidget(self.A_checkbutton)
    self.tab2Layout.addWidget(self.clear_map_btn)
    self.tab2Layout.addWidget(self.colour_table_options_btn)
    self.tab2Layout.addStretch(1)
    self.tab2.setLayout(self.tab2Layout)
    #tab3
    self.tab3Layout = QVBoxLayout()
    self.tab3Layout.addWidget(self.pI_checkbutton)
    self.tab3Layout.addWidget(self.pQ_checkbutton)
    self.tab3Layout.addWidget(self.pU_checkbutton)
    self.tab3Layout.addWidget(self.pV_checkbutton)
    self.tab3Layout.addWidget(self.clear_profiles_btn)
    self.tab3Layout.addWidget(self.mT_checkbutton)
    self.tab3Layout.addWidget(self.mB_checkbutton)
    self.tab3Layout.addWidget(self.mV_checkbutton)
    self.tab3Layout.addWidget(self.mG_checkbutton)
    self.tab3Layout.addWidget(self.clear_models_btn)
    self.tab3Layout.addStretch(1)
    self.tab3.setLayout(self.tab3Layout)

    #display
    self.left_layout.addWidget(self.btnDisplay)

    #canvas
    self.oneWidget = QWidget()
    self.twoWidget = QWidget()
    self.oneWidget.setLayout(self.right_layout)
    self.twoWidget.setLayout(self.right_layout)
    self.splitter1 = QSplitter(Qt.Vertical)
    self.splitter1.addWidget(self.oneWidget)
    self.splitter1.addWidget(self.twoWidget)
    self.right_layout.addWidget(self.splitter1)

    self.oneLayout = QHBoxLayout() #maps
    self.twoLayout = QVBoxLayout() #plots
    self.oneWidget.setLayout(self.oneLayout)
    self.twoWidget.setLayout(self.twoLayout)

    self.oneLayout.addWidget(self.sc2)
    # self.sc2.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc2.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc2.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc2.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.twoLayout.addWidget(self.sc3)
    # self.sc3.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc3.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc3.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    # self.sc3.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)

    self.threeWidget = QWidget()
    self.threeWidget.setLayout(self.right_layout)
    self.splitter2 = QSplitter(Qt.Horizontal)
    self.splitter2.addWidget(self.threeWidget)
    self.splitter2.addWidget(self.splitter1)
    self.right_layout.addWidget(self.splitter2)

    self.threeLayout = QHBoxLayout() #maps
    self.threeWidget.setLayout(self.threeLayout)

    self.threeLayout.addWidget(self.sc1)

    self.right_bottom_layout = QHBoxLayout()
    self.right_layout.addLayout(self.right_bottom_layout)

    self.frame_layout = QHBoxLayout()
    self.right_bottom_layout.addLayout(self.frame_layout)
    self.wl_layout = QHBoxLayout()
    self.right_bottom_layout.addLayout(self.wl_layout)
    self.optical_depth_layout = QHBoxLayout()
    self.right_bottom_layout.addLayout(self.optical_depth_layout)
    self.frame_layout.addWidget(self.frame_label)
    self.frame_layout.addWidget(self.frame_scale)
    self.wl_layout.addWidget(self.wl_label)
    self.wl_layout.addWidget(self.wl_scale)
    self.optical_depth_layout.addWidget(self.optical_depth_label)
    self.optical_depth_layout.addWidget(self.optical_depth_scale)

def widgets(self):
    #-------widgets for control panel-------#
    self.btnDisplay = QPushButton("Display dataset")
    self.btnDisplay.clicked.connect(lambda checked: self.change_canvas())

    #-------tab1-------#
    self.btn_folder_search = QPushButton("Search for folder")
    self.btn_folder_search.clicked.connect(lambda checked: self.get_folder())

    self.select_folder = QComboBox(self)

    self.model2_checkbutton = QCheckBox("Include 2 models",self)
    self.mac1_checkbutton = QCheckBox("Include primary macroturbulence",self)
    self.mac2_checkbutton = QCheckBox("Include secondary macroturbulence",self)
    self.chi2_checkbutton = QCheckBox("Include chi^2",self)
    self.binary_checkbutton = QCheckBox("Include binary map",self)

    self.clear_map_btn = QPushButton("Update maps")
    self.clear_map_btn.clicked.connect(lambda checked: clear_fig1(self))

    self.colour_table_options_btn = QPushButton("Colour table options")
    self.colour_table_options_btn.clicked.connect(lambda checked: self.colour_table_options())

    self.clear_profiles_btn = QPushButton("Update profiles axes")
    self.clear_profiles_btn.clicked.connect(lambda checked: clear_fig2(self))
    self.clear_models_btn = QPushButton("Update models axes")
    self.clear_models_btn.clicked.connect(lambda checked: clear_fig3(self))

    self.autofill_btn = QPushButton("Autofill")
    self.autofill_btn.clicked.connect(lambda checked: self.autofill())

    self.model1_btn = QPushButton("Search for model files")
    self.model1_btn.clicked.connect(lambda checked: self.get_model1())
    self.select_model1 = QComboBox(self)
    self.syn_prof_btn = QPushButton("Search for synthetic profile files")
    self.syn_prof_btn.clicked.connect(lambda checked: self.get_syn_prof())
    self.select_syn_prof = QComboBox(self)
    self.obs_prof_btn = QPushButton("Search for observed profile files")
    self.obs_prof_btn.clicked.connect(lambda checked: self.get_obs_prof())
    self.select_obs_prof = QComboBox(self)
    self.model2_btn = QPushButton("Search for secondary model files")
    self.model2_btn.clicked.connect(lambda checked: self.get_model2())
    self.select_model2 = QComboBox(self)
    self.mac1_btn = QPushButton("Search for primary macroturbulence files")
    self.mac1_btn.clicked.connect(lambda checked: self.get_mac1())
    self.select_mac1 = QComboBox(self)
    self.mac2_btn = QPushButton("Search for secondary macroturbulence files")
    self.mac2_btn.clicked.connect(lambda checked: self.get_mac2())
    self.select_mac2 = QComboBox(self)
    self.chi2_btn = QPushButton("Search for chi^2 files")
    self.chi2_btn.clicked.connect(lambda checked: self.get_chi2())
    self.select_chi2 = QComboBox(self)
    self.binary_btn = QPushButton("Search for binary map files")
    self.binary_btn.clicked.connect(lambda checked: self.get_binary())
    self.select_binary = QComboBox(self)

    #-------tab2-------#
    self.Stokes_checkbutton = QCheckBox("Show observed profiles",self)
    self.Stokes_checkbutton.setChecked(True)
    self.T_checkbutton = QCheckBox("Show temperature",self)
    self.T_checkbutton.setChecked(True)
    self.B_checkbutton = QCheckBox("Show magnetic field strength/flux",self)
    self.B_checkbutton.setChecked(True)
    self.V_checkbutton = QCheckBox("Show velocity",self)
    self.V_checkbutton.setChecked(True)
    self.G_checkbutton = QCheckBox("Show inclination",self)
    self.G_checkbutton.setChecked(True)
    self.A_checkbutton = QCheckBox("Show azimuth",self)
    self.A_checkbutton.setChecked(True)
    #-------tab3-------#
    self.pI_checkbutton = QCheckBox("Show Stokes I",self)
    self.pI_checkbutton.setChecked(True)
    self.pQ_checkbutton = QCheckBox("Show Stokes Q",self)
    self.pQ_checkbutton.setChecked(True)
    self.pU_checkbutton = QCheckBox("Show Stokes U",self)
    self.pU_checkbutton.setChecked(True)
    self.pV_checkbutton = QCheckBox("Show Stokes V",self)
    self.pV_checkbutton.setChecked(True)

    self.mT_checkbutton = QCheckBox("Show temperature",self)
    self.mT_checkbutton.setChecked(True)
    self.mB_checkbutton = QCheckBox("Show magnetic field strength/flux",self)
    self.mB_checkbutton.setChecked(True)
    self.mV_checkbutton = QCheckBox("Show velocity",self)
    self.mV_checkbutton.setChecked(True)
    self.mG_checkbutton = QCheckBox("Show inclination/azimuth",self)
    self.mG_checkbutton.setChecked(True)

    #-------widgets for canvas-------#
    self.sc1 = MplCanvas1(self, width=5, height=4, dpi=100)
    self.sc1.fig1.canvas.mpl_connect('button_press_event', self.mouseclicks)
    self.sc2 = MplCanvas2(self, width=5, height=4, dpi=100)
    self.sc3 = MplCanvas3(self, width=5, height=4, dpi=100)

    self.frame_scale = QSlider(Qt.Horizontal)
    self.frame_scale.sliderReleased.connect(lambda: change_frame(self))
    self.frame_scale.valueChanged.connect(lambda: update_frame_label(self))
    self.frame_label = QLabel("FR: " + str(self.frame_scale.value()),self)
    self.wl_scale = QSlider(Qt.Horizontal)
    self.wl_scale.sliderReleased.connect(lambda: change_wl(self))
    self.wl_scale.valueChanged.connect(lambda: update_wl_label(self))
    self.wl_label = QLabel("WL: " + str(self.wl_scale.value()),self)
    self.optical_depth_scale = QSlider(Qt.Horizontal)
    self.optical_depth_scale.sliderReleased.connect(lambda: change_optical_depth(self))
    self.optical_depth_scale.valueChanged.connect(lambda: update_optical_depth_label(self))
    self.optical_depth_label = QLabel("OD: " + str(self.optical_depth_scale.value()),self)

def update_frame_label(self):
    self.frame_label.setText("FR: " + str(self.frame_scale.value()))
def update_wl_label(self):
    self.wl_label.setText("WL: " + str(self.wl_scale.value()))
def update_optical_depth_label(self):
    self.optical_depth_label.setText("OD: " + str(self.optical_depth_scale.value()))

class MplCanvas1(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig1 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas1, self).__init__(self.fig1)
class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig2 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas2, self).__init__(self.fig2)
class MplCanvas3(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig3 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas3, self).__init__(self.fig3)


def colour_table_layouts(self,sire):
    self.colour_table_layout = QGridLayout() #row,col

    self.colour_table_layout.addWidget(self.CT_empty_label,0,0)
    self.colour_table_layout.addWidget(self.CT_StkI_label,1,0)
    self.colour_table_layout.addWidget(self.CT_T_label,2,0)
    self.colour_table_layout.addWidget(self.CT_B_label,3,0)
    self.colour_table_layout.addWidget(self.CT_V_label,4,0)
    self.colour_table_layout.addWidget(self.CT_G_label,5,0)
    self.colour_table_layout.addWidget(self.CT_A_label,6,0)

    self.colour_table_layout.addWidget(self.CT_label,0,1)
    self.colour_table_layout.addWidget(self.CT_StkI,1,1)
    self.colour_table_layout.addWidget(self.CT_T,2,1)
    self.colour_table_layout.addWidget(self.CT_B,3,1)
    self.colour_table_layout.addWidget(self.CT_V,4,1)
    self.colour_table_layout.addWidget(self.CT_G,5,1)
    self.colour_table_layout.addWidget(self.CT_A,6,1)

    self.colour_table_layout.addWidget(self.CT_vmin_label,0,2)
    self.colour_table_layout.addWidget(self.CT_StkI_vmin,1,2)
    self.colour_table_layout.addWidget(self.CT_T_vmin,2,2)
    self.colour_table_layout.addWidget(self.CT_B_vmin,3,2)
    self.colour_table_layout.addWidget(self.CT_V_vmin,4,2)
    self.colour_table_layout.addWidget(self.CT_G_vmin,5,2)
    self.colour_table_layout.addWidget(self.CT_A_vmin,6,2)

    self.colour_table_layout.addWidget(self.CT_vmax_label,0,3)
    self.colour_table_layout.addWidget(self.CT_StkI_vmax,1,3)
    self.colour_table_layout.addWidget(self.CT_T_vmax,2,3)
    self.colour_table_layout.addWidget(self.CT_B_vmax,3,3)
    self.colour_table_layout.addWidget(self.CT_V_vmax,4,3)
    self.colour_table_layout.addWidget(self.CT_G_vmax,5,3)
    self.colour_table_layout.addWidget(self.CT_A_vmax,6,3)

    self.colour_table_layout.addWidget(self.CT_StkI_autoscaling_checkbutton,1,4)
    self.colour_table_layout.addWidget(self.CT_T_autoscaling_checkbutton,2,4)
    self.colour_table_layout.addWidget(self.CT_B_autoscaling_checkbutton,3,4)
    self.colour_table_layout.addWidget(self.CT_V_autoscaling_checkbutton,4,4)
    self.colour_table_layout.addWidget(self.CT_G_autoscaling_checkbutton,5,4)
    self.colour_table_layout.addWidget(self.CT_A_autoscaling_checkbutton,6,4)

    self.colour_table_layout.addWidget(self.update_and_set,7,0)

    self.setLayout(self.colour_table_layout)
def colour_table_widgets(self,sire):
    self.CT_empty_label = QLabel(" ")
    self.CT_StkI_label = QLabel("Stokes ")
    self.CT_T_label = QLabel("Temperature ")
    self.CT_B_label = QLabel("Magnetic field str./flux dens.")
    self.CT_V_label = QLabel("Velocity")
    self.CT_G_label = QLabel("Inclination ")
    self.CT_A_label = QLabel("Azimuth ")

    self.CT_label = QLabel("Colour tables")
    self.CT_StkI = QComboBox(self)
    set_CT_combos(self.CT_StkI,sire.I_CT[0],sire.CT_options)
    self.CT_T = QComboBox(self)
    set_CT_combos(self.CT_T,sire.T_CT[0],sire.CT_options)
    self.CT_B = QComboBox(self)
    set_CT_combos(self.CT_B,sire.B_CT[0],sire.CT_options)
    self.CT_V = QComboBox(self)
    set_CT_combos(self.CT_V,sire.V_CT[0],sire.CT_options)
    self.CT_G = QComboBox(self)
    set_CT_combos(self.CT_G,sire.G_CT[0],sire.CT_options)
    self.CT_A = QComboBox(self)
    set_CT_combos(self.CT_A,sire.A_CT[0],sire.CT_options)

    self.CT_vmin_label = QLabel("Vmin")
    self.CT_StkI_vmin = QLineEdit(self)
    self.CT_StkI_vmin.setText(str(sire.I_CT[1]))
    self.CT_StkI_vmin.setEnabled(False)
    self.CT_T_vmin = QLineEdit(self)
    self.CT_T_vmin.setText(str(sire.T_CT[1]))
    self.CT_T_vmin.setEnabled(False)
    self.CT_B_vmin = QLineEdit(self)
    self.CT_B_vmin.setText(str(sire.B_CT[1]))
    self.CT_B_vmin.setEnabled(False)
    self.CT_V_vmin = QLineEdit(self)
    self.CT_V_vmin.setText(str(sire.V_CT[1]))
    self.CT_V_vmin.setEnabled(False)
    self.CT_G_vmin = QLineEdit(self)
    self.CT_G_vmin.setText(str(sire.G_CT[1]))
    self.CT_G_vmin.setEnabled(False)
    self.CT_A_vmin = QLineEdit(self)
    self.CT_A_vmin.setText(str(sire.A_CT[1]))
    self.CT_A_vmin.setEnabled(False)

    self.CT_vmax_label = QLabel("Vmax")
    self.CT_StkI_vmax = QLineEdit(self)
    self.CT_StkI_vmax.setText(str(sire.I_CT[2]))
    self.CT_StkI_vmax.setEnabled(False)
    self.CT_T_vmax = QLineEdit(self)
    self.CT_T_vmax.setText(str(sire.T_CT[2]))
    self.CT_T_vmax.setEnabled(False)
    self.CT_B_vmax = QLineEdit(self)
    self.CT_B_vmax.setText(str(sire.B_CT[2]))
    self.CT_B_vmax.setEnabled(False)
    self.CT_V_vmax = QLineEdit(self)
    self.CT_V_vmax.setText(str(sire.V_CT[2]))
    self.CT_V_vmax.setEnabled(False)
    self.CT_G_vmax = QLineEdit(self)
    self.CT_G_vmax.setText(str(sire.G_CT[2]))
    self.CT_G_vmax.setEnabled(False)
    self.CT_A_vmax = QLineEdit(self)
    self.CT_A_vmax.setText(str(sire.A_CT[2]))
    self.CT_A_vmax.setEnabled(False)

    self.CT_StkI_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_StkI_autoscaling_checkbutton.setChecked(sire.I_CT[3])
    self.CT_StkI_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_StkI_vmin, self.CT_StkI_vmax, self.CT_StkI_autoscaling_checkbutton))
    self.CT_T_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_T_autoscaling_checkbutton.setChecked(sire.T_CT[3])
    self.CT_T_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_T_vmin, self.CT_T_vmax, self.CT_T_autoscaling_checkbutton))
    self.CT_B_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_B_autoscaling_checkbutton.setChecked(sire.B_CT[3])
    self.CT_B_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_B_vmin, self.CT_B_vmax, self.CT_B_autoscaling_checkbutton))
    self.CT_V_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_V_autoscaling_checkbutton.setChecked(sire.V_CT[3])
    self.CT_V_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_V_vmin, self.CT_V_vmax, self.CT_V_autoscaling_checkbutton))
    self.CT_G_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_G_autoscaling_checkbutton.setChecked(sire.G_CT[3])
    self.CT_G_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_G_vmin, self.CT_G_vmax, self.CT_G_autoscaling_checkbutton))
    self.CT_A_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_A_autoscaling_checkbutton.setChecked(sire.A_CT[3])
    self.CT_A_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_A_vmin, self.CT_A_vmax, self.CT_A_autoscaling_checkbutton))

    self.update_and_set = QPushButton("Set values and display")
    self.update_and_set.clicked.connect(lambda: update_and_set(self,sire))

def set_CT_combos(combo,text,items):
    combo.addItems(items)
    index = combo.findText(text, Qt.MatchFixedString) #-1 if no match
    if index >= 0:
        combo.setCurrentIndex(index)

def CT_state_changed(widget1, widget2, checkbutton):
    if checkbutton.isChecked():
        widget1.setEnabled(False)
        widget2.setEnabled(False)
    else:
        widget1.setEnabled(True)
        widget2.setEnabled(True)

def update_and_set(self,sire):
    sire.I_CT[0] = self.CT_StkI.currentText()
    sire.T_CT[0] = self.CT_T.currentText()
    sire.B_CT[0] = self.CT_B.currentText()
    sire.V_CT[0] = self.CT_V.currentText()
    sire.G_CT[0] = self.CT_G.currentText()
    sire.A_CT[0] = self.CT_A.currentText()

    if self.CT_StkI_autoscaling_checkbutton.isChecked():
        sire.I_CT[3] = 1
    else:
        sire.I_CT[3] = 0
        sire.I_CT[1] = self.CT_StkI_vmin.text()
        sire.I_CT[2] = self.CT_StkI_vmax.text()
    if self.CT_T_autoscaling_checkbutton.isChecked():
        sire.T_CT[3] = 1
    else:
        sire.T_CT[3] = 0
        sire.T_CT[1] = self.CT_T_vmin.text()
        sire.T_CT[2] = self.CT_T_vmax.text()
    if self.CT_B_autoscaling_checkbutton.isChecked():
        sire.B_CT[3] = 1
    else:
        sire.B_CT[3] = 0
        sire.B_CT[1] = self.CT_B_vmin.text()
        sire.B_CT[2] = self.CT_B_vmax.text()
    if self.CT_V_autoscaling_checkbutton.isChecked():
        sire.V_CT[3] = 1
    else:
        sire.V_CT[3] = 0
        sire.V_CT[1] = self.CT_V_vmin.text()
        sire.V_CT[2] = self.CT_V_vmax.text()
    if self.CT_G_autoscaling_checkbutton.isChecked():
        sire.G_CT[3] = 1
    else:
        sire.G_CT[3] = 0
        sire.G_CT[1] = float(self.CT_G_vmin.text())
        sire.G_CT[2] = float(self.CT_G_vmax.text())
    if self.CT_A_autoscaling_checkbutton.isChecked():
        sire.A_CT[3] = 1
    else:
        sire.A_CT[3] = 0
        sire.A_CT[1] = self.CT_A_vmin.text()
        sire.A_CT[2] = self.CT_A_vmax.text()

    clear_fig1(sire)




