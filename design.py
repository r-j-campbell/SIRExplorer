from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from canvas_functions import *

def layouts(sire):
    sire.main_layout = QHBoxLayout()
    sire.setLayout(sire.main_layout)
    sire.left_layout = QVBoxLayout() #control panel
    sire.right_layout = QVBoxLayout() #canvas
    sire.main_layout.addLayout(sire.left_layout,20)
    sire.main_layout.addLayout(sire.right_layout,80)
    #control panel
    sire.tabs = QTabWidget()
    sire.tab1 = QWidget()
    sire.tab2 = QWidget()
    sire.tab3 = QWidget()
    sire.tab4 = QWidget()
    sire.tabs.addTab(sire.tab1,"Files")
    sire.tabs.addTab(sire.tab2,"Map options")
    sire.tabs.addTab(sire.tab3,"Plot options")
    sire.tabs.addTab(sire.tab4,"Pixel info")
    sire.left_layout.addWidget(sire.tabs)
    #tab1
    sire.tab1Layout = QVBoxLayout()
    sire.tab1Layout.addWidget(sire.btn_folder_search)
    sire.tab1Layout.addWidget(sire.select_folder)
    sire.tab1Layout.addWidget(sire.model2_checkbutton)
    sire.tab1Layout.addWidget(sire.mac1_checkbutton)
    sire.tab1Layout.addWidget(sire.mac2_checkbutton)
    #sire.tab1Layout.addWidget(sire.chi2_checkbutton)
    sire.tab1Layout.addWidget(sire.binary_checkbutton)

    sire.tab1Layout.addWidget(sire.autofill_btn)

    sire.tab1Layout.addWidget(sire.model1_btn)
    sire.tab1Layout.addWidget(sire.select_model1)

    sire.tab1Layout.addWidget(sire.syn_prof_btn)
    sire.tab1Layout.addWidget(sire.select_syn_prof)

    sire.tab1Layout.addWidget(sire.obs_prof_btn)
    sire.tab1Layout.addWidget(sire.select_obs_prof)

    sire.tab1Layout.addWidget(sire.model2_btn)
    sire.tab1Layout.addWidget(sire.select_model2)

    sire.tab1Layout.addWidget(sire.mac1_btn)
    sire.tab1Layout.addWidget(sire.select_mac1)

    sire.tab1Layout.addWidget(sire.mac2_btn)
    sire.tab1Layout.addWidget(sire.select_mac2)

    sire.tab1Layout.addWidget(sire.binary_btn)
    sire.tab1Layout.addWidget(sire.select_binary)

    sire.tab1Layout.addStretch(1)
    sire.tab1.setLayout(sire.tab1Layout)
    #tab2
    sire.tab2Layout = QVBoxLayout()
    sire.tab2Layout.addWidget(sire.clear_map_btn)
    sire.tab2Layout.addWidget(sire.Stokes_checkbutton)
    sire.tab2Layout.addWidget(sire.Stokes_Q_checkbutton)
    sire.tab2Layout.addWidget(sire.Stokes_U_checkbutton)
    sire.tab2Layout.addWidget(sire.Stokes_V_checkbutton)
    sire.tab2Layout.addWidget(sire.T_checkbutton)
    sire.tab2Layout.addWidget(sire.B_checkbutton)
    sire.tab2Layout.addWidget(sire.V_checkbutton)
    sire.tab2Layout.addWidget(sire.G_checkbutton)
    sire.tab2Layout.addWidget(sire.A_checkbutton)
    sire.tab2Layout.addWidget(sire.colour_table_options_btn)
    sire.tab2Layout.addStretch(1)
    sire.tab2.setLayout(sire.tab2Layout)
    #tab3
    sire.tab3Layout = QVBoxLayout()
    sire.tab3Layout.addWidget(sire.clear_profiles_btn)
    sire.tab3Layout.addWidget(sire.clear_models_btn)
    sire.tab3Layout.addWidget(sire.pI_checkbutton)
    sire.tab3Layout.addWidget(sire.pQ_checkbutton)
    sire.tab3Layout.addWidget(sire.pU_checkbutton)
    sire.tab3Layout.addWidget(sire.pV_checkbutton)
    sire.tab3_wl_min_layout = QHBoxLayout()
    sire.tab3Layout.addLayout(sire.tab3_wl_min_layout)
    sire.tab3_wl_min_layout.addWidget(sire.wl_min_label)
    sire.tab3_wl_min_layout.addWidget(sire.wl_min_entry)
    sire.tab3_wl_min_layout.addWidget(sire.wl_max_label)
    sire.tab3_wl_min_layout.addWidget(sire.wl_max_entry)
    sire.tab3Layout.addWidget(sire.wl_range_btn)
    sire.tab3Layout.addWidget(sire.mT_checkbutton)
    sire.tab3Layout.addWidget(sire.mB_checkbutton)
    sire.tab3Layout.addWidget(sire.mV_checkbutton)
    sire.tab3Layout.addWidget(sire.mG_checkbutton)
    sire.tab3_optical_depth_min_layout = QHBoxLayout()
    sire.tab3Layout.addLayout(sire.tab3_optical_depth_min_layout)
    sire.tab3_optical_depth_min_layout.addWidget(sire.optical_depth_min_label)
    sire.tab3_optical_depth_min_layout.addWidget(sire.optical_depth_min_entry)
    sire.tab3_optical_depth_min_layout.addWidget(sire.optical_depth_max_label)
    sire.tab3_optical_depth_min_layout.addWidget(sire.optical_depth_max_entry)
    sire.tab3Layout.addWidget(sire.optical_depth_range_btn)
    sire.tab3Layout.addStretch(1)
    sire.tab3.setLayout(sire.tab3Layout)

    #tab4
    sire.tab4Layout = QVBoxLayout()
    sire.tab4.setLayout(sire.tab4Layout)
    sire.tab4_grid_layout = QGridLayout()
    sire.tab4Layout.addLayout(sire.tab4_grid_layout)
    sire.tab4_grid_layout.addWidget(sire.parameter_label, 1, 0)
    sire.tab4_grid_layout.addWidget(sire.ff_label, 2, 0)
    sire.tab4_grid_layout.addWidget(sire.T_label, 3, 0)
    sire.tab4_grid_layout.addWidget(sire.B_label, 4, 0)
    sire.tab4_grid_layout.addWidget(sire.V_label, 5, 0)
    sire.tab4_grid_layout.addWidget(sire.G_label, 6, 0)
    sire.tab4_grid_layout.addWidget(sire.A_label, 7, 0)
    sire.tab4_grid_layout.addWidget(sire.mic_label, 8, 0)
    sire.tab4_grid_layout.addWidget(sire.mac_label, 9, 0)
    sire.tab4_grid_layout.addWidget(sire.mod1_label, 1, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_ff_value, 2, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_T_value, 3, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_B_value, 4, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_V_value, 5, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_G_value, 6, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_A_value, 7, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_mic_value, 8, 1)
    sire.tab4_grid_layout.addWidget(sire.mod1_mac_value, 9, 1)
    sire.tab4_grid_layout.addWidget(sire.mod2_label, 1, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_ff_value, 2, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_T_value, 3, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_B_value, 4, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_V_value, 5, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_G_value, 6, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_A_value, 7, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_mic_value, 8, 2)
    sire.tab4_grid_layout.addWidget(sire.mod2_mac_value, 9, 2)
    sire.tab4Layout.addWidget(sire.pixel_values)
    sire.tab4Layout.addStretch(1)

    #display
    sire.left_layout.addWidget(sire.display_btn)
    #preferences
    sire.left_layout.addWidget(sire.preferences_btn)

    #canvas
    sire.oneWidget = QWidget()
    sire.twoWidget = QWidget()
    sire.oneWidget.setLayout(sire.right_layout)
    sire.twoWidget.setLayout(sire.right_layout)
    sire.splitter1 = QSplitter(Qt.Vertical)
    sire.splitter1.addWidget(sire.oneWidget)
    sire.splitter1.addWidget(sire.twoWidget)
    sire.right_layout.addWidget(sire.splitter1)

    sire.oneLayout = QHBoxLayout() #maps
    sire.twoLayout = QVBoxLayout() #plots
    sire.oneWidget.setLayout(sire.oneLayout)
    sire.twoWidget.setLayout(sire.twoLayout)

    sire.oneLayout.addWidget(sire.sc2)
    sire.sc2.setMinimumSize(1,1)
    sire.twoLayout.addWidget(sire.sc3)
    sire.sc3.setMinimumSize(1,1)

    sire.threeWidget = QWidget()
    sire.threeWidget.setLayout(sire.right_layout)
    sire.splitter2 = QSplitter(Qt.Horizontal)
    sire.splitter2.addWidget(sire.threeWidget)
    sire.splitter2.addWidget(sire.splitter1)
    sire.right_layout.addWidget(sire.splitter2)

    sire.threeLayout = QHBoxLayout() #maps
    sire.threeWidget.setLayout(sire.threeLayout)

    sire.threeLayout.addWidget(sire.sc1)
    sire.sc1.setMinimumSize(1,1)

    sire.right_bottom_layout = QHBoxLayout()
    sire.right_layout.addLayout(sire.right_bottom_layout)

    sire.frame_layout = QHBoxLayout()
    sire.right_bottom_layout.addLayout(sire.frame_layout)
    sire.wl_layout = QHBoxLayout()
    sire.right_bottom_layout.addLayout(sire.wl_layout)
    sire.optical_depth_layout = QHBoxLayout()
    sire.right_bottom_layout.addLayout(sire.optical_depth_layout)
    #sire.frame_layout.addWidget(sire.frame_spinbox)
    sire.frame_layout.addWidget(sire.frame_label)
    sire.frame_layout.addWidget(sire.frame_scale)
    #sire.wl_layout.addWidget(sire.wl_spinbox)
    sire.wl_layout.addWidget(sire.wl_label)
    sire.wl_layout.addWidget(sire.wl_scale)
    sire.optical_depth_layout.addWidget(sire.optical_depth_label)
    sire.optical_depth_layout.addWidget(sire.optical_depth_scale)

