import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import astropy.io.fits as pyfits
import matplotlib
matplotlib.use("TkAgg")
matplotlib.rc('image',interpolation='none',origin='lower')
from PyQt5.QtWidgets import QMessageBox

def show(self, class_object):
    if self.increment == 0:
        create_figure1(self)
        create_figure2(self)
        create_figure3(self)
    if self.increment == 1 or self.frame_flag == 1:
        self.sc1.ax1.clear()
        self.sc1.ax2.clear()
        self.sc1.ax3.clear()
        self.sc1.ax4.clear()
        self.sc1.ax5.clear()
        self.sc1.ax6.clear()
        self.sc1.ax7.clear()
        self.sc1.ax8.clear()
        self.sc1.ax9.clear()
        remove_cbars(self)

    if self.flag == False or self.frame_flag == 1:
        open_files(self,class_object)

    update_canvas(self,class_object)
    self.sc1.fig1.canvas.draw()


def open_files(self,class_object):
    model1 = pyfits.open(class_object["model_file"])[0].data
    obs_prof = pyfits.open(class_object["obs_prof_file"])[0].data
    syn_prof = pyfits.open(class_object["syn_prof_file"])[0].data
    model1 = np.squeeze(model1)
    obs_prof = np.squeeze(obs_prof)
    syn_prof = np.squeeze(syn_prof)
    if model1.ndim == 4:
        self.frame_flag = 0
    if model1.ndim == 5:  # executed only if there are multiple frames of data
        self.frame_flag = 1
        class_object["class_object"].Attributes["t"] = model1.shape[0]
        model1 = model1[class_object["class_object"].current_frame_index, :, :, :, :]
        obs_prof = obs_prof[class_object["class_object"].current_frame_index, :, :, :, :]
        syn_prof = syn_prof[class_object["class_object"].current_frame_index, :, :, :, :]
        self.frame_scale.setMinimum(0)
        self.frame_scale.setMaximum(class_object['class_object'].Attributes["t"] - 1)
    class_object["class_object"].Attributes["optical_depth"] = model1.shape[1]
    class_object["class_object"].Attributes["y"] = model1.shape[2]
    class_object["class_object"].Attributes["x"] = model1.shape[3]
    class_object["class_object"].Attributes["wl"] = obs_prof.shape[1]
    self.x_spinbox.setRange(0,class_object["class_object"].Attributes["x"]-1)
    self.y_spinbox.setRange(0,class_object["class_object"].Attributes["y"]-1)

    if self.flag == False:
        self.wl_scale.setMinimum(0)
        self.wl_scale.setMaximum(class_object["class_object"].Attributes["wl"] - 1)
        self.optical_depth_scale.setMinimum(0)
        self.optical_depth_scale.setMaximum(class_object["class_object"].Attributes["optical_depth"] - 1)

        class_object["class_object"].wl_min = 0
        class_object["class_object"].wl_max = class_object["class_object"].Attributes["wl"] -1
        self.wl_min_entry.setEnabled(True)
        self.wl_min_entry.setText(str(0))
        self.wl_max_entry.setEnabled(True)
        self.wl_max_entry.setText(str(class_object["class_object"].Attributes["wl"] - 1))

        class_object["class_object"].optical_depth_min = 0
        class_object["class_object"].optical_depth_max = class_object["class_object"].Attributes["optical_depth"] - 1
        self.optical_depth_min_entry.setEnabled(True)
        self.optical_depth_min_entry.setText(str(0))
        self.optical_depth_max_entry.setEnabled(True)
        self.optical_depth_max_entry.setText(str(class_object["class_object"].Attributes["optical_depth"] - 1))

    class_object["class_object"].update_model1(model1)
    class_object["class_object"].update_obs(obs_prof)
    class_object["class_object"].update_syn(syn_prof)
    if self.binary_checkbutton.isChecked():
        binary_map = pyfits.open(class_object["binary_file"])[0].data
        binary_map = np.squeeze(binary_map)
        if binary_map.ndim == 3:  # executed only if there are multiple frames of data
            binary_map = binary_map[class_object["class_object"].current_frame_index, :, :]
        class_object["class_object"].update_binary(binary_map)
    else:
        binary_map = np.ones(
            [class_object["class_object"].Attributes["y"], class_object["class_object"].Attributes["x"]])
        class_object["class_object"].update_binary(binary_map)

    if self.model2_checkbutton.isChecked() and self.mac1_checkbutton.isChecked() and self.mac2_checkbutton.isChecked():
        if self.flag == False or self.frame_flag == 1:
            model2 = pyfits.open(class_object["secondary_model_file"])[0].data
            model2 = np.squeeze(model2)
            mac1_file = pyfits.open(class_object["mac1_file"])[0].data
            mac1_file = np.squeeze(mac1_file)
            mac2_file = pyfits.open(class_object["mac2_file"])[0].data
            mac2_file = np.squeeze(mac2_file)
            if model2.ndim == 5:  # executed only if there are multiple frames of data
                model2 = model2[class_object["class_object"].current_frame_index, :, :, :, :]
                mac1_file = mac1_file[class_object["class_object"].current_frame_index, :, :, :]
                mac2_file = mac2_file[class_object["class_object"].current_frame_index, :, :, :]
            class_object["class_object"].update_model2(model2)
            class_object["class_object"].update_mac1(mac1_file)
            class_object["class_object"].update_mac2(mac2_file)
    elif self.model2_checkbutton.isChecked() == False and self.mac1_checkbutton.isChecked():
        if self.flag == False or self.frame_flag == 1:
            mac1_file = pyfits.open(class_object["mac1_file"])[0].data
            mac1_file = np.squeeze(mac1_file)
            if mac1_file.ndim == 4:  # executed only if there are multiple frames of data
                mac1_file = mac1_file[class_object["class_object"].current_frame_index, :, :, :]
            class_object["class_object"].updatemac1(mac1_file)
    elif self.model2_checkbutton.isChecked() and self.mac1_checkbutton.isChecked() and self.mac2_checkbutton.isChecked() == False:
        if self.flag == False or self.frame_flag == 1:
            model2 = pyfits.open(class_object["secondary_model_file"])[0].data
            model2 = np.squeeze(model2)
            mac1_file = pyfits.open(class_object["mac1_file"])[0].data
            mac1_file = np.squeeze(mac1_file)
            if model2.ndim == 5:  # executed only if there are multiple frames of data
                mac1_file = mac1_file[class_object["class_object"].current_frame_index, :, :, :]
                model2 = model2[class_object["class_object"].current_frame_index, :, :, :, :]
            class_object["class_object"].update_model2(model2)
            class_object["class_object"].update_mac1(mac1_file)
            mac2_file = np.empty((3, model1.shape[2], model1.shape[3]))  # create dummy mac2 file
            mac2_file[1, :, :] = np.subtract(np.ones((model1.shape[2], model1.shape[3])), mac1_file[1, :, :])  # update dummy mac2 file filling factor as (1 - mac1) when mac2 not provided"
            class_object["class_object"].update_mac2(mac2_file)


