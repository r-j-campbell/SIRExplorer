from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
from time import sleep
from design import layouts, widgets, colour_table_layouts, colour_table_widgets, preferences_layouts, preferences_widgets
from Instruments import SIR
from canvas_functions import show, click, update_pixel_info, change_frame, change_wl, change_optical_depth

class SIRExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIR Explorer: PyQt version")
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.appheight = self.screenRect.height()
        self.appwidth = self.screenRect.width()
        self.setGeometry(0,0,int(self.appwidth),int(self.appheight))
        self.w = None
        self.p = None

        self.increment = 0 #zero on first launch, 1 thereafter
        self.click_increment = 0
        self.flag = None
        self.match = 0 #zero when no match is found, index of class_objects otherwise
        self.frame_changed_flag = 0 #1 when framescale released, otherwise 0

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

        #[CT, min, max, automatic scaling flag, display flag]
        self.StkI_CT = ['gray',0.9,1.1,1,1]
        self.StkQ_CT = ['gray',-0.05,0.05,1,1]
        self.StkU_CT = ['gray',-0.05,0.05,1,1]
        self.StkV_CT = ['gray',-0.05,0.05,1,1]
        self.T_CT = ['gray',6500,7500,1,1]
        self.G_CT = ['bwr',0,180,1,1]
        self.A_CT = ['hsv',0,360,1,1]
        self.V_CT = ['bwr',-4,4,1,1]
        self.B_CT = ['viridis',0,2000,1,1]
        self.CT_options = ['hsv', 'gray', 'gray_r', 'viridis','bwr', 'bwr_r','hot', 'plasma', 'inferno', 'magma', 'cividis',
                            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                            'binary', 'gist_yarg', 'gist_gray', 'bone',
                            'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                            'Wistia', 'afmhot', 'gist_heat', 'copper',
                            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                            'RdYlGn', 'Spectral', 'coolwarm', 'seismic',
                            'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                            'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                            'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                            'turbo', 'nipy_spectral', 'gist_ncar']

        self.fontsize_titles=7
        self.fontsize_axislabels=7
        self.fontsize_ticklabels=7
        self.linewidth=1

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

        if self.model2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mod2.fits"
            if value not in self.model2_file_list:
                self.model2_file_list.append(value)
                self.select_model2.addItem(value)
            index = self.select_model2.findText(value)
            if index >= 0:
                self.select_model2.setCurrentIndex(index)
            del value

        if self.mac1_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac1.fits"
            if value not in self.mac1_file_list:
                self.mac1_file_list.append(value)
                self.select_mac1.addItem(value)
            index = self.select_mac1.findText(value)
            if index >= 0:
                self.select_mac1.setCurrentIndex(index)
            del value

        if self.mac2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac2.fits"
            if value not in self.mac2_file_list:
                self.mac2_file_list.append(value)
                self.select_mac2.addItem(value)
            index = self.select_mac2.findText(value)
            if index >= 0:
                self.select_mac2.setCurrentIndex(index)
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
        print("change canvas")
        self.flag=False
        self.get_all_values(self.class_objects,0,self.select_model1.currentText())
        if self.flag == True: #if match is found
            print("match found")
            i=str(self.match)
            show(self,self.class_objects[i])
        elif self.flag == False: #if match is not found
            class_object = SIR()
            j=str(len(self.class_objects))
            self.match = j
            self.class_objects[j] = {'model_file': self.select_model1.currentText(),
                     'secondary_model_file': self.select_model2.currentText(),
                     'obs_prof_file': self.select_obs_prof.currentText(),
                     'syn_prof_file': self.select_syn_prof.currentText(),
                     'mac1_file': self.select_mac1.currentText(),
                     'mac2_file': self.select_mac2.currentText(),
                     'binary_file': self.select_binary.currentText(),
                     'class_object': class_object
                                     }
            show(self,self.class_objects[j])
        if self.increment == 0:
            click(self,self.class_objects[j])
            update_pixel_info(self, self.class_objects[j])
            if self.click_increment == 0:
                self.click_increment=1
            self.increment=1

    def mouseclicks(self, event):
        self.setFocus()
        i=str(self.match)
        self.class_objects[i]["class_object"].current_x = event.xdata
        self.class_objects[i]["class_object"].current_y = event.ydata
        if self.click_increment == 0:
            self.click_increment = 1
        click(self,self.class_objects[i])
        self.change_canvas()
        update_pixel_info(self, self.class_objects[i])

    def keyPressEvent(self, event):
        i=str(self.match)
        if event.key() == Qt.Key_Up:
            if int(self.class_objects[i]["class_object"].current_y) + 1 < self.class_objects[i]["class_object"].Attributes["y"]:
                self.class_objects[i]["class_object"].current_y = self.class_objects[i]["class_object"].current_y + 1
                click(self,self.class_objects[i])
                self.change_canvas()
                update_pixel_info(self, self.class_objects[i])
        if event.key() == Qt.Key_Right:
            if int(self.class_objects[i]["class_object"].current_x) + 1 < self.class_objects[i]["class_object"].Attributes["x"]:
                self.class_objects[i]["class_object"].current_x = self.class_objects[i]["class_object"].current_x + 1
                click(self,self.class_objects[i])
                self.change_canvas()
                update_pixel_info(self, self.class_objects[i])
        if event.key() == Qt.Key_Down:
            if int(self.class_objects[i]["class_object"].current_y) - 1 >= 0:
                self.class_objects[i]["class_object"].current_y = self.class_objects[i]["class_object"].current_y - 1
                click(self,self.class_objects[i])
                self.change_canvas()
                update_pixel_info(self, self.class_objects[i])
        if event.key() == Qt.Key_Left:
            if int(self.class_objects[i]["class_object"].current_x) - 1 >= 0:
                self.class_objects[i]["class_object"].current_x = self.class_objects[i]["class_object"].current_x - 1
                click(self,self.class_objects[i])
                self.change_canvas()
                update_pixel_info(self, self.class_objects[i])
        if event.key() == Qt.Key_Q:
            self.frame_scale.setSliderPosition(int(self.frame_scale.value()-1))
            change_frame(self)
        if event.key() == Qt.Key_E:
            self.frame_scale.setSliderPosition(int(self.frame_scale.value()+1))
            change_frame(self)
        if event.key() == Qt.Key_A:
            self.wl_scale.setSliderPosition(int(self.wl_scale.value()-1))
            change_wl(self)
        if event.key() == Qt.Key_D:
            self.wl_scale.setSliderPosition(int(self.wl_scale.value()+1))
            change_wl(self)
        if event.key() == Qt.Key_Z:
            self.optical_depth_scale.setSliderPosition(int(self.optical_depth_scale.value()-1))
            change_optical_depth(self)
        if event.key() == Qt.Key_C:
            self.optical_depth_scale.setSliderPosition(int(self.optical_depth_scale.value()+1))
            change_optical_depth(self)



    def colour_table_options(self):
        if self.w is None:
            self.w = ColourTables(self)
            self.w.show()
        else:
            self.w.close()
            self.w = None

    def preferences(self):
        if self.p is None:
            self.p = Preferences(self)
            self.p.show()
        else:
            self.p.close()
            self.p = None

class ColourTables(QWidget):
    def __init__(self,sire):
        super().__init__()
        colour_table_widgets(self,sire)
        colour_table_layouts(self,sire)

class Preferences(QWidget):
    def __init__(self,sire):
        super().__init__()
        preferences_widgets(self,sire)
        preferences_layouts(self,sire)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SIRExplorer()
    window.show()
    sys.exit(app.exec_())

