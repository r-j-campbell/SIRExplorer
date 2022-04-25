from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from canvas_functions import *

def layouts(self):
    self.mainLayout = QHBoxLayout()
    self.setLayout(self.mainLayout)
    self.leftLayout = QVBoxLayout() #control panel
    self.rightLayout = QVBoxLayout() #canvas
    self.mainLayout.addLayout(self.leftLayout,20)
    self.mainLayout.addLayout(self.rightLayout,80)

    self.rightTopWidget = QWidget()
    self.rightMiddleWidget = QWidget()
    self.rightBottomWidget = QWidget()
    self.rightTopWidget.setLayout(self.rightLayout)
    self.rightMiddleWidget.setLayout(self.rightLayout)
    self.rightBottomWidget.setLayout(self.rightLayout)
    splitter = QSplitter(Qt.Vertical)
    splitter.addWidget(self.rightTopWidget)
    splitter.addWidget(self.rightMiddleWidget)
    splitter.addWidget(self.rightBottomWidget)
    self.rightLayout.addWidget(splitter)
    self.rightTopLayout = QVBoxLayout() #maps
    self.rightMiddleLayout = QHBoxLayout() #plots
    self.rightBottomLayout = QHBoxLayout() #buttons
    self.rightTopWidget.setLayout(self.rightTopLayout)
    self.rightMiddleWidget.setLayout(self.rightMiddleLayout)
    self.rightBottomWidget.setLayout(self.rightBottomLayout)
    #adding tabs to control panel
    self.tabs = QTabWidget()
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.tab3 = QWidget()
    self.tabs.addTab(self.tab1,"File manager")
    self.tabs.addTab(self.tab2,"Map controls")
    self.tabs.addTab(self.tab3,"Plot controls")
    self.tabLayout = QVBoxLayout()
    #-------adding widgets-------#
    self.leftLayout.addWidget(self.tabs)
    self.tabLayout.addWidget(self.btn_search)
    self.tabLayout.addWidget(self.select_file)
    self.tabLayout.addWidget(self.select_instrument)
    self.tabLayout.addStretch(1)
    self.tab1.setLayout(self.tabLayout)

    self.leftLayout.addWidget(self.btnDisplay)
    self.rightTopLayout.addWidget(self.sc1)
    self.rightMiddleLayout.addWidget(self.sc2)
    self.rightBottomLayout.addWidget(self.framescale)
    self.rightBottomLayout.addWidget(self.wlscale)


    #--------setting main window layout----------#
    #self.setLayout(self.mainLayout)

def widgets(self):
    #-------widgets for canvas-------#
    self.sc1 = MplCanvas1(self, width=5, height=4, dpi=100)
    self.sc1.fig.canvas.mpl_connect('button_press_event', self.mouseclicks)
    self.sc2 = MplCanvas2(self, width=5, height=4, dpi=100)

    self.btnDisplay = QPushButton("Display dataset")
    self.btnDisplay.clicked.connect(lambda checked: self.change_canvas())
    #-------widgets for control panel-------#

    self.btn_search = QPushButton("Search for datasets")
    self.btn_search.clicked.connect(lambda checked: self.get_instrument())

    self.select_file = QComboBox(self)

    self.select_instrument = QComboBox(self)
    self.select_instrument.addItems(self.instrument_options)

    self.framescale = QSlider(Qt.Horizontal)
    self.framescale.sliderReleased.connect(self.updateFrame)
    self.wlscale = QSlider(Qt.Horizontal)

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

