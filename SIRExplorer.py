from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
import sys,os
import sqlite3
from PIL import Image

import numpy as np

from design import layouts, widgets
from Instruments import Imager, IFU
from canvas_functions import show_IFU, click_IFU, show_imager, change_frame

class SIRExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIR Explorer: PyQt version")
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.appheight = self.screenRect.height()
        self.appwidth = self.screenRect.width()
        self.setGeometry(0,0,int(self.appwidth),int(self.appheight))

        self.increment = 0
        self.click_increment=0
        self.flag = None
        self.match = 0
        self.frame_flag=0
        self.continuum_flag=0

        self.set_wavelength=0
        self.set_frame=0

        self.class_objects = {0: {"file": "first dummy value"}
                              }
        self.file_list = [None]
        self.instrument_options = ["Integral field unit (IFU)",
                                   "Fabry–Pérot interferometer (FPI)",
                                   "Slit-spectropolarimeter",
                                   "Imager",
                                   "DKIST/VTF",
                                   "DKIST/ViSP",
                                   "DKIST/DL-NIRSP",
                                   "DKIST/VBI",
                                   "Hinode/SP",
                                   "GREGOR/GRIS",
                                   "GREGOR/GRIS-IFU",
                                   "GREGOR/HiFI",
                                   "SIR/synthetic"]
        #colour tables for spectropolarimetric datasets
        self.I_im_CT = ['gray',0.9,1.1,1]
        self.Q_im_CT = ['gray',0.9,1.1,1]
        self.U_im_CT = ['gray',0.9,1.1,1]
        self.V_im_CT = ['gray',0.9,1.1,1]
        #colour tables for imager datasets
        self.I_CT = ['gray',0.9,1.1,1]
        # self.bind("<Left>",lambda event: self.left_arrow())
        # self.bind("<Right>",lambda event: self.right_arrow())
        # self.bind("<Up>",lambda event: self.up_arrow())
        # self.bind("<Down>",lambda event: self.down_arrow())

        self.fontsize_titles=10
        self.fontsize_axislabels=10
        self.linewidth=1

        self.wl_max=100
        self.wl_min=0
        self.wl_dim=100

        self.UI()
        self.show()

    def UI(self):
        widgets(self)
        layouts(self)

    def get_instrument(self):
        url = QFileDialog.getOpenFileName(self,"Select a dataset","","All Files(*);;*fits")
        value = url[0]
        if value not in self.file_list:
            self.file_list.append(value)
            print(self.file_list)
            self.select_file.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This dataset has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


    def get_all_values(self,nested_dictionary,i,match): #searches nested dictionary for datasets that are already loaded
        for key, value in nested_dictionary.items():
            if type(value) is dict:
                i+=1
                self.get_all_values(value,i,match)
            else:
                if value == match:
                    self.flag=True
                    self.match = i-1
                    return

    def change_canvas(self):
        self.flag=False
        self.get_all_values(self.class_objects,0,self.select_file.currentText())

        if self.flag == True: #if match is found
            i=str(self.match)
            if self.select_instrument.currentText() == "Imager":
                print("imager match")
            elif self.select_instrument.currentText() == "Integral field unit (IFU)" or self.select_instrument.currentText() == "GREGOR/GRIS-IFU":
                show_IFU(self,self.class_objects[i],self.click_increment,self.increment,self.frame_flag,self.flag)
                print("IFU match")

        elif self.flag == False: #if match is not found
            if self.select_instrument.currentText() == "Imager" or self.select_instrument.currentText() == "GREGOR/HiFI":
                class_object = Imager()
                j=str(len(self.class_objects))
                self.class_objects[j] = {'file': self.select_file.currentText(),
                                        'class_object': class_object
                                        }
                print(self.class_objects[j])
                show_imager(self,self.class_objects[j])
            elif self.select_instrument.currentText() == "Integral field unit (IFU)" or self.select_instrument.currentText() == "GREGOR/GRIS-IFU":
                class_object = IFU()
                j=str(len(self.class_objects))
                self.class_objects[j] = {'file': self.select_file.currentText(),
                                        'class_object': class_object
                                        }
                print(self.class_objects[j])
                show_IFU(self,self.class_objects[j],self.click_increment,self.increment,self.frame_flag,self.flag)

        if self.increment == 0:
            print("increment changed to 1")
            click_IFU(self,self.class_objects[j],self.click_increment)
            self.increment=1
        #self.canvas_frame.toggle_widgets(self)

    def mouseclicks(self,event):
        self.flag=False
        self.get_all_values(self.class_objects,0,self.select_file.currentText())
        if self.flag == True:
            i=str(self.match)
            self.class_objects[i]["class_object"].current_x = event.xdata
            self.class_objects[i]["class_object"].current_y = event.ydata
            if self.click_increment == 0 :
                self.click_increment=1
                print("click increment changed to 1")
            click_IFU(self,self.class_objects[i],self.click_increment)
            self.change_canvas()

        else:
            print("error!! dataset not found...")

    def updateWavelength(self, event):
        self.set_wavelength=self.controller.control_panel.wlscale.get()
        self.controller.canvas_frame.change_wl(self.set_wavelength)
    def updateFrame(self):
        if self.frame_flag == 1:
            self.set_frame=int(self.framescale.value())
            change_frame(self,self.set_frame)

def main():
    app=QApplication(sys.argv)
    window=SIRExplorer()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