def widgets(sire):
    #-------widgets for control panel-------#
    sire.display_btn = QPushButton("Display")
    sire.display_btn.clicked.connect(lambda checked: sire.change_canvas())

    sire.preferences_btn = QPushButton("Preferences")
    sire.preferences_btn.clicked.connect(lambda checked: sire.preferences())

    #-------tab1-------#
    sire.btn_folder_search = QPushButton("Search for folder")
    sire.btn_folder_search.clicked.connect(lambda checked: sire.get_folder())

    sire.select_folder = QComboBox(sire)

    sire.model2_checkbutton = QCheckBox("Include 2 models",sire)
    sire.mac1_checkbutton = QCheckBox("Include primary macroturbulence",sire)
    sire.mac2_checkbutton = QCheckBox("Include secondary macroturbulence",sire)
    #sire.chi2_checkbutton = QCheckBox("Include chi^2",sire)
    sire.binary_checkbutton = QCheckBox("Include binary map",sire)

    sire.clear_map_btn = QPushButton("Update maps")
    sire.clear_map_btn.clicked.connect(lambda checked: clear_fig1(sire))

    sire.colour_table_options_btn = QPushButton("Colour table options")
    sire.colour_table_options_btn.clicked.connect(lambda checked: sire.colour_table_options())

    sire.clear_profiles_btn = QPushButton("Update profiles axes")
    sire.clear_profiles_btn.clicked.connect(lambda checked: clear_fig2(sire))
    sire.clear_models_btn = QPushButton("Update models axes")
    sire.clear_models_btn.clicked.connect(lambda checked: clear_fig3(sire))

    sire.autofill_btn = QPushButton("Autofill")
    sire.autofill_btn.clicked.connect(lambda checked: sire.autofill())

    sire.model1_btn = QPushButton("Search for model files")
    sire.model1_btn.clicked.connect(lambda checked: sire.get_model1())
    sire.select_model1 = QComboBox(sire)
    sire.syn_prof_btn = QPushButton("Search for synthetic profile files")
    sire.syn_prof_btn.clicked.connect(lambda checked: sire.get_syn_prof())
    sire.select_syn_prof = QComboBox(sire)
    sire.obs_prof_btn = QPushButton("Search for observed profile files")
    sire.obs_prof_btn.clicked.connect(lambda checked: sire.get_obs_prof())
    sire.select_obs_prof = QComboBox(sire)
    sire.model2_btn = QPushButton("Search for secondary model files")
    sire.model2_btn.clicked.connect(lambda checked: sire.get_model2())
    sire.select_model2 = QComboBox(sire)
    sire.mac1_btn = QPushButton("Search for primary macroturbulence files")
    sire.mac1_btn.clicked.connect(lambda checked: sire.get_mac1())
    sire.select_mac1 = QComboBox(sire)
    sire.mac2_btn = QPushButton("Search for secondary macroturbulence files")
    sire.mac2_btn.clicked.connect(lambda checked: sire.get_mac2())
    sire.select_mac2 = QComboBox(sire)
    # sire.chi2_btn = QPushButton("Search for chi^2 files")
    # sire.chi2_btn.clicked.connect(lambda checked: sire.get_chi2())
    # sire.select_chi2 = QComboBox(sire)
    sire.binary_btn = QPushButton("Search for binary map files")
    sire.binary_btn.clicked.connect(lambda checked: sire.get_binary())
    sire.select_binary = QComboBox(sire)
    #-------tab2-------#
    sire.Stokes_checkbutton = QCheckBox("Show observed Stokes I",sire)
    sire.Stokes_checkbutton.setChecked(True)
    sire.Stokes_Q_checkbutton = QCheckBox("Show observed Stokes Q",sire)
    sire.Stokes_Q_checkbutton.setChecked(True)
    sire.Stokes_U_checkbutton = QCheckBox("Show observed Stokes U",sire)
    sire.Stokes_U_checkbutton.setChecked(True)
    sire.Stokes_V_checkbutton = QCheckBox("Show observed Stokes V",sire)
    sire.Stokes_V_checkbutton.setChecked(True)
    sire.T_checkbutton = QCheckBox("Show temperature",sire)
    sire.T_checkbutton.setChecked(True)
    sire.B_checkbutton = QCheckBox("Show magnetic field strength/flux",sire)
    sire.B_checkbutton.setChecked(True)
    sire.V_checkbutton = QCheckBox("Show velocity",sire)
    sire.V_checkbutton.setChecked(True)
    sire.G_checkbutton = QCheckBox("Show inclination",sire)
    sire.G_checkbutton.setChecked(True)
    sire.A_checkbutton = QCheckBox("Show azimuth",sire)
    sire.A_checkbutton.setChecked(True)
    #-------tab3-------#
    sire.pI_checkbutton = QCheckBox("Show Stokes I",sire)
    sire.pI_checkbutton.setChecked(True)
    sire.pQ_checkbutton = QCheckBox("Show Stokes Q",sire)
    sire.pQ_checkbutton.setChecked(True)
    sire.pU_checkbutton = QCheckBox("Show Stokes U",sire)
    sire.pU_checkbutton.setChecked(True)
    sire.pV_checkbutton = QCheckBox("Show Stokes V",sire)
    sire.pV_checkbutton.setChecked(True)

    sire.mT_checkbutton = QCheckBox("Show temperature",sire)
    sire.mT_checkbutton.setChecked(True)
    sire.mB_checkbutton = QCheckBox("Show magnetic field strength/flux",sire)
    sire.mB_checkbutton.setChecked(True)
    sire.mV_checkbutton = QCheckBox("Show velocity",sire)
    sire.mV_checkbutton.setChecked(True)
    sire.mG_checkbutton = QCheckBox("Show inclination/azimuth",sire)
    sire.mG_checkbutton.setChecked(True)

    sire.wl_min_label = QLabel("WL min: ")
    sire.wl_min_entry = QLineEdit(sire)
    sire.wl_min_entry.setEnabled(False)
    sire.wl_max_label = QLabel("WL max: ")
    sire.wl_max_entry = QLineEdit(sire)
    sire.wl_max_entry.setEnabled(False)
    sire.wl_range_btn = QPushButton("Set wavelength range")
    sire.wl_range_btn.clicked.connect(lambda: set_wavelength_range(sire))

    sire.optical_depth_min_label = QLabel("OD min: ")
    sire.optical_depth_min_entry = QLineEdit(sire)
    sire.optical_depth_min_entry.setEnabled(False)
    sire.optical_depth_max_label = QLabel("OD max: ")
    sire.optical_depth_max_entry = QLineEdit(sire)
    sire.optical_depth_max_entry.setEnabled(False)
    sire.optical_depth_range_btn = QPushButton("Set optical depth range")
    sire.optical_depth_range_btn.clicked.connect(lambda: set_optical_depth_range(sire))
    #-------tab4-------#
    sire.parameter_label = QLabel("Parameter")
    sire.parameter_label.setStyleSheet("background-color: white")
    sire.ff_label = QLabel("ff")
    sire.T_label = QLabel("T [K]")
    sire.B_label = QLabel("B [G]")
    sire.V_label = QLabel("LOS vel [km/s]")
    sire.G_label = QLabel("inclin. [deg.]")
    sire.A_label = QLabel("azi. [deg.]")
    sire.mic_label = QLabel("mic vel [cm/s]")
    sire.mac_label = QLabel("mac vel [cm/s]")
    sire.mod1_label = QLabel("Mod 1")
    sire.mod1_label.setStyleSheet("background-color: white")
    sire.mod1_ff_value = QLabel("N/A")
    sire.mod1_T_value = QLabel("N/A")
    sire.mod1_B_value = QLabel("N/A")
    sire.mod1_V_value = QLabel("N/A")
    sire.mod1_G_value = QLabel("N/A")
    sire.mod1_A_value = QLabel("N/A")
    sire.mod1_mic_value = QLabel("N/A")
    sire.mod1_mac_value = QLabel("N/A")
    sire.mod2_label = QLabel("Mod 2")
    sire.mod2_label.setStyleSheet("background-color: white")
    sire.mod2_ff_value = QLabel("N/A")
    sire.mod2_T_value = QLabel("N/A")
    sire.mod2_B_value = QLabel("N/A")
    sire.mod2_V_value = QLabel("N/A")
    sire.mod2_G_value = QLabel("N/A")
    sire.mod2_A_value = QLabel("N/A")
    sire.mod2_mic_value = QLabel("N/A")
    sire.mod2_mac_value = QLabel("N/A")
    sire.pixel_values = QLabel("")
    sire.pixel_values.setStyleSheet("background-color: white")
    #-------widgets for canvas-------#
    sire.sc1 = MplCanvas1(sire, width=5, height=4, dpi=100)
    sire.sc1.fig1.canvas.mpl_connect('button_press_event', sire.mouseclicks)
    sire.sc2 = MplCanvas2(sire, width=5, height=4, dpi=100)
    sire.sc3 = MplCanvas3(sire, width=5, height=4, dpi=100)

    sire.frame_scale = QSlider(Qt.Horizontal)
    sire.frame_scale.sliderReleased.connect(lambda: change_frame(sire))
    sire.frame_scale.valueChanged.connect(lambda: update_frame_label(sire))
    sire.frame_label = QLabel("FR: " + str(sire.frame_scale.value()),sire)
    sire.wl_scale = QSlider(Qt.Horizontal)
    sire.wl_scale.sliderReleased.connect(lambda: change_wl(sire))
    sire.wl_scale.valueChanged.connect(lambda: update_wl_label(sire))
    sire.wl_label = QLabel("WL: " + str(sire.wl_scale.value()),sire)
    sire.optical_depth_scale = QSlider(Qt.Horizontal)
    sire.optical_depth_scale.sliderReleased.connect(lambda: change_optical_depth(sire))
    sire.optical_depth_scale.valueChanged.connect(lambda: update_optical_depth_label(sire))
    sire.optical_depth_label = QLabel("OD: " + str(sire.optical_depth_scale.value()),sire)

