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
    #adding tabs to control panel
    self.tabs = QTabWidget()
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.tabs.addTab(self.tab1,"Folder search")
    self.tabs.addTab(self.tab2,"File search")
    self.tabs.addTab(self.tab3,"Optional")
    self.tabLayout = QVBoxLayout()
    #-------adding widgets-------#
    self.left_layout.addWidget(self.tabs)
    self.tabLayout.addWidget(self.btn_folder_search)
    self.tabLayout.addWidget(self.select_folder)
    self.tabLayout.addWidget(self.select_instrument)
    self.tabLayout.addStretch(1)
    self.tab1.setLayout(self.tabLayout)

    self.left_layout.addWidget(self.btnDisplay)

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
    self.twoLayout.addWidget(self.sc3)

#slider
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
    self.right_bottom_layout.addWidget(self.frame_scale)
    self.right_bottom_layout.addWidget(self.wl_scale)
    self.right_bottom_layout.addWidget(self.optical_depth_scale)

    #--------setting main window layout----------#
    #self.setLayout(self.mainLayout)

def widgets(self):
    #-------widgets for canvas-------#
    self.sc1 = MplCanvas1(self, width=5, height=4, dpi=100)
    self.sc1.fig.canvas.mpl_connect('button_press_event', self.mouseclicks)
    self.sc2 = MplCanvas2(self, width=5, height=4, dpi=100)
    self.sc3 = MplCanvas2(self, width=5, height=4, dpi=100)

    #-------widgets for control panel-------#
    self.btnDisplay = QPushButton("Display dataset")
    self.btnDisplay.clicked.connect(lambda checked: self.change_canvas())

    self.btn_folder_search = QPushButton("Search for folder")
    self.btn_folder_search.clicked.connect(lambda checked: self.get_instrument())

    self.select_folder = QComboBox(self)
    self.select_folder.addItems(self.instrument_options)

    self.btn_search = QPushButton("Search for datasets")
    self.btn_search.clicked.connect(lambda checked: self.get_instrument())

    self.btn_search = QPushButton("Search for datasets")
    self.btn_search.clicked.connect(lambda checked: self.get_instrument())

    self.btn_search = QPushButton("Search for datasets")
    self.btn_search.clicked.connect(lambda checked: self.get_instrument())

    #self.select_file = QComboBox(self)

    self.select_instrument = QComboBox(self)
    self.select_instrument.addItems(self.instrument_options)

    self.frame_scale = QSlider(Qt.Horizontal)
    self.frame_scale.sliderReleased.connect(self.updateFrame)
    self.wl_scale = QSlider(Qt.Horizontal)
    self.optical_depth_scale = QSlider(Qt.Horizontal)



class MplCanvas1(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.ax1 = self.fig.add_subplot(141)
        self.ax2 = self.fig.add_subplot(142)
        self.ax3 = self.fig.add_subplot(143)
        self.ax4 = self.fig.add_subplot(144)
        super(MplCanvas1, self).__init__(self.fig)
class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi,tight_layout=True)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        super(MplCanvas2, self).__init__(self.fig)