def update_canvas(self,class_object):
    model1 = class_object["class_object"].model1
    model2 = class_object["class_object"].model2
    obs_prof = class_object["class_object"].obs
    syn_prof = class_object["class_object"].syn
    binary_map = class_object["class_object"].binary
    mac1_file = class_object["class_object"].mac1
    mac2_file = class_object["class_object"].mac2
    current_x = int(class_object["class_object"].current_x)
    current_y = int(class_object["class_object"].current_y)
    if self.Stokes_checkbutton.isChecked():
        if self.StkI_CT[3] == 0:
            StkI_map = self.sc1.ax1.imshow(obs_prof[0, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkI_CT[0], vmin=self.StkI_CT[1], vmax=self.StkI_CT[2])
        elif self.StkI_CT[3] == 1:
            StkI_map = self.sc1.ax1.imshow(obs_prof[0, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkI_CT[0])
        dividerStkI = make_axes_locatable(self.sc1.ax1)
        self.caxStkI = dividerStkI.append_axes("right", size="3%", pad=0)
        self.cbar_StkI = self.sc1.fig1.colorbar(StkI_map, cax=self.caxStkI, pad=0)
        self.cbar_StkI.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax1.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax1.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax1.set_title("Stokes $I$ [$I_c$]", fontsize=self.fontsize_titles)
        self.sc1.ax1.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax1.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.Stokes_Q_checkbutton.isChecked():
        if self.StkQ_CT[3] == 0:
            StkQ_map = self.sc1.ax2.imshow(obs_prof[1, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkQ_CT[0], vmin=self.StkQ_CT[1], vmax=self.StkQ_CT[2])
        elif self.StkQ_CT[3] == 1:
            StkQ_map = self.sc1.ax2.imshow(obs_prof[1, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkQ_CT[0])
        dividerStkQ = make_axes_locatable(self.sc1.ax2)
        self.caxStkQ = dividerStkQ.append_axes("right", size="3%", pad=0)
        self.cbar_StkQ = self.sc1.fig1.colorbar(StkQ_map, cax=self.caxStkQ, pad=0)
        self.cbar_StkQ.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax2.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax2.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax2.set_title("Stokes $Q$ [$I_c$]", fontsize=self.fontsize_titles)
        self.sc1.ax2.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax2.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.Stokes_U_checkbutton.isChecked():
        if self.StkU_CT[3] == 0:
            StkU_map = self.sc1.ax3.imshow(obs_prof[2, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkU_CT[0], vmin=self.StkU_CT[1], vmax=self.StkU_CT[2])
        elif self.StkU_CT[3] == 1:
            StkU_map = self.sc1.ax3.imshow(obs_prof[2, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkU_CT[0])
        dividerStkU = make_axes_locatable(self.sc1.ax3)
        self.caxStkU = dividerStkU.append_axes("right", size="3%", pad=0)
        self.cbar_StkU = self.sc1.fig1.colorbar(StkU_map, cax=self.caxStkU, pad=0)
        self.cbar_StkU.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax3.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax3.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax3.set_title("Stokes $U$ [$I_c$]", fontsize=self.fontsize_titles)
        self.sc1.ax3.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax3.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.Stokes_V_checkbutton.isChecked():
        if self.StkV_CT[3] == 0:
            StkV_map = self.sc1.ax4.imshow(obs_prof[3, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkV_CT[0], vmin=self.StkV_CT[1], vmax=self.StkV_CT[2])
        elif self.StkV_CT[3] == 1:
            StkV_map = self.sc1.ax4.imshow(obs_prof[3, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.StkV_CT[0])
        dividerStkV = make_axes_locatable(self.sc1.ax4)
        self.caxStkV = dividerStkV.append_axes("right", size="3%", pad=0)
        self.cbar_StkV = self.sc1.fig1.colorbar(StkV_map, cax=self.caxStkV, pad=0)
        self.cbar_StkV.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax4.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax4.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax4.set_title("Stokes $V$ [$I_c$]", fontsize=self.fontsize_titles)
        self.sc1.ax4.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax4.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.T_checkbutton.isChecked():
        if self.T_CT[3] == 0:
            T_map = self.sc1.ax5.imshow(model1[1, class_object["class_object"].current_optical_depth_index, :, :],
                    origin='lower', cmap=self.T_CT[0], vmin=self.T_CT[1], vmax=self.T_CT[2])
        elif self.T_CT[3] == 1:
            T_map = self.sc1.ax5.imshow(model1[1, class_object["class_object"].current_optical_depth_index, :, :],
                    origin='lower', cmap=self.T_CT[0])
        dividerT = make_axes_locatable(self.sc1.ax5)
        self.caxT = dividerT.append_axes("right", size="3%", pad=0)
        self.cbar_T = self.sc1.fig1.colorbar(T_map, cax=self.caxT, pad=0)
        self.cbar_T.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax5.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax5.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax5.set_title("T [K]", fontsize=self.fontsize_titles)
        self.sc1.ax5.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax5.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.B_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.B_CT[3] == 0:
                B_map = self.sc1.ax6.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', vmin=self.B_CT[1], vmax=self.B_CT[2], cmap=self.B_CT[0])
            elif self.B_CT[3] == 1:
                B_map = self.sc1.ax6.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', cmap=self.B_CT[0], interpolation='none')
            self.sc1.ax6.set_title("$\\alpha$ B [G]", fontsize=self.fontsize_titles)
        else:
            if self.B_CT[3] == 0:
                B_map = self.sc1.ax6.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.B_CT[1], vmax=self.B_CT[2], cmap=self.B_CT[0])
            elif self.B_CT[3] == 1:
                B_map = self.sc1.ax6.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.B_CT[0], interpolation='none')
            self.sc1.ax6.set_title("B [G]", fontsize=self.fontsize_titles)
        dividerB = make_axes_locatable(self.sc1.ax6)
        self.caxB = dividerB.append_axes("right", size="3%", pad=0)
        self.cbar_B = self.sc1.fig1.colorbar(B_map, cax=self.caxB, pad=0)
        self.cbar_B.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax6.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax6.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax6.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax6.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.V_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            combined_V = np.empty([class_object["class_object"].Attributes["y"], class_object["class_object"].Attributes["x"]]) * np.nan
            combined_V = (model2[5, class_object["class_object"].current_optical_depth_index, :, :] * mac2_file[1, :, :]) + (model1[5, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :])
            if self.V_CT[3] == 0:
                V_map = self.sc1.ax7.imshow((combined_V / (100 * 1000)), origin='lower', cmap=self.V_CT[0], vmin=self.V_CT[1], vmax=self.V_CT[2])
            elif self.V_CT[3] == 1:
                V_map = self.sc1.ax7.imshow((combined_V / (100 * 1000)), origin='lower', cmap=self.V_CT[0])
        else:
            if self.V_CT[3] == 0:
                V_map = self.sc1.ax7.imshow(
                    (model1[5, class_object["class_object"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=self.V_CT[0], vmin=self.V_CT[1], vmax=self.V_CT[2])
            elif self.V_CT[3] == 1:
                V_map = self.sc1.ax7.imshow(
                    (model1[5, class_object["class_object"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=self.V_CT[0])
        dividerV = make_axes_locatable(self.sc1.ax7)
        self.caxV = dividerV.append_axes("right", size="3%", pad=0)
        self.cbar_V = self.sc1.fig1.colorbar(V_map, cax=self.caxV, pad=0)
        self.cbar_V.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax7.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax7.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax7.set_title("$v_\mathrm{{LOS}}$ [km/s]", fontsize=self.fontsize_titles)
        self.sc1.ax7.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax7.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.G_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.G_CT[3] == 0:
                G_map = self.sc1.ax8.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.G_CT[1], vmax=self.G_CT[2], cmap=self.G_CT[0])
            elif self.G_CT[3] == 1:
                G_map = self.sc1.ax8.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.G_CT[0])
        else:
            if self.G_CT[3] == 0:
                G_map = self.sc1.ax8.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.G_CT[1], vmax=self.G_CT[2], cmap=self.G_CT[0])
            if self.G_CT[3] == 1:
                G_map = self.sc1.ax8.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.G_CT[0])
        dividerG = make_axes_locatable(self.sc1.ax8)
        self.caxG = dividerG.append_axes("right", size="3%", pad=0)
        self.cbar_G = self.sc1.fig1.colorbar(G_map, cax=self.caxG, pad=0)
        self.cbar_G.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax8.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax8.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax8.set_title("$\\gamma$ [deg.]", fontsize=self.fontsize_titles)
        self.sc1.ax8.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax8.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    if self.A_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.A_CT[3] == 0:
                A_map = self.sc1.ax9.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0], vmin=self.A_CT[1], vmax=self.A_CT[2])
            elif self.A_CT[3] == 1:
                A_map = self.sc1.ax9.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0])
        else:
            if self.A_CT[3] == 0:
                A_map = self.sc1.ax9.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0], vmin=self.A_CT[1], vmax=self.A_CT[2])
            elif self.A_CT[3] == 1:
                A_map = self.sc1.ax9.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0])
        dividerA = make_axes_locatable(self.sc1.ax9)
        self.caxA = dividerA.append_axes("right", size="3%", pad=0)
        self.cbar_A = self.sc1.fig1.colorbar(A_map, cax=self.caxA, pad=0)
        self.cbar_A.ax.tick_params(labelsize=self.fontsize_ticklabels)
        self.sc1.ax9.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax9.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
        self.sc1.ax9.set_title("$\\phi$ [deg.]", fontsize=self.fontsize_titles)
        self.sc1.ax9.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
        self.sc1.ax9.set_ylabel("Y [pix.]", fontsize=self.fontsize_axislabels)

    del model1, model2, syn_prof, obs_prof, binary_map, mac1_file, mac2_file