def update_frame_label(sire):
    sire.frame_label.setText("FR: " + str(sire.frame_scale.value()))
def update_wl_label(sire):
    sire.wl_label.setText("WL: " + str(sire.wl_scale.value()))
def update_optical_depth_label(sire):
    sire.optical_depth_label.setText("OD: " + str(sire.optical_depth_scale.value()))

class MplCanvas1(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=300):
        self.fig1 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas1, self).__init__(self.fig1)
class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=300):
        self.fig2 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas2, self).__init__(self.fig2)
class MplCanvas3(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=300):
        self.fig3 = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        super(MplCanvas3, self).__init__(self.fig3)


def colour_table_layouts(self,sire):
    self.colour_table_layout = QGridLayout() #row,col

    self.colour_table_layout.addWidget(self.CT_empty_label,0,0)
    self.colour_table_layout.addWidget(self.CT_StkI_label,1,0)
    self.colour_table_layout.addWidget(self.CT_StkQ_label,2,0)
    self.colour_table_layout.addWidget(self.CT_StkU_label,3,0)
    self.colour_table_layout.addWidget(self.CT_StkV_label,4,0)
    self.colour_table_layout.addWidget(self.CT_T_label,5,0)
    self.colour_table_layout.addWidget(self.CT_B_label,6,0)
    self.colour_table_layout.addWidget(self.CT_V_label,7,0)
    self.colour_table_layout.addWidget(self.CT_G_label,8,0)
    self.colour_table_layout.addWidget(self.CT_A_label,9,0)

    self.colour_table_layout.addWidget(self.CT_label,0,1)
    self.colour_table_layout.addWidget(self.CT_StkI,1,1)
    self.colour_table_layout.addWidget(self.CT_StkQ,2,1)
    self.colour_table_layout.addWidget(self.CT_StkU,3,1)
    self.colour_table_layout.addWidget(self.CT_StkV,4,1)
    self.colour_table_layout.addWidget(self.CT_T,5,1)
    self.colour_table_layout.addWidget(self.CT_B,6,1)
    self.colour_table_layout.addWidget(self.CT_V,7,1)
    self.colour_table_layout.addWidget(self.CT_G,8,1)
    self.colour_table_layout.addWidget(self.CT_A,9,1)

    self.colour_table_layout.addWidget(self.CT_vmin_label,0,2)
    self.colour_table_layout.addWidget(self.CT_StkI_vmin,1,2)
    self.colour_table_layout.addWidget(self.CT_StkQ_vmin,2,2)
    self.colour_table_layout.addWidget(self.CT_StkU_vmin,3,2)
    self.colour_table_layout.addWidget(self.CT_StkV_vmin,4,2)
    self.colour_table_layout.addWidget(self.CT_T_vmin,5,2)
    self.colour_table_layout.addWidget(self.CT_B_vmin,6,2)
    self.colour_table_layout.addWidget(self.CT_V_vmin,7,2)
    self.colour_table_layout.addWidget(self.CT_G_vmin,8,2)
    self.colour_table_layout.addWidget(self.CT_A_vmin,9,2)

    self.colour_table_layout.addWidget(self.CT_vmax_label,0,3)
    self.colour_table_layout.addWidget(self.CT_StkI_vmax,1,3)
    self.colour_table_layout.addWidget(self.CT_StkQ_vmax,2,3)
    self.colour_table_layout.addWidget(self.CT_StkU_vmax,3,3)
    self.colour_table_layout.addWidget(self.CT_StkV_vmax,4,3)
    self.colour_table_layout.addWidget(self.CT_T_vmax,5,3)
    self.colour_table_layout.addWidget(self.CT_B_vmax,6,3)
    self.colour_table_layout.addWidget(self.CT_V_vmax,7,3)
    self.colour_table_layout.addWidget(self.CT_G_vmax,8,3)
    self.colour_table_layout.addWidget(self.CT_A_vmax,9,3)

    self.colour_table_layout.addWidget(self.CT_StkI_autoscaling_checkbutton,1,4)
    self.colour_table_layout.addWidget(self.CT_StkQ_autoscaling_checkbutton,2,4)
    self.colour_table_layout.addWidget(self.CT_StkU_autoscaling_checkbutton,3,4)
    self.colour_table_layout.addWidget(self.CT_StkV_autoscaling_checkbutton,4,4)
    self.colour_table_layout.addWidget(self.CT_T_autoscaling_checkbutton,5,4)
    self.colour_table_layout.addWidget(self.CT_B_autoscaling_checkbutton,6,4)
    self.colour_table_layout.addWidget(self.CT_V_autoscaling_checkbutton,7,4)
    self.colour_table_layout.addWidget(self.CT_G_autoscaling_checkbutton,8,4)
    self.colour_table_layout.addWidget(self.CT_A_autoscaling_checkbutton,9,4)

    self.colour_table_layout.addWidget(self.update_and_set,10,0)

    self.setLayout(self.colour_table_layout)
