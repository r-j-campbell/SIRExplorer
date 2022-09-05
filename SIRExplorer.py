from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sys
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSettings
from design import layouts, widgets, colour_table_layouts, colour_table_widgets, preferences_layouts, preferences_widgets, sfa_layouts, sfa_widgets
from Instruments import SIR
from canvas_functions import show, click, update_pixel_info, change_frame, change_wl, change_optical_depth, create_figure1,clear_fig1
import os

class SIRExplorer(QWidget):
    def __init__(self):
        super().__init__()
        QSettings().clear()
        self.setWindowTitle("SIR Explorer")
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.appheight = self.screenRect.height()
        self.appwidth = self.screenRect.width()
        self.setGeometry(0,0,int(self.appwidth),int(self.appheight))
        self.settings = QSettings("SIRE", "SIRE")

        self.only_int = QIntValidator()
        self.only_double = QDoubleValidator()

        self.increment = 0 #zero on first launch, 1 thereafter
        self.click_increment = 0
        self.flag = None
        self.match = 0 #zero when no match is found, index of dataset_dict otherwise
        self.frame_changed_flag = 0 #1 when framescale released, otherwise 0
        self.reload_flag = False #set to 1 when dataset_dict to be overwritten

        self.dataset_dict = {0: {"file": "first dummy value"}}
        self.folder_list = [None]
        self.model1_file_list = [None]
        self.model2_file_list = [None]
        self.obs_prof_file_list = [None]
        self.syn_prof_file_list = [None]
        self.mac1_file_list = [None]
        self.mac2_file_list = [None]
        self.chi2_file_list = [None]
        self.binary_file_list = [None]

        self.map_modes = ["2 models (1 magnetic, 2 non-magnetic)", "2 models (both magnetic)"]
        self.CT_flag = None
        self.preferences_flag = None
        self.sfa_flag = None

        #load settings for maps or set to default values if no settings saved
        if self.settings.value('StkI_CT') is not None:
            self.StkI_CT = self.settings.value('StkI_CT')
        else:
            self.StkI_CT = ['gray', 0.9, 1.1, 1, 1, 'dashed', 'red'] #[cmap, vmin, vmax, automatic scaling flag, display flag, linestyle, linecolour]
        if self.settings.value('StkQ_CT') is not None:
            self.StkQ_CT = self.settings.value('StkQ_CT')
        else:
            self.StkQ_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        if self.settings.value('StkU_CT') is not None:
            self.StkU_CT = self.settings.value('StkU_CT')
        else:
            self.StkU_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        if self.settings.value('StkV_CT') is not None:
            self.StkV_CT = self.settings.value('StkV_CT')
        else:
            self.StkV_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        if self.settings.value('T_CT') is not None:
            self.T_CT = self.settings.value('T_CT')
        else:
            self.T_CT = ['gray', 6500, 7500, 1, 1, 'dashed', 'red']
        if self.settings.value('B_CT') is not None:
            self.B_CT = self.settings.value('B_CT')
        else:
            self.B_CT = ['viridis', 0, 2000, 1, 1, 'dashed', 'red']
        if self.settings.value('V_CT') is not None:
            self.V_CT = self.settings.value('V_CT')
        else:
            self.V_CT = ['bwr', -4, 4, 1, 1, 'dashed', 'red']
        if self.settings.value('G_CT') is not None:
            self.G_CT = self.settings.value('G_CT')
        else:
            self.G_CT = ['bwr', 0, 180, 1, 1, 'dashed', 'cyan']
        if self.settings.value('A_CT') is not None:
            self.A_CT = self.settings.value('A_CT')
        else:
            self.A_CT = ['hsv', 0, 360, 1, 1, 'dashed', 'red']
        #uncomment below to reset Qsettings to default
        # self.StkI_CT = ['gray', 0.9, 1.1, 1, 1, 'dashed', 'red']
        # self.StkQ_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        # self.StkU_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        # self.StkV_CT = ['bwr', -0.005, 0.005, 1, 1, 'dashed', 'red']
        # self.T_CT = ['gray', 6500, 7500, 1, 1, 'dashed', 'red']
        # self.B_CT = ['viridis', 0, 2000, 1, 1, 'dashed', 'red']
        # self.V_CT = ['bwr', -4, 4, 1, 1, 'dashed', 'red']
        # self.G_CT = ['bwr', 0, 180, 1, 1, 'dashed', 'cyan']
        # self.A_CT = ['hsv', 0, 360, 1, 1, 'dashed', 'red']
        # print(self.V_CT)
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

        self.fontsize_titles = 7
        self.fontsize_axislabels = 7
        self.fontsize_ticklabels = 7
        self.line_widths = 1
        self.line_styles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.line_colours = ['black', 'gray', 'blue', 'red', 'green', 'white', 'yellow', 'purple', 'orange', 'magenta', 'cyan']

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
        if os.path.exists(value):
            if value not in self.model1_file_list:
                self.model1_file_list.append(value)
                self.select_model1.addItem(value)
            index = self.select_model1.findText(value)
            if index >= 0:
                self.select_model1.setCurrentIndex(index)
            del value
        else:
            msg = QMessageBox()
            msg.setText("Primary model file does not exist in selected folder.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        value = str(self.select_folder.currentText())+"/obs_prof.fits"
        if os.path.exists(value):
            if value not in self.obs_prof_file_list:
                self.obs_prof_file_list.append(value)
                self.select_obs_prof.addItem(value)
            index = self.select_obs_prof.findText(value)
            if index >= 0:
                self.select_obs_prof.setCurrentIndex(index)
            del value
        else:
            msg = QMessageBox()
            msg.setText("Observed profiles file does not exist in selected folder.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        value = str(self.select_folder.currentText())+"/syn_prof.fits"
        if os.path.exists(value):
            if value not in self.syn_prof_file_list:
                self.syn_prof_file_list.append(value)
                self.select_syn_prof.addItem(value)
            index = self.select_syn_prof.findText(value)
            if index >= 0:
                self.select_syn_prof.setCurrentIndex(index)
            del value
        else:
            msg = QMessageBox()
            msg.setText("Synthetic profiles file does not exist in selected folder.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        if self.model2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mod2.fits"
            if os.path.exists(value):
                if value not in self.model2_file_list:
                    self.model2_file_list.append(value)
                    self.select_model2.addItem(value)
                index = self.select_model2.findText(value)
                if index >= 0:
                    self.select_model2.setCurrentIndex(index)
                del value
            else:
                msg = QMessageBox()
                msg.setText("Secondary model file does not exist in selected folder.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

        if self.mac1_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac1.fits"
            if os.path.exists(value):
                if value not in self.mac1_file_list:
                    self.mac1_file_list.append(value)
                    self.select_mac1.addItem(value)
                index = self.select_mac1.findText(value)
                if index >= 0:
                    self.select_mac1.setCurrentIndex(index)
                del value
            else:
                msg = QMessageBox()
                msg.setText("Primary macroturbulence file does not exist in selected folder.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

        if self.mac2_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/mac2.fits"
            if os.path.exists(value):
                if value not in self.mac2_file_list:
                    self.mac2_file_list.append(value)
                    self.select_mac2.addItem(value)
                index = self.select_mac2.findText(value)
                if index >= 0:
                    self.select_mac2.setCurrentIndex(index)
                del value
            else:
                msg = QMessageBox()
                msg.setText("Secondary macroturbulence file does not exist in selected folder.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

        if self.binary_checkbutton.isChecked():
            value = str(self.select_folder.currentText())+"/binary.fits"
            if os.path.exists(value):
                if value not in self.binary_file_list:
                    self.binary_file_list.append(value)
                    self.select_binary.addItem(value)
                index = self.select_binary.findText(value)
                if index >= 0:
                    self.select_binary.setCurrentIndex(index)
                del value
            else:
                msg = QMessageBox()
                msg.setText("Binary file does not exist in selected folder.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

    def get_all_values(self,nested_dictionary, i, match): #searches nested dictionary for datasets that are already loaded
        for key, value in nested_dictionary.items():
            if type(value) is dict:
                i+=1
                self.get_all_values(value, i, match)
            else:
                if value == match:
                    self.flag=True
                    self.match = i-1
                    return

    def display_validation(self):
        missing_files = []
        if not os.path.exists(str(self.select_model1.currentText())):
            missing_files.append("Primary models")
        if not os.path.exists(str(self.select_obs_prof.currentText())):
            missing_files.append("Observed profiles")
        if not os.path.exists(str(self.select_syn_prof.currentText())):
            missing_files.append("Synthetic profiles")
        if not os.path.exists(str(self.select_model2.currentText())) and self.model2_checkbutton.isChecked():
            missing_files.append("Secondary models")
        if not os.path.exists(str(self.select_mac1.currentText())) and self.mac1_checkbutton.isChecked():
            missing_files.append("Primary macroturbulence")
        if not os.path.exists(str(self.select_mac2.currentText())) and self.mac2_checkbutton.isChecked():
            missing_files.append("Secondary macroturbulence")
        if not os.path.exists(str(self.select_binary.currentText())) and self.binary_checkbutton.isChecked():
            missing_files.append("Binary map")

        if len(missing_files) > 0:
            msg = QMessageBox()
            missing_message = ""
            for m in range(0,len(missing_files)):
                missing_message+=missing_files[m]+"\n"
            msg.setText("The following files do not exist:\n"+missing_message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return False
        return True

    def reload(self):
        self.reload_flag = True
        self.sc1.fig1.clf()
        create_figure1(self)
        self.change_canvas()
        self.reload_flag = False

    def change_canvas(self): #changes the map figure
        if self.display_validation():
            self.flag = False
            self.get_all_values(self.dataset_dict,0,self.select_model1.currentText())
            if self.flag: #if match is found
                i=str(self.match)
                sir = SIR()
                if self.reload_flag:
                    self.flag = False
                    self.dataset_dict[i] = {'model_file': self.select_model1.currentText(),
                                        'secondary_model_file': self.select_model2.currentText(),
                                        'obs_prof_file': self.select_obs_prof.currentText(),
                                        'syn_prof_file': self.select_syn_prof.currentText(),
                                        'mac1_file': self.select_mac1.currentText(),
                                        'mac2_file': self.select_mac2.currentText(),
                                        'binary_file': self.select_binary.currentText(),
                                        'sir': sir
                                         }
                    show(self,self.dataset_dict[i])
                    click(self,self.dataset_dict[i])
                    update_pixel_info(self, self.dataset_dict[i])
                else:
                    show(self,self.dataset_dict[i])
            elif not self.flag: #if match is not found
                sir = SIR()
                j=str(len(self.dataset_dict))
                self.match = j
                self.dataset_dict[j] = {'model_file': self.select_model1.currentText(),
                                        'secondary_model_file': self.select_model2.currentText(),
                                        'obs_prof_file': self.select_obs_prof.currentText(),
                                        'syn_prof_file': self.select_syn_prof.currentText(),
                                        'mac1_file': self.select_mac1.currentText(),
                                        'mac2_file': self.select_mac2.currentText(),
                                        'binary_file': self.select_binary.currentText(),
                                        'sir': sir
                                         }
                show(self,self.dataset_dict[j])
            if self.increment == 0:
                click(self,self.dataset_dict[j])
                update_pixel_info(self, self.dataset_dict[j])
                if self.click_increment == 0:
                    self.click_increment = 1
                self.increment = 1
        else:
            pass

    def mouseclicks(self, event): #called when user clicks one of the maps
        self.setFocus()
        if event.xdata is not None and event.ydata is not None:
            i=str(self.match)
            self.dataset_dict[i]["sir"].current_x = event.xdata
            self.dataset_dict[i]["sir"].current_y = event.ydata
            if self.click_increment == 0:
                self.click_increment = 1
            click(self,self.dataset_dict[i])
            self.change_canvas()
            update_pixel_info(self, self.dataset_dict[i])
        else:
            msg = QMessageBox()
            msg.setText("You must click one of the maps.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def keyPressEvent(self, event): #called when user presses up, down, left, right, Q, E, A, D, Z or C keys
        if self.increment == 1:
            i=str(self.match)
            if event.key() == Qt.Key_Up:
                if int(self.dataset_dict[i]["sir"].current_y) + 1 < self.dataset_dict[i]["sir"].Attributes["y"]:
                    self.dataset_dict[i]["sir"].current_y = self.dataset_dict[i]["sir"].current_y + 1
                    click(self,self.dataset_dict[i])
                    self.change_canvas()
                    update_pixel_info(self, self.dataset_dict[i])
            if event.key() == Qt.Key_Right:
                if int(self.dataset_dict[i]["sir"].current_x) + 1 < self.dataset_dict[i]["sir"].Attributes["x"]:
                    self.dataset_dict[i]["sir"].current_x = self.dataset_dict[i]["sir"].current_x + 1
                    click(self,self.dataset_dict[i])
                    self.change_canvas()
                    update_pixel_info(self, self.dataset_dict[i])
            if event.key() == Qt.Key_Down:
                if int(self.dataset_dict[i]["sir"].current_y) - 1 >= 0:
                    self.dataset_dict[i]["sir"].current_y = self.dataset_dict[i]["sir"].current_y - 1
                    click(self,self.dataset_dict[i])
                    self.change_canvas()
                    update_pixel_info(self, self.dataset_dict[i])
            if event.key() == Qt.Key_Left:
                if int(self.dataset_dict[i]["sir"].current_x) - 1 >= 0:
                    self.dataset_dict[i]["sir"].current_x = self.dataset_dict[i]["sir"].current_x - 1
                    click(self,self.dataset_dict[i])
                    self.change_canvas()
                    update_pixel_info(self, self.dataset_dict[i])
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
        else:
            pass

    def colour_table_options(self):
        if self.CT_flag is None:
            self.CT_flag = ColourTables(self)
            self.CT_flag.show()
        else:
            self.CT_flag.close()
            self.CT_flag = None

    def preferences(self):
        if self.preferences_flag is None:
            self.preferences_flag = Preferences(self)
            self.preferences_flag.show()
        else:
            self.preferences_flag.close()
            self.preferences_flag = None

    def sfa(self):
        if self.sfa_flag is None:
            self.sfa_flag = StrongFieldApproximation(self)
            self.sfa_flag.show()
        else:
            self.sfa_flag.close()
            self.sfa_flag = None

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

class StrongFieldApproximation(QWidget):
    def __init__(self,sire):
        super().__init__()
        sfa_widgets(self,sire)
        sfa_layouts(self,sire)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SIRExplorer()
    window.show()
    sys.exit(app.exec_())

