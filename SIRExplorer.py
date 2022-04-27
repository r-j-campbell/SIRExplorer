from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
import sys,os
import sqlite3
from PIL import Image

import numpy as np

from design import layouts, widgets
from Instruments import SIR
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

        self.set_wavelength=0
        self.set_frame=0

        self.class_objects = {0: {"file": "first dummy value"}
                              }
        self.folder_list = [None]
        self.model1_file_list = [None]
        self.model2_file_list = [None]
        self.obs_prof_file_list = [None]
        self.syn_prof_file_list = [None]
        self.mac1_file_list = [None]
        self.mac2_file_list = [None]
        self.chi2_file_list = [None]
        self.binary_file_list = [None]

        self.I_CT = ['gray',0.9,1.1,0]
        self.T_CT = ['gray',6500,7500,0]
        self.G_CT = ['bwr',0,180,0]
        self.A_CT = ['hsv',0,360,0]
        self.V_CT = ['bwr',-4,4,0]
        self.B_CT = ['viridis',0,2000,0]

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

    def get_model1(self):
        url = QFileDialog.getOpenFileName(self,"Select a primary model file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.model1_file_list:
            self.model1_file_list.append(value)
            self.select_model1.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_syn_prof(self):
        url = QFileDialog.getOpenFileName(self,"Select a synthetic profile file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.syn_prof_file_list:
            self.syn_prof_file_list.append(value)
            self.select_syn_prof.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_obs_prof(self):
        url = QFileDialog.getOpenFileName(self,"Select a observed profile file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.obs_prof_file_list:
            self.obs_prof_file_list.append(value)
            self.select_obs_prof.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_model2(self):
        url = QFileDialog.getOpenFileName(self,"Select a secondary model file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.model2_file_list:
            self.model2_file_list.append(value)
            self.select_model2.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_mac1(self):
        url = QFileDialog.getOpenFileName(self,"Select a primary macroturbulence file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.mac1_file_list:
            self.mac1_file_list.append(value)
            self.select_mac1.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_mac2(self):
        url = QFileDialog.getOpenFileName(self,"Select a secondary macroturbulence file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.mac2_file_list:
            self.mac2_file_list.append(value)
            self.select_mac2.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_chi2(self):
        url = QFileDialog.getOpenFileName(self,"Select a chi^2 file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.chi2_file_list:
            self.chi2_file_list.append(value)
            self.select_chi2.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
    def get_binary(self):
        url = QFileDialog.getOpenFileName(self,"Select a binary file","","All Files(*);;*fits")
        value = str(url[0])
        if value not in self.binary_file_list:
            self.binary_file_list.append(value)
            self.select_binary.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def get_folder(self):
        value = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #url = QFileDialog.getOpenFileName(self,"Select a dataset","","All Files(*);;*fits")
        if value not in self.folder_list:
            self.folder_list.append(value)
            self.select_folder.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This dataset has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def autofill(self):
        value = str(self.select_folder.currentText())+"/mod1.fits"
        if value not in self.model1_file_list:
            self.model1_file_list.append(value)
            self.select_model1.addItem(value)
        index = self.select_model1.findText(value)
        if index >= 0:
            self.select_model1.setCurrentIndex(index)
        del value

        value = str(self.select_folder.currentText())+"/obs_prof.fits"
        if value not in self.obs_prof_file_list:
            self.obs_prof_file_list.append(value)
            self.select_obs_prof.addItem(value)
        index = self.select_obs_prof.findText(value)
        if index >= 0:
            self.select_obs_prof.setCurrentIndex(index)
        del value

        value = str(self.select_folder.currentText())+"/syn_prof.fits"
        if value not in self.syn_prof_file_list:
            self.syn_prof_file_list.append(value)
            self.select_syn_prof.addItem(value)
        index = self.select_syn_prof.findText(value)
        if index >= 0:
            self.select_syn_prof.setCurrentIndex(index)
        del value

        if self.two_models_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mod2.fits"
            if value not in self.model2_file_list:
                self.model2_file_list.append(value)
                self.select_model2.addItem(value)
            index = self.select_model2.findText(value)
            if index >= 0:
                self.select_model2.setCurrentIndex(index)
            del value

        if self.macro1_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac1.fits"
            if value not in self.mac1_file_list:
                self.mac1_file_list.append(value)
                self.select_mac1.addItem(value)
            index = self.select_mac1.findText(value)
            if index >= 0:
                self.select_mac1.setCurrentIndex(index)
            del value

        if self.macro2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac2.fits"
            if value not in self.mac2_file_list:
                self.mac2_file_list.append(value)
                self.select_mac2.addItem(value)
            index = self.select_mac2.findText(value)
            if index >= 0:
                self.select_mac2.setCurrentIndex(index)
            del value

        if self.chi2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/chi2.fits"
            if value not in self.chi2_file_list:
                self.chi2_file_list.append(value)
                self.select_chi2.addItem(value)
            index = self.select_chi2.findText(value)
            if index >= 0:
                self.select_chi2.setCurrentIndex(index)
            del value

        if self.binary_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/binary.fits"
            if value not in self.binary_file_list:
                self.binary_file_list.append(value)
                self.select_binary.addItem(value)
            index = self.select_binary.findText(value)
            if index >= 0:
                self.select_binary.setCurrentIndex(index)
            del value


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

    def update_wavelength(self, event):
        self.set_wavelength=self.controller.control_panel.wlscale.get()
        self.controller.canvas_frame.change_wl(self.set_wavelength)
    def update_frame(self):
        if self.frame_flag == 1:
            self.set_frame=int(self.framescale.value())
            change_frame(self,self.set_frame)
    def update_optical_depth(self, event):
        self.set_wavelength=self.controller.control_panel.wlscale.get()
        self.controller.canvas_frame.change_wl(self.set_wavelength)

def main():
    app=QApplication(sys.argv)
    window=SIRExplorer()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