def colour_table_widgets(self,sire):
    self.CT_empty_label = QLabel(" ")
    self.CT_StkI_label = QLabel("Stokes I")
    self.CT_StkQ_label = QLabel("Stokes Q")
    self.CT_StkU_label = QLabel("Stokes U")
    self.CT_StkV_label = QLabel("Stokes V")
    self.CT_T_label = QLabel("Temperature ")
    self.CT_B_label = QLabel("Magnetic field str./flux dens.")
    self.CT_V_label = QLabel("Velocity")
    self.CT_G_label = QLabel("Inclination ")
    self.CT_A_label = QLabel("Azimuth ")

    self.CT_label = QLabel("Colour tables")
    self.CT_StkI = QComboBox(self)
    set_CT_combos(self.CT_StkI,sire.StkI_CT[0],sire.CT_options)
    self.CT_StkQ = QComboBox(self)
    set_CT_combos(self.CT_StkQ,sire.StkQ_CT[0],sire.CT_options)
    self.CT_StkU = QComboBox(self)
    set_CT_combos(self.CT_StkU,sire.StkU_CT[0],sire.CT_options)
    self.CT_StkV = QComboBox(self)
    set_CT_combos(self.CT_StkV,sire.StkV_CT[0],sire.CT_options)
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
    self.CT_StkI_vmin.setText(str(sire.StkI_CT[1]))
    self.CT_StkI_vmin.setEnabled(False)
    self.CT_StkQ_vmin = QLineEdit(self)
    self.CT_StkQ_vmin.setText(str(sire.StkQ_CT[1]))
    self.CT_StkQ_vmin.setEnabled(False)
    self.CT_StkU_vmin = QLineEdit(self)
    self.CT_StkU_vmin.setText(str(sire.StkU_CT[1]))
    self.CT_StkU_vmin.setEnabled(False)
    self.CT_StkV_vmin = QLineEdit(self)
    self.CT_StkV_vmin.setText(str(sire.StkV_CT[1]))
    self.CT_StkV_vmin.setEnabled(False)
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
    self.CT_StkI_vmax.setText(str(sire.StkI_CT[2]))
    self.CT_StkI_vmax.setEnabled(False)
    self.CT_StkQ_vmax = QLineEdit(self)
    self.CT_StkQ_vmax.setText(str(sire.StkQ_CT[2]))
    self.CT_StkQ_vmax.setEnabled(False)
    self.CT_StkU_vmax = QLineEdit(self)
    self.CT_StkU_vmax.setText(str(sire.StkU_CT[2]))
    self.CT_StkU_vmax.setEnabled(False)
    self.CT_StkV_vmax = QLineEdit(self)
    self.CT_StkV_vmax.setText(str(sire.StkV_CT[2]))
    self.CT_StkV_vmax.setEnabled(False)
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
    self.CT_StkI_autoscaling_checkbutton.setChecked(sire.StkI_CT[3])
    self.CT_StkI_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_StkI_vmin, self.CT_StkI_vmax, self.CT_StkI_autoscaling_checkbutton))
    self.CT_StkQ_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_StkQ_autoscaling_checkbutton.setChecked(sire.StkQ_CT[3])
    self.CT_StkQ_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_StkQ_vmin, self.CT_StkQ_vmax, self.CT_StkQ_autoscaling_checkbutton))
    self.CT_StkU_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_StkU_autoscaling_checkbutton.setChecked(sire.StkU_CT[3])
    self.CT_StkU_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_StkU_vmin, self.CT_StkU_vmax, self.CT_StkU_autoscaling_checkbutton))
    self.CT_StkV_autoscaling_checkbutton = QCheckBox("Enable autoscaling",self)
    self.CT_StkV_autoscaling_checkbutton.setChecked(sire.StkV_CT[3])
    self.CT_StkV_autoscaling_checkbutton.stateChanged.connect(lambda: CT_state_changed(self.CT_StkV_vmin, self.CT_StkV_vmax, self.CT_StkV_autoscaling_checkbutton))
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
    sire.StkI_CT[0] = self.CT_StkI.currentText()
    sire.StkQ_CT[0] = self.CT_StkQ.currentText()
    sire.StkU_CT[0] = self.CT_StkU.currentText()
    sire.StkV_CT[0] = self.CT_StkV.currentText()
    sire.T_CT[0] = self.CT_T.currentText()
    sire.B_CT[0] = self.CT_B.currentText()
    sire.V_CT[0] = self.CT_V.currentText()
    sire.G_CT[0] = self.CT_G.currentText()
    sire.A_CT[0] = self.CT_A.currentText()

    if self.CT_StkI_autoscaling_checkbutton.isChecked():
        sire.StkI_CT[3] = 1
    else:
        sire.StkI_CT[3] = 0
        sire.StkI_CT[1] = self.CT_StkI_vmin.text()
        sire.StkI_CT[2] = self.CT_StkI_vmax.text()
    if self.CT_StkQ_autoscaling_checkbutton.isChecked():
        sire.StkQ_CT[3] = 1
    else:
        sire.StkQ_CT[3] = 0
        sire.StkQ_CT[1] = self.CT_StkQ_vmin.text()
        sire.StkQ_CT[2] = self.CT_StkQ_vmax.text()
    if self.CT_StkU_autoscaling_checkbutton.isChecked():
        sire.StkU_CT[3] = 1
    else:
        sire.StkU_CT[3] = 0
        sire.StkU_CT[1] = self.CT_StkU_vmin.text()
        sire.StkU_CT[2] = self.CT_StkU_vmax.text()
    if self.CT_StkV_autoscaling_checkbutton.isChecked():
        sire.StkV_CT[3] = 1
    else:
        sire.StkV_CT[3] = 0
        sire.StkV_CT[1] = self.CT_StkV_vmin.text()
        sire.StkV_CT[2] = self.CT_StkV_vmax.text()
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