def click(self, class_object):
    current_x = class_object["class_object"].current_x
    current_y = class_object["class_object"].current_y
    if self.click_increment == 1:
        self.sc2.ax1.clear()
        self.sc2.ax2.clear()
        self.sc2.ax3.clear()
        self.sc2.ax4.clear()
        self.sc3.ax1.clear()
        self.sc3.ax2.clear()
        self.sc3.ax3.clear()
        self.sc3.ax4.clear()
    self.sc3.ax1.set_title("T [K]", fontsize=self.fontsize_titles)
    self.sc3.ax2.set_title("B [G]", fontsize=self.fontsize_titles)
    self.sc3.ax3.set_title("$v_\mathrm{{LOS}}$ [km/s]", fontsize=self.fontsize_titles)
    self.sc3.ax4.set_title("$\\gamma$ (solid), $\\phi$ (dashed) [deg.]", fontsize=self.fontsize_titles)
    self.sc3.ax1.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=self.fontsize_axislabels)
    self.sc3.ax2.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=self.fontsize_axislabels)
    self.sc3.ax3.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=self.fontsize_axislabels)
    self.sc3.ax4.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=self.fontsize_axislabels)
    self.sc2.ax1.set_title("Stokes $I$ [$I_c$]", fontsize=self.fontsize_titles)
    self.sc2.ax2.set_title("Stokes $Q$ [$I_c$]", fontsize=self.fontsize_titles)
    self.sc2.ax3.set_title("Stokes $U$ [$I_c$]", fontsize=self.fontsize_titles)
    self.sc2.ax4.set_title("Stokes $V$ [$I_c$]", fontsize=self.fontsize_titles)
    self.sc2.ax1.set_xlabel("wavelength [pix.]", fontsize=self.fontsize_axislabels)
    self.sc2.ax2.set_xlabel("wavelength [pix.]", fontsize=self.fontsize_axislabels)
    self.sc2.ax3.set_xlabel("wavelength [pix.]", fontsize=self.fontsize_axislabels)
    self.sc2.ax4.set_xlabel("wavelength [pix.]", fontsize=self.fontsize_axislabels)

    model1 = class_object["class_object"].model1
    obs_prof = class_object["class_object"].obs
    syn_prof = class_object["class_object"].syn

    # Stokes plots
    self.sc2.ax1.plot(obs_prof[0, :, int(current_y), int(current_x)], label='Obs', linewidth=self.linewidth)
    self.sc2.ax1.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax1.plot(syn_prof[0, :, int(current_y), int(current_x)], label='Syn', linewidth=self.linewidth)
    self.sc2.ax1.legend(frameon=False, fontsize=self.fontsize_axislabels)
    self.sc2.ax1.set_xlim(class_object["class_object"].wl_min, class_object["class_object"].wl_max)
    self.sc2.ax2.plot(obs_prof[1, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax2.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax2.plot(syn_prof[1, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax2.set_xlim(class_object["class_object"].wl_min, class_object["class_object"].wl_max)
    self.sc2.ax3.plot(obs_prof[2, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax3.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax3.plot(syn_prof[2, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax3.set_xlim(class_object["class_object"].wl_min, class_object["class_object"].wl_max)
    self.sc2.ax4.plot(obs_prof[3, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax4.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax4.plot(syn_prof[3, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax4.set_xlim(class_object["class_object"].wl_min, class_object["class_object"].wl_max)

    # Model parameter plots
    self.sc3.ax1.plot(model1[0, :, int(current_y), int(current_x)], model1[1, :, int(current_y), int(current_x)], label="mod 1",
        linestyle='solid',color='red', linewidth=self.linewidth)
    self.sc3.ax1.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax1.set_xlim(model1[0, class_object["class_object"].optical_depth_min, int(current_y), int(current_x)], model1[0, class_object["class_object"].optical_depth_max, int(current_y), int(current_x)])

    self.sc3.ax2.plot(model1[0, :, int(current_y), int(current_x)], model1[4, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=self.linewidth)
    self.sc3.ax2.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax2.set_xlim(model1[0, class_object["class_object"].optical_depth_min, int(current_y), int(current_x)], model1[0, class_object["class_object"].optical_depth_max, int(current_y), int(current_x)])

    self.sc3.ax3.plot(model1[0, :, int(current_y), int(current_x)], model1[5, :, int(current_y), int(current_x)] / (100 * 1000),
        linestyle='solid', color='red', linewidth=self.linewidth)
    self.sc3.ax3.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax3.set_xlim(model1[0, class_object["class_object"].optical_depth_min, int(current_y), int(current_x)], model1[0, class_object["class_object"].optical_depth_max, int(current_y), int(current_x)])

    self.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[6, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=self.linewidth)  # inclination
    self.sc3.ax4.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[7, :, int(current_y), int(current_x)],
        linestyle=':', color='red', linewidth=self.linewidth)  # azimuth
    self.sc3.ax4.set_xlim(model1[0, class_object["class_object"].optical_depth_min, int(current_y), int(current_x)], model1[0, class_object["class_object"].optical_depth_max, int(current_y), int(current_x)])

    if self.model2_checkbutton.isChecked():
        model2 = class_object["class_object"].model2
        self.sc3.ax1.plot(model2[0, :, int(current_y), int(current_x)], model2[1, :, int(current_y), int(current_x)],
            label="mod 2", linestyle='solid', color='blue', linewidth=self.linewidth)
        self.sc3.ax1.legend(frameon=False, fontsize=self.fontsize_axislabels)
        self.sc3.ax2.plot(model2[0, :, int(current_y), int(current_x)], model2[4, :, int(current_y), int(current_x)],
            linestyle='solid', color='blue', linewidth=self.linewidth)
        self.sc3.ax3.plot(model2[0, :, int(current_y), int(current_x)], model2[5, :, int(current_y), int(current_x)] / (100 * 1000),
            linestyle='solid', color='blue', linewidth=self.linewidth)
        self.sc3.ax4.plot(model2[0, :, int(current_y), int(current_x)], model2[6, :, int(current_y), int(current_x)],
            linestyle='solid', color='blue', linewidth=self.linewidth)  # inclination
        self.sc3.ax4.plot(model2[0, :, int(current_y), int(current_x)], model2[7, :, int(current_y), int(current_x)],
            linestyle=':', color='blue', linewidth=self.linewidth)  # azimuth
        del model2

    self.sc2.fig2.canvas.draw()
    self.sc3.fig3.canvas.draw()

    del model1, obs_prof, syn_prof


def create_figure1(self):
    index=1
    total=0
    if self.Stokes_checkbutton.isChecked():
        total+=1
    if self.Stokes_Q_checkbutton.isChecked():
        total+=1
    if self.Stokes_U_checkbutton.isChecked():
        total+=1
    if self.Stokes_V_checkbutton.isChecked():
        total+=1
    if self.T_checkbutton.isChecked():
        total+=1
    if self.B_checkbutton.isChecked():
        total+=1
    if self.V_checkbutton.isChecked():
        total+=1
    if self.G_checkbutton.isChecked():
        total+=1
    if self.A_checkbutton.isChecked():
        total+=1
    if total >= 6:
        columns = 2
        if total % 2 == 0:
            rows = int(total/2)

        else:
            rows = int((total+1)/2)
    else:
        rows = int(total)
        columns = 1
    if self.Stokes_checkbutton.isChecked():
        self.sc1.ax1 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.Stokes_Q_checkbutton.isChecked():
        self.sc1.ax2 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.Stokes_U_checkbutton.isChecked():
        self.sc1.ax3 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.Stokes_V_checkbutton.isChecked():
        self.sc1.ax4 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.T_checkbutton.isChecked():
        self.sc1.ax5 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax5.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.B_checkbutton.isChecked():
        self.sc1.ax6 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax6.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.V_checkbutton.isChecked():
        self.sc1.ax7 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax7.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.G_checkbutton.isChecked():
        self.sc1.ax8 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax8.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        self.sc1.ax8.set_facecolor('xkcd:black')
        index+=1
    if self.A_checkbutton.isChecked():
        self.sc1.ax9 = self.sc1.fig1.add_subplot(rows,columns,index)
        self.sc1.ax9.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        self.sc1.ax9.set_facecolor('xkcd:black')
        index+=1


def clear_fig1(self):
    self.sc1.fig1.clf()
    create_figure1(self)
    self.flag=False
    self.get_all_values(self.class_objects,0,self.select_model1.currentText())
    if self.flag == True:
        i=str(self.match)
        if self.click_increment == 1:
            self.change_canvas()
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def create_figure2(self):
    index=1
    total=0
    if self.pI_checkbutton.isChecked():
        total+=1
    if self.pQ_checkbutton.isChecked():
        total+=1
    if self.pU_checkbutton.isChecked():
        total+=1
    if self.pV_checkbutton.isChecked():
        total+=1

    if self.pI_checkbutton.isChecked():
        self.sc2.ax1 = self.sc2.fig2.add_subplot(total,1,index)
        self.sc2.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.pQ_checkbutton.isChecked():
        self.sc2.ax2 = self.sc2.fig2.add_subplot(total,1,index)
        self.sc2.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.pU_checkbutton.isChecked():
        self.sc2.ax3 = self.sc2.fig2.add_subplot(total,1,index)
        self.sc2.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.pV_checkbutton.isChecked():
        self.sc2.ax4 = self.sc2.fig2.add_subplot(total,1,index)
        self.sc2.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1


def clear_fig2(self):
    self.sc2.fig2.clf()
    create_figure2(self)
    self.flag=False
    self.get_all_values(self.class_objects,0,self.select_model1.currentText())
    if self.flag == True:
        i=str(self.match)
        if self.click_increment == 1:
            click(self,self.class_objects[i])
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def create_figure3(self):
    index=1
    total=0
    if self.mT_checkbutton.isChecked():
        total+=1
    if self.mB_checkbutton.isChecked():
        total+=1
    if self.mV_checkbutton.isChecked():
        total+=1
    if self.mG_checkbutton.isChecked():
        total+=1
    if total <= 2:
        rows = 1
        columns = total
    else:
        rows = 2
        columns = 2
    if self.mT_checkbutton.isChecked():
        self.sc3.ax1 = self.sc3.fig3.add_subplot(columns,rows,index)
        self.sc3.ax1.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.mB_checkbutton.isChecked():
        self.sc3.ax2 = self.sc3.fig3.add_subplot(columns,rows,index)
        self.sc3.ax2.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.mV_checkbutton.isChecked():
        self.sc3.ax3 = self.sc3.fig3.add_subplot(columns,rows,index)
        self.sc3.ax3.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1
    if self.mG_checkbutton.isChecked():
        self.sc3.ax4 = self.sc3.fig3.add_subplot(columns,rows,index)
        self.sc3.ax4.tick_params(axis='both', labelsize=self.fontsize_ticklabels)
        index+=1


def clear_fig3(self):
    self.sc3.fig3.clf()
    create_figure3(self)
    self.flag=False
    self.get_all_values(self.class_objects,0,self.select_model1.currentText())
    if self.flag == True:
        i=str(self.match)
        if self.click_increment == 1:
            click(self,self.class_objects[i])
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def remove_cbars(self):
    try:
        self.caxStkI.remove()
    except:
        pass
    try:
        self.caxStkQ.remove()
    except:
        pass
    try:
        self.caxStkU.remove()
    except:
        pass
    try:
        self.caxStkV.remove()
    except:
        pass
    try:
        self.caxT.remove()
    except:
        pass
    try:
        self.caxB.remove()
    except:
        pass
    try:
        self.caxV.remove()
    except:
        pass
    try:
        self.caxG.remove()
    except:
        pass
    try:
        self.caxA.remove()
    except:
        pass


def set_wavelength_range(sire):
    i = str(sire.match)
    try:
        if int(sire.wl_min_entry.text()) >= 0 and int(sire.wl_max_entry.text()) < sire.class_objects[i]["class_object"].Attributes['wl']:
            sire.class_objects[i]["class_object"].wl_min = int(sire.wl_min_entry.text())
            sire.class_objects[i]["class_object"].wl_max = int(sire.wl_max_entry.text())
            click(sire, sire.class_objects[i])
        else:
            msg = QMessageBox()
            msg.setText("Selected range out of bounds.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            sire.wl_min_entry.setText(str(sire.class_objects[i]["class_object"].wl_min))
            sire.wl_max_entry.setText(str(sire.class_objects[i]["class_object"].wl_max))
    except ValueError:
        msg = QMessageBox()
        msg.setText("Value error. You must enter an integer as the index.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        sire.optical_depth_min_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_min))
        sire.optical_depth_max_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_max))



def set_optical_depth_range(sire):
    i = str(sire.match)
    try:
        if int(sire.optical_depth_min_entry.text()) >= 0 and int(sire.optical_depth_max_entry.text()) < sire.class_objects[i]["class_object"].Attributes['optical_depth']:
            sire.class_objects[i]["class_object"].optical_depth_min = int(sire.optical_depth_min_entry.text())
            sire.class_objects[i]["class_object"].optical_depth_max = int(sire.optical_depth_max_entry.text())
            click(sire, sire.class_objects[i])
        else:
            msg = QMessageBox()
            msg.setText("Selected range out of bounds.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            sire.optical_depth_min_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_min))
            sire.optical_depth_max_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_max))
    except ValueError:
            msg = QMessageBox()
            msg.setText("Value error. You must enter an integer as the index.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            sire.optical_depth_min_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_min))
            sire.optical_depth_max_entry.setText(str(sire.class_objects[i]["class_object"].optical_depth_max))


def change_frame(self):
    frame = int(self.frame_scale.value())
    i = str(self.match)
    self.class_objects[i]['class_object'].current_frame_index = int(frame)
    self.change_canvas()
    click(self, self.class_objects[i])
    update_pixel_info(self, self.class_objects[i])


def change_wl(self):
    wl = int(self.wl_scale.value())
    i = str(self.match)
    self.class_objects[i]['class_object'].current_wl_index = int(wl)
    self.change_canvas()
    click(self, self.class_objects[i])
    update_pixel_info(self, self.class_objects[i])


def change_optical_depth(self):
    optical_depth = int(self.optical_depth_scale.value())
    i = str(self.match)
    self.class_objects[i]['class_object'].current_optical_depth_index = int(optical_depth)
    self.change_canvas()
    click(self, self.class_objects[i])
    update_pixel_info(self, self.class_objects[i])


def update_pixel_info(sire, class_object):
    T1 = class_object["class_object"].model1[1,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
    G1 = class_object["class_object"].model1[6,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
    B1 = class_object["class_object"].model1[4,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
    A1 = class_object["class_object"].model1[7,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
    V1 = class_object["class_object"].model1[5,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]/(100*1000)
    mic1 = class_object["class_object"].model1[3,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
    if sire.mac1_checkbutton.isChecked():
        ff1 = class_object["class_object"].mac1[1, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        mac1 = class_object["class_object"].mac1[0, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        sire.mod1_mac_value.setText(str(round(mac1,3)))
    else:
        ff1 = 1
    sire.mod1_ff_value.setText(str(round(ff1,3)))
    sire.mod1_T_value.setText(str(round(T1,3)))
    sire.mod1_B_value.setText(str(round(B1,3)))
    sire.mod1_V_value.setText(str(round(V1,3)))
    sire.mod1_G_value.setText(str(round(G1,3)))
    sire.mod1_A_value.setText(str(round(A1,3)))
    sire.mod1_mic_value.setText(str(round(mic1,3)))

    if sire.model2_checkbutton.isChecked():
        T2 = class_object["class_object"].model2[1,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        G2 = class_object["class_object"].model2[6,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        B2 = class_object["class_object"].model2[4,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        A2 = class_object["class_object"].model2[7,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        V2 = class_object["class_object"].model2[5,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]/(100*1000)
        mic2 = class_object["class_object"].model2[3,class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
        if sire.mac2_checkbutton.isChecked():
            mac2 = class_object["class_object"].mac2[0, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)]
            sire.mod2_mac_value.setText(str(round(mac2,3)))
        sire.mod2_ff_value.setText(str(round(1-ff1,3)))
        sire.mod2_T_value.setText(str(round(T2,3)))
        sire.mod2_B_value.setText(str(round(B2,3)))
        sire.mod2_V_value.setText(str(round(V2,3)))
        sire.mod2_G_value.setText(str(round(G2,3)))
        sire.mod2_A_value.setText(str(round(A2,3)))
        sire.mod2_mic_value.setText(str(round(mic2,3)))

    Z = round(class_object["class_object"].model1[8, class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)], 3)
    OD = round(class_object["class_object"].model1[0, class_object["class_object"].current_optical_depth_index, int(class_object["class_object"].current_y), int(class_object["class_object"].current_x)], 3)
    sire.pixel_values.setText("Z: %s [cm] OD: %s" %(str(Z), str(OD)))
    sire.x_spinbox.blockSignals(True)
    sire.y_spinbox.blockSignals(True)
    sire.x_spinbox.setValue(int(class_object["class_object"].current_x))
    sire.y_spinbox.setValue(int(class_object["class_object"].current_y))
    sire.x_spinbox.blockSignals(False)
    sire.y_spinbox.blockSignals(False)

def set_font_sizes(self,sire):
    try:
        sire.fontsize_titles = int(self.fontsize_titles_map_entry.text())
        sire.fontsize_axislabels = int(self.fontsize_axislabels_map_entry.text())
        sire.fontsize_ticklabels = int(self.fontsize_ticklabels_map_entry.text())
    except ValueError:
        msg = QMessageBox()
        msg.setText("Value error. You must enter an integer as the font size.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        self.fontsize_titles_map_entry.setText(str(sire.fontsize_titles))
        self.fontsize_axislabels_map_entry.setText(str(sire.fontsize_axislabels))
        self.fontsize_ticklabels_map_entry.setText(str(sire.fontsize_ticklabels))
