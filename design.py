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
    self.tabs.addTab(self.tab2,"Options")
    self.tabs.addTab(self.tab3,"Options")
    self.tabLayout = QVBoxLayout()
    self.left_layout.addWidget(self.tabs)
    self.tabLayout.addWidget(self.btn_folder_search)
    self.tabLayout.addWidget(self.select_folder)
    self.tabLayout.addWidget(self.model2_checkbutton)
    self.tabLayout.addWidget(self.mac1_checkbutton)
    self.tabLayout.addWidget(self.mac2_checkbutton)
    self.tabLayout.addWidget(self.chi2_checkbutton)
    self.tabLayout.addWidget(self.binary_checkbutton)

    self.tabLayout.addWidget(self.autofill_btn)

    self.tabLayout.addWidget(self.model1_btn)
    self.tabLayout.addWidget(self.select_model1)

    self.tabLayout.addWidget(self.syn_prof_btn)
    self.tabLayout.addWidget(self.select_syn_prof)

    self.tabLayout.addWidget(self.obs_prof_btn)
    self.tabLayout.addWidget(self.select_obs_prof)

    self.tabLayout.addWidget(self.model2_btn)
    self.tabLayout.addWidget(self.select_model2)

    self.tabLayout.addWidget(self.mac1_btn)
    self.tabLayout.addWidget(self.select_mac1)

    self.tabLayout.addWidget(self.mac2_btn)
    self.tabLayout.addWidget(self.select_mac2)

    self.tabLayout.addWidget(self.chi2_btn)
    self.tabLayout.addWidget(self.select_chi2)

    self.tabLayout.addWidget(self.binary_btn)
    self.tabLayout.addWidget(self.select_binary)

    self.tabLayout.addStretch(1)
    self.tab1.setLayout(self.tabLayout)

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
    self.sc2.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc2.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc2.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc2.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.twoLayout.addWidget(self.sc3)
    self.sc3.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc3.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc3.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc3.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)

    self.threeWidget = QWidget()
    self.threeWidget.setLayout(self.right_layout)
    self.splitter2 = QSplitter(Qt.Horizontal)
    self.splitter2.addWidget(self.threeWidget)
    self.splitter2.addWidget(self.splitter1)
    self.right_layout.addWidget(self.splitter2)

    self.threeLayout = QHBoxLayout() #maps
    self.threeWidget.setLayout(self.threeLayout)

    self.threeLayout.addWidget(self.sc1)
    self.sc1.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc1.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc1.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc1.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc1.ax5.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
    self.sc1.ax6.tick_params(axis='both', labelsize=self.fontsize_ticklabels)

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
    #-------widgets for canvas-------#
    self.sc1 = MplCanvas1(self, width=5, height=4, dpi=100)
    self.sc1.fig.canvas.mpl_connect('button_press_event', self.mouseclicks)
    self.sc2 = MplCanvas2(self, width=5, height=4, dpi=100)
    self.sc3 = MplCanvas3(self, width=5, height=4, dpi=100)

    #-------widgets for control panel-------#
    self.btnDisplay = QPushButton("Display dataset")
    self.btnDisplay.clicked.connect(lambda checked: self.change_canvas())

    self.btn_folder_search = QPushButton("Search for folder")
    self.btn_folder_search.clicked.connect(lambda checked: self.get_folder())

    self.select_folder = QComboBox(self)

    self.model2_checkbutton = QCheckBox("Include 2 models",self)
    self.mac1_checkbutton = QCheckBox("Include primary macroturbulence",self)
    self.mac2_checkbutton = QCheckBox("Include secondary macroturbulence",self)
    self.chi2_checkbutton = QCheckBox("Include chi^2",self)
    self.binary_checkbutton = QCheckBox("Include binary map",self)

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
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.ax1 = self.fig.add_subplot(611)
        self.ax2 = self.fig.add_subplot(612)
        self.ax3 = self.fig.add_subplot(613)
        self.ax4 = self.fig.add_subplot(614)
        self.ax5 = self.fig.add_subplot(615)
        self.ax6 = self.fig.add_subplot(616)
        super(MplCanvas1, self).__init__(self.fig)
class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.ax1 = self.fig.add_subplot(411)
        self.ax2 = self.fig.add_subplot(412)
        self.ax3 = self.fig.add_subplot(413)
        self.ax4 = self.fig.add_subplot(414)
        super(MplCanvas2, self).__init__(self.fig)
class MplCanvas3(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        super(MplCanvas3, self).__init__(self.fig)