def preferences_layouts(self,sire):
    self.preferences_layout = QGridLayout() #row,col

    self.preferences_layout.addWidget(self.fontsize_label,0,0)
    self.preferences_layout.addWidget(self.fontsize_btn,0,1)

    self.preferences_layout.addWidget(self.fontsize_titles_map_label,1,0)
    self.preferences_layout.addWidget(self.fontsize_titles_map_entry,1,1)

    self.preferences_layout.addWidget(self.fontsize_axislabels_map_label,2,0)
    self.preferences_layout.addWidget(self.fontsize_axislabels_map_entry,2,1)

    self.preferences_layout.addWidget(self.fontsize_ticklabels_map_label,3,0)
    self.preferences_layout.addWidget(self.fontsize_ticklabels_map_entry,3,1)

    self.setLayout(self.preferences_layout)

def preferences_widgets(self,sire):
    self.fontsize_label = QLabel("Font sizes")
    self.fontsize_label.setStyleSheet("font-weight: bold")
    self.fontsize_titles_map_label = QLabel("Titles: ")
    self.fontsize_titles_map_entry = QLineEdit(self)
    self.fontsize_axislabels_map_label = QLabel("Axis labels: ")
    self.fontsize_axislabels_map_entry = QLineEdit(self)
    self.fontsize_ticklabels_map_label = QLabel("Tick labels: ")
    self.fontsize_ticklabels_map_entry = QLineEdit(self)
    self.fontsize_btn = QPushButton("Set font sizes")
    self.fontsize_btn.clicked.connect(lambda: set_font_sizes(self,sire))
    self.fontsize_titles_map_entry.setText(str(sire.fontsize_titles))
    self.fontsize_axislabels_map_entry.setText(str(sire.fontsize_axislabels))
    self.fontsize_ticklabels_map_entry.setText(str(sire.fontsize_ticklabels))
