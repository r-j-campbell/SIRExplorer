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
            print(self.model1_file_list)
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
            print(self.syn_prof_file_list)
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
            print(self.obs_prof_file_list)
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
            print(self.model2_file_list)
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
            print(self.mac1_file_list)
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
            print(self.mac2_file_list)
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
            print(self.chi2_file_list)
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
            print(self.binary_file_list)
            self.select_binary.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This file has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def get_folder(self):
        value = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #url = QFileDialog.getOpenFileName(self,"Select a dataset","","All Files(*);;*fits")
        print(value)
        if value not in self.folder_list:
            self.folder_list.append(value)
            print(self.folder_list)
            self.select_folder.addItem(value)
        else:
            msg = QMessageBox()
            msg.setText("This dataset has already been selected.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def autofill(self):
        print("autofill")
        auto_model_file = str(self.select_folder.get())+"/inv_res_mod_SIRE.fits"
        if auto_model_file not in self.model_file_list:
            self.model_file_list.append(auto_model_file)
            self.select_model_files["values"] = self.model_file_list
            self.select_model.set(auto_model_file)

        auto_obs_file = str(self.select_folder.get())+"/observed_prof_SIRE.fits"
        if auto_obs_file not in self.obs_prof_file_list:
            self.obs_prof_file_list.append(auto_obs_file)
            self.select_obs_prof_files["values"] = self.obs_prof_file_list
            self.selected_obs_prof.set(auto_obs_file)

        auto_syn_file = str(self.selected_folder.get())+"/inv_res_prof_SIRE.fits"
        if auto_syn_file not in self.syn_prof_file_list:
            self.syn_prof_file_list.append(auto_syn_file)
            self.select_syn_prof_files["values"] = self.syn_prof_file_list
            self.selected_syn_prof.set(auto_syn_file)

        if self.two_models_var.get() == 1:
            auto_model_two_file = str(self.selected_folder.get())+"/inv_res_sec_mods_SIRE.fits"
            if auto_model_two_file not in self.secondary_model_file_list:
                self.secondary_model_file_list.append(auto_model_two_file)
                self.select_secondary_model_files["values"] = self.secondary_model_file_list
                self.selected_secondary_model.set(auto_model_two_file)

        if self.macroturb1_var.get() == 1:
            auto_macroturb1_file = str(self.selected_folder.get())+"/inv_res_macro_mod_SIRE.fits"
            if auto_macroturb1_file not in self.mac1_file_list:
                self.mac1_file_list.append(auto_macroturb1_file)
                self.select_mac1_files["values"] = self.mac1_file_list
                self.selected_mac1.set(auto_macroturb1_file)

        if self.macroturb2_var.get() == 1:
            auto_macroturb2_file = str(self.selected_folder.get())+"/inv_res_sec_macro_mod_SIRE.fits"
            if auto_macroturb2_file not in self.mac2_file_list:
                self.mac2_file_list.append(auto_macroturb2_file)
                self.select_mac2_files["values"] = self.mac2_file_list
                self.selected_mac2.set(auto_macroturb2_file)

        if self.chi2_var.get() == 1:
            auto_chi2_file = str(self.selected_folder.get())+"/chi2.fits"
            if auto_chi2_file not in self.chi2_file_list:
                self.chi2_file_list.append(auto_chi2_file)
                self.select_chi2_files["values"] = self.chi2_file_list
                self.selected_chi2.set(auto_chi2_file)

        if self.binary_var.get() == 1:
            auto_binary_file = str(self.selected_folder.get())+"/binary.fits"
            if auto_binary_file not in self.binary_file_list:
                self.binary_file_list.append(auto_binary_file)
                self.select_binary_files["values"] = self.binary_file_list
                self.selected_binary.set(auto_binary_file)


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
