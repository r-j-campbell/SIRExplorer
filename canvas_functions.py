import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import astropy.io.fits as pyfits
import matplotlib
matplotlib.use("TkAgg")

def show(self, class_object):
    # print("self.increment", self.increment)  # zero on first launch, always one thereafter
    # print("self.frame_flag", self.frame_flag)  # zero when dataset has 1 frame, one otherwise
    # print("self.flag", self.flag)  # false when dataset has no match in dict, true when match found
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
    self.wl_scale.setMinimum(0)
    self.wl_scale.setMaximum(class_object["class_object"].Attributes["wl"] - 1)
    self.optical_depth_scale.setMinimum(0)
    self.optical_depth_scale.setMaximum(class_object["class_object"].Attributes["optical_depth"] - 1)
    self.wl_max = obs_prof.shape[1]
    self.wl_dim = obs_prof.shape[1]
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
    if self.chi2_checkbutton.isChecked():
        chi2 = pyfits.open(class_object["chi2_file"])[0].data
        chi2 = np.squeeze(chi2)
        if chi2.ndim == 3:  # executed only if there are multiple frames of data
            chi2 = chi2[class_object["class_object"].current_frame_index, :, :]
        class_object["class_object"].update_chi2(chi2)

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
    # print(model1.shape)
    # print(model2.shape)
    # print(obs_prof.shape)
    # print(syn_prof.shape)
    # print(binary_map.shape)
    # print(mac1_file.shape)
    # print(mac2_file.shape)

    if self.Stokes_checkbutton.isChecked():
        if self.I_CT[3] == 0:
            I_map = self.sc1.ax1.imshow(obs_prof[0, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.I_CT[0], vmin=self.I_CT[1], vmax=self.I_CT[2])
        elif self.I_CT[3] == 1:
            I_map = self.sc1.ax1.imshow(obs_prof[0, class_object["class_object"].current_wl_index, :, :], origin='lower',
                    cmap=self.I_CT[0])
        dividerI = make_axes_locatable(self.sc1.ax1)
        self.caxI = dividerI.append_axes("right", size="3%", pad=0)
        self.cbar_I = self.sc1.fig1.colorbar(I_map, cax=self.caxI, pad=0)
        self.cbar_I.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.T_checkbutton.isChecked():
        if self.T_CT[3] == 0:
            T_map = self.sc1.ax2.imshow(model1[1, class_object["class_object"].current_optical_depth_index, :, :],
                    origin='lower', cmap=self.T_CT[0], vmin=self.T_CT[1], vmax=self.T_CT[2])
        elif self.T_CT[3] == 1:
            T_map = self.sc1.ax2.imshow(model1[1, class_object["class_object"].current_optical_depth_index, :, :],
                    origin='lower', cmap=self.T_CT[0])
        dividerT = make_axes_locatable(self.sc1.ax2)
        self.caxT = dividerT.append_axes("right", size="3%", pad=0)
        self.cbar_T = self.sc1.fig1.colorbar(T_map, cax=self.caxT, pad=0)
        self.cbar_T.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.B_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.B_CT[3] == 0:
                B_map = self.sc1.ax3.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', vmin=self.B_CT[1], vmax=self.B_CT[2], cmap=self.B_CT[0])
            elif self.B_CT[3] == 1:
                B_map = self.sc1.ax3.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', cmap=self.B_CT[0])
        else:
            if self.B_CT[3] == 0:
                B_map = self.sc1.ax3.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.B_CT[1], vmax=self.B_CT[2], cmap=self.B_CT[0])
            elif self.B_CT[3] == 1:
                B_map = self.sc1.ax3.imshow(
                    model1[4, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.B_CT[0])
        dividerB = make_axes_locatable(self.sc1.ax3)
        self.caxB = dividerB.append_axes("right", size="3%", pad=0)
        self.cbar_B = self.sc1.fig1.colorbar(B_map, cax=self.caxB, pad=0)
        self.cbar_B.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.V_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            combined_V = np.empty([class_object["class_object"].Attributes["y"], class_object["class_object"].Attributes["x"]]) * np.nan
            combined_V = (model2[5, class_object["class_object"].current_optical_depth_index, :, :] * mac2_file[1, :, :]) + (model1[5, class_object["class_object"].current_optical_depth_index, :, :] * mac1_file[1, :, :])
            if self.V_CT[3] == 0:
                V_map = self.sc1.ax4.imshow((combined_V / (100 * 1000)), origin='lower', cmap=self.V_CT[0], vmin=self.V_CT[1], vmax=self.V_CT[2])
            elif self.V_CT[3] == 1:
                V_map = self.sc1.ax4.imshow((combined_V / (100 * 1000)), origin='lower', cmap=self.V_CT[0])
        else:
            if self.V_CT[3] == 0:
                V_map = self.sc1.ax4.imshow(
                    (model1[5, class_object["class_object"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=self.V_CT[0], vmin=self.V_CT[1], vmax=self.V_CT[2])
            elif self.V_CT[3] == 1:
                V_map = self.sc1.ax4.imshow(
                    (model1[5, class_object["class_object"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=self.V_CT[0])
        dividerV = make_axes_locatable(self.sc1.ax4)
        self.caxV = dividerV.append_axes("right", size="3%", pad=0)
        self.cbar_V = self.sc1.fig1.colorbar(V_map, cax=self.caxV, pad=0)
        self.cbar_V.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.G_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.G_CT[3] == 0:
                G_map = self.sc1.ax5.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.G_CT[1], vmax=self.G_CT[2], cmap=self.G_CT[0])
            elif self.G_CT[3] == 1:
                G_map = self.sc1.ax5.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.G_CT[0])
        else:
            if self.G_CT[3] == 0:
                G_map = self.sc1.ax5.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=self.G_CT[1], vmax=self.G_CT[2], cmap=self.G_CT[0])
            if self.G_CT[3] == 1:
                G_map = self.sc1.ax5.imshow(
                    model1[6, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.G_CT[0])
        dividerG = make_axes_locatable(self.sc1.ax5)
        self.caxG = dividerG.append_axes("right", size="3%", pad=0)
        self.cbar_G = self.sc1.fig1.colorbar(G_map, cax=self.caxG, pad=0)
        self.cbar_G.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.A_checkbutton.isChecked():
        if self.model2_checkbutton.isChecked():
            if self.A_CT[3] == 0:
                A_map = self.sc1.ax6.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0], vmin=self.A_CT[1], vmax=self.A_CT[2])
            elif self.A_CT[3] == 1:
                A_map = self.sc1.ax6.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0])
        else:
            if self.A_CT[3] == 0:
                A_map = self.sc1.ax6.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0], vmin=self.A_CT[1], vmax=self.A_CT[2])
            elif self.A_CT[3] == 1:
                A_map = self.sc1.ax6.imshow(
                    model1[7, class_object["class_object"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=self.A_CT[0])
        dividerA = make_axes_locatable(self.sc1.ax6)
        self.caxA = dividerA.append_axes("right", size="3%", pad=0)
        self.cbar_A = self.sc1.fig1.colorbar(A_map, cax=self.caxA, pad=0)
        self.cbar_A.ax.tick_params(labelsize=self.fontsize_axislabels)

    current_x = class_object["class_object"].current_x
    current_y = class_object["class_object"].current_y
    #if self.click_increment == 1:
    self.sc1.ax1.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax1.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax2.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax2.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax3.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax3.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax4.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax4.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax5.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax5.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax6.axvline(current_x, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax6.axhline(current_y, color='red', linestyle=':', linewidth=self.linewidth)
    self.sc1.ax1.set_title("Stokes $I$ [$I_c$]", fontsize=self.fontsize_titles)
    self.sc1.ax2.set_title("T [K]", fontsize=self.fontsize_titles)
    self.sc1.ax5.set_title("$\\gamma$ [deg.]", fontsize=self.fontsize_titles)
    self.sc1.ax4.set_title("$v_\mathrm{{LOS}}$ [km/s]", fontsize=self.fontsize_titles)
    if self.model2_checkbutton.isChecked():
        self.sc1.ax3.set_title("$\\alpha$ B [G]", fontsize=self.fontsize_titles)
    else:
        self.sc1.ax3.set_title("B [G]", fontsize=self.fontsize_titles)
    self.sc1.ax6.set_title("$\\phi$ [deg.]", fontsize=self.fontsize_titles)
    self.sc1.ax4.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
    self.sc1.ax3.set_xlabel("X [pix.]", fontsize=self.fontsize_axislabels)
    self.sc1.ax1.set_ylabel("X [pix.]", fontsize=self.fontsize_axislabels)
    self.sc1.ax5.set_ylabel("X [pix.]", fontsize=self.fontsize_axislabels)
    self.sc1.ax4.set_ylabel("X [pix.]", fontsize=self.fontsize_axislabels)

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
    if self.model2_checkbutton.isChecked():
        model2 = class_object["class_object"].model2
        mac1 = class_object["class_object"].mac1
        mac2 = class_object["class_object"].mac2

    # Stokes plots
    self.sc2.ax1.plot(obs_prof[0, :, int(current_y), int(current_x)], label='Observed profile', linewidth=self.linewidth)
    self.sc2.ax1.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax1.plot(syn_prof[0, :, int(current_y), int(current_x)], label='Synthetic profile', linewidth=self.linewidth)
    self.sc2.ax1.legend(frameon=False, fontsize=self.fontsize_axislabels)
    self.sc2.ax1.set_xlim(self.wl_min, self.wl_max)
    self.sc2.ax2.plot(obs_prof[1, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax2.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax2.plot(syn_prof[1, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax2.set_xlim(self.wl_min, self.wl_max)
    self.sc2.ax3.plot(obs_prof[2, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax3.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax3.plot(syn_prof[2, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax3.set_xlim(self.wl_min, self.wl_max)
    self.sc2.ax4.plot(obs_prof[3, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax4.axvline(class_object["class_object"].current_wl_index, linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc2.ax4.plot(syn_prof[3, :, int(current_y), int(current_x)], linewidth=self.linewidth)
    self.sc2.ax4.set_xlim(self.wl_min, self.wl_max)

    # Model parameter plots
    self.sc3.ax1.plot(model1[0, :, int(current_y), int(current_x)], model1[1, :, int(current_y), int(current_x)], label="mod 1",
        linestyle='solid',color='red', linewidth=self.linewidth)
    self.sc3.ax1.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax2.plot(model1[0, :, int(current_y), int(current_x)], model1[4, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=self.linewidth)
    self.sc3.ax2.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax3.plot(model1[0, :, int(current_y), int(current_x)], model1[5, :, int(current_y), int(current_x)] / (100 * 1000),
        linestyle='solid', color='red', linewidth=self.linewidth)
    self.sc3.ax3.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[6, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=self.linewidth)  # inclination
    self.sc3.ax4.axvline(model1[0, class_object["class_object"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=self.linewidth)
    self.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[7, :, int(current_y), int(current_x)],
        linestyle=':', color='red', linewidth=self.linewidth)  # azimuth

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
        del model2, mac1, mac2

    self.sc2.fig2.canvas.draw()
    self.sc3.fig3.canvas.draw()

    del model1, obs_prof, syn_prof

def create_figure1(self):
    index=1
    total=0
    if self.Stokes_checkbutton.isChecked():
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

    if self.Stokes_checkbutton.isChecked():
        self.sc1.ax1 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1
    if self.T_checkbutton.isChecked():
        self.sc1.ax2 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1
    if self.B_checkbutton.isChecked():
        self.sc1.ax3 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1
    if self.V_checkbutton.isChecked():
        self.sc1.ax4 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1
    if self.G_checkbutton.isChecked():
        self.sc1.ax5 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1
    if self.A_checkbutton.isChecked():
        self.sc1.ax6 = self.sc1.fig1.add_subplot(total,1,index)
        index+=1

def clear_fig1(self):
    self.sc1.fig1.clf()
    create_figure1(self)
    self.flag=False
    self.get_all_values(self.class_objects,0,self.select_model1.currentText())
    if self.flag == True:
        i=str(self.match)
        if self.click_increment == 1:
            #click(self,self.class_objects[i])
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
        index+=1
    if self.pQ_checkbutton.isChecked():
        self.sc2.ax2 = self.sc2.fig2.add_subplot(total,1,index)
        index+=1
    if self.pU_checkbutton.isChecked():
        self.sc2.ax3 = self.sc2.fig2.add_subplot(total,1,index)
        index+=1
    if self.pV_checkbutton.isChecked():
        self.sc2.ax4 = self.sc2.fig2.add_subplot(total,1,index)
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
            #self.change_canvas()
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
        index+=1
    if self.mB_checkbutton.isChecked():
        self.sc3.ax2 = self.sc3.fig3.add_subplot(columns,rows,index)
        index+=1
    if self.mV_checkbutton.isChecked():
        self.sc3.ax3 = self.sc3.fig3.add_subplot(columns,rows,index)
        index+=1
    if self.mG_checkbutton.isChecked():
        self.sc3.ax4 = self.sc3.fig3.add_subplot(columns,rows,index)
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
            #self.change_canvas()
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")

def remove_cbars(self):
    try:
        self.caxI.remove()
    except:
        pass
    try:
        self.caxT.remove()
    except:
        print("Something went wrong")
    try:
        self.caxB.remove()
    except:
        print("Something went wrong")
    try:
        self.caxV.remove()
    except:
        print("Something went wrong")

    try:
        self.caxG.remove()
    except:
        print("Something went wrong")
    else:
        print("Nothing went wrong")
    try:
        self.caxA.remove()
    except:
        print("Something went wrong")
    else:
        print("Nothing went wrong")

def change_frame(self):
    frame = int(self.frame_scale.value())
    self.flag = False
    self.get_all_values(self.class_objects, 0, self.select_model1.currentText())
    if self.flag == True:
        i = str(self.match)
        self.class_objects[i]['class_object'].current_frame_index = int(frame)
        self.change_canvas()
        click(self, self.class_objects[i])
    elif self.flag == False:
        print("ERROR: dataset not found")

def change_wl(self):
    wl = int(self.wl_scale.value())
    self.flag = False
    self.get_all_values(self.class_objects, 0, self.select_model1.currentText())
    if self.flag == True:
        i = str(self.match)
        self.class_objects[i]['class_object'].current_wl_index = int(wl)
        self.change_canvas()
        click(self, self.class_objects[i])
    elif self.flag == False:
        print("ERROR: dataset not found")

def change_optical_depth(self):
    self.flag = False
    self.get_all_values(self.class_objects, 0, self.select_model1.currentText())
    print(self.flag)
    if self.flag == True:
        i = str(self.match)
        optical_depth = int(self.optical_depth_scale.value())
        self.class_objects[i]['class_object'].current_optical_depth_index = int(optical_depth)
        self.change_canvas()
        click(self, self.class_objects[i])
    elif self.flag == False:
        print("ERROR: dataset not found")
