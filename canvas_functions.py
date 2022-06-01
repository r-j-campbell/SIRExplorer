import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import astropy.io.fits as pyfits
import matplotlib
matplotlib.use("TkAgg")
matplotlib.rc('image',interpolation='none',origin='lower')
from PyQt5.QtWidgets import QMessageBox


def show(sire, sir):
    if sire.increment == 0:
        create_figure1(sire)
        create_figure2(sire)
        create_figure3(sire)
    if sire.increment == 1:
        clear_maps_and_remove_cbars(sire)
    if sire.flag == False or sire.frame_changed_flag == 1:
        open_files(sire,sir)
    update_canvas(sire,sir)
    sire.sc1.fig1.canvas.draw()


def open_files(sire,sir):
    model1 = pyfits.open(sir["model_file"])[0].data
    obs_prof = pyfits.open(sir["obs_prof_file"])[0].data
    syn_prof = pyfits.open(sir["syn_prof_file"])[0].data
    model1 = np.squeeze(model1)
    obs_prof = np.squeeze(obs_prof)
    if model1.ndim == 5:  # executed only if there are multiple frames of data
        sir["sir"].Attributes["t"] = model1.shape[0]
        model1 = model1[sir["sir"].current_frame_index, :, :, :, :]
        obs_prof = obs_prof[sir["sir"].current_frame_index, :, :, :, :]
        syn_prof = syn_prof[sir["sir"].current_frame_index, :, :, :, :]
        if sire.flag == False:
            sire.frame_scale.setMinimum(0)
            sire.frame_scale.setMaximum(sir['sir'].Attributes["t"] - 1)
    sir["sir"].Attributes["optical_depth"] = model1.shape[1]
    sir["sir"].Attributes["y"] = model1.shape[2]
    sir["sir"].Attributes["x"] = model1.shape[3]
    sir["sir"].Attributes["wl"] = obs_prof.shape[1]
    sir["sir"].update_model1(model1)
    sir["sir"].update_obs(obs_prof)
    sir["sir"].update_syn(syn_prof)

    if sire.flag == False:
        sir["sir"].x_min = 0
        sir["sir"].x_max = sir["sir"].Attributes["x"] - 1
        sir["sir"].y_min = 0
        sir["sir"].y_max = sir["sir"].Attributes["y"] - 1
        sire.x_min_entry.setEnabled(True)
        sire.x_min_entry.setText(str(0))
        sire.x_max_entry.setEnabled(True)
        sire.x_max_entry.setText(str(sir["sir"].Attributes["x"] - 1))
        sire.y_min_entry.setEnabled(True)
        sire.y_min_entry.setText(str(0))
        sire.y_max_entry.setEnabled(True)
        sire.y_max_entry.setText(str(sir["sir"].Attributes["y"] - 1))

        sire.wl_scale.setMinimum(0)
        sire.wl_scale.setMaximum(sir["sir"].Attributes["wl"] - 1)
        sir["sir"].wl_min = 0
        sir["sir"].wl_max = sir["sir"].Attributes["wl"] - 1
        sire.wl_min_entry.setEnabled(True)
        sire.wl_min_entry.setText(str(0))
        sire.wl_max_entry.setEnabled(True)
        sire.wl_max_entry.setText(str(sir["sir"].Attributes["wl"] - 1))

        sire.optical_depth_scale.setMinimum(0)
        sire.optical_depth_scale.setMaximum(sir["sir"].Attributes["optical_depth"] - 1)
        sir["sir"].optical_depth_min = 0
        sir["sir"].optical_depth_max = sir["sir"].Attributes["optical_depth"] - 1
        sire.optical_depth_min_entry.setEnabled(True)
        sire.optical_depth_min_entry.setText(str(0))
        sire.optical_depth_max_entry.setEnabled(True)
        sire.optical_depth_max_entry.setText(str(sir["sir"].Attributes["optical_depth"] - 1))

    if sire.binary_checkbutton.isChecked():
        binary_map = pyfits.open(sir["binary_file"])[0].data
        binary_map = np.squeeze(binary_map)
        if binary_map.ndim == 3:  # executed only if there are multiple frames of data
            binary_map = binary_map[sir["sir"].current_frame_index, :, :]
        sir["sir"].update_binary(binary_map)
    else:
        binary_map = np.ones([sir["sir"].Attributes["y"], sir["sir"].Attributes["x"]])
        sir["sir"].update_binary(binary_map)

    if sire.model2_checkbutton.isChecked() and sire.mac1_checkbutton.isChecked() and sire.mac2_checkbutton.isChecked():
        model2 = pyfits.open(sir["secondary_model_file"])[0].data
        mac1_file = pyfits.open(sir["mac1_file"])[0].data
        mac2_file = pyfits.open(sir["mac2_file"])[0].data
        mac1_file = np.squeeze(mac1_file)
        model2 = np.squeeze(model2)
        mac2_file = np.squeeze(mac2_file)
        if model2.ndim == 5:  # executed only if there are multiple frames of data
            model2 = model2[sir["sir"].current_frame_index, :, :, :, :]
            mac1_file = mac1_file[sir["sir"].current_frame_index, :, :, :]
            mac2_file = mac2_file[sir["sir"].current_frame_index, :, :, :]
        sir["sir"].update_model2(model2)
        sir["sir"].update_mac1(mac1_file)
        sir["sir"].update_mac2(mac2_file)
    elif sire.model2_checkbutton.isChecked() == False and sire.mac1_checkbutton.isChecked():
        mac1_file = pyfits.open(sir["mac1_file"])[0].data
        mac1_file = np.squeeze(mac1_file)
        if mac1_file.ndim == 4:  # executed only if there are multiple frames of data
            mac1_file = mac1_file[sir["sir"].current_frame_index, :, :, :]
        sir["sir"].updatemac1(mac1_file)
    elif sire.model2_checkbutton.isChecked() and sire.mac1_checkbutton.isChecked() and sire.mac2_checkbutton.isChecked() == False:
        model2 = pyfits.open(sir["secondary_model_file"])[0].data
        model2 = np.squeeze(model2)
        mac1_file = pyfits.open(sir["mac1_file"])[0].data
        mac1_file = np.squeeze(mac1_file)
        if model2.ndim == 5:  # executed only if there are multiple frames of data
            mac1_file = mac1_file[sir["sir"].current_frame_index, :, :, :]
            model2 = model2[sir["sir"].current_frame_index, :, :, :, :]
        sir["sir"].update_model2(model2)
        sir["sir"].update_mac1(mac1_file)
        mac2_file = np.empty((3, model1.shape[2], model1.shape[3]))  # create dummy mac2 file
        mac2_file[1, :, :] = np.subtract(np.ones((model1.shape[2], model1.shape[3])), mac1_file[1, :, :])  # update dummy mac2 file filling factor as (1 - mac1) when mac2 not provided"
        sir["sir"].update_mac2(mac2_file)


def update_canvas(sire,sir):
    model1 = sir["sir"].model1
    model2 = sir["sir"].model2
    obs_prof = sir["sir"].obs
    binary_map = sir["sir"].binary
    mac1_file = sir["sir"].mac1
    mac2_file = sir["sir"].mac2
    current_x = int(sir["sir"].current_x)
    current_y = int(sir["sir"].current_y)
    if sire.Stokes_checkbutton.isChecked():
        if sire.StkI_CT[3] == 0:
            StkI_map = sire.sc1.ax1.imshow(obs_prof[0, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkI_CT[0], vmin=sire.StkI_CT[1], vmax=sire.StkI_CT[2])
        elif sire.StkI_CT[3] == 1:
            StkI_map = sire.sc1.ax1.imshow(obs_prof[0, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkI_CT[0])
        dividerStkI = make_axes_locatable(sire.sc1.ax1)
        sire.caxStkI = dividerStkI.append_axes("right", size="3%", pad=0)
        sire.cbar_StkI = sire.sc1.fig1.colorbar(StkI_map, cax=sire.caxStkI, pad=0)
        sire.cbar_StkI.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax1.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax1.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax1.set_title("Stokes $I$ [$I_c$]", fontsize=sire.fontsize_titles)
        sire.sc1.ax1.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax1.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax1.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax1.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.Stokes_Q_checkbutton.isChecked():
        if sire.StkQ_CT[3] == 0:
            StkQ_map = sire.sc1.ax2.imshow(obs_prof[1, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkQ_CT[0], vmin=sire.StkQ_CT[1], vmax=sire.StkQ_CT[2])
        elif sire.StkQ_CT[3] == 1:
            StkQ_map = sire.sc1.ax2.imshow(obs_prof[1, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkQ_CT[0])
        dividerStkQ = make_axes_locatable(sire.sc1.ax2)
        sire.caxStkQ = dividerStkQ.append_axes("right", size="3%", pad=0)
        sire.cbar_StkQ = sire.sc1.fig1.colorbar(StkQ_map, cax=sire.caxStkQ, pad=0)
        sire.cbar_StkQ.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax2.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax2.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax2.set_title("Stokes $Q$ [$I_c$]", fontsize=sire.fontsize_titles)
        sire.sc1.ax2.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax2.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax2.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax2.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.Stokes_U_checkbutton.isChecked():
        if sire.StkU_CT[3] == 0:
            StkU_map = sire.sc1.ax3.imshow(obs_prof[2, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkU_CT[0], vmin=sire.StkU_CT[1], vmax=sire.StkU_CT[2])
        elif sire.StkU_CT[3] == 1:
            StkU_map = sire.sc1.ax3.imshow(obs_prof[2, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkU_CT[0])
        dividerStkU = make_axes_locatable(sire.sc1.ax3)
        sire.caxStkU = dividerStkU.append_axes("right", size="3%", pad=0)
        sire.cbar_StkU = sire.sc1.fig1.colorbar(StkU_map, cax=sire.caxStkU, pad=0)
        sire.cbar_StkU.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax3.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax3.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax3.set_title("Stokes $U$ [$I_c$]", fontsize=sire.fontsize_titles)
        sire.sc1.ax3.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax3.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax3.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax3.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.Stokes_V_checkbutton.isChecked():
        if sire.StkV_CT[3] == 0:
            StkV_map = sire.sc1.ax4.imshow(obs_prof[3, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkV_CT[0], vmin=sire.StkV_CT[1], vmax=sire.StkV_CT[2])
        elif sire.StkV_CT[3] == 1:
            StkV_map = sire.sc1.ax4.imshow(obs_prof[3, sir["sir"].current_wl_index, :, :], origin='lower',
                    cmap=sire.StkV_CT[0])
        dividerStkV = make_axes_locatable(sire.sc1.ax4)
        sire.caxStkV = dividerStkV.append_axes("right", size="3%", pad=0)
        sire.cbar_StkV = sire.sc1.fig1.colorbar(StkV_map, cax=sire.caxStkV, pad=0)
        sire.cbar_StkV.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax4.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax4.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax4.set_title("Stokes $V$ [$I_c$]", fontsize=sire.fontsize_titles)
        sire.sc1.ax4.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax4.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax4.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax4.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.T_checkbutton.isChecked():
        if sire.T_CT[3] == 0:
            T_map = sire.sc1.ax5.imshow(model1[1, sir["sir"].current_optical_depth_index, :, :],
                    origin='lower', cmap=sire.T_CT[0], vmin=sire.T_CT[1], vmax=sire.T_CT[2])
        elif sire.T_CT[3] == 1:
            T_map = sire.sc1.ax5.imshow(model1[1, sir["sir"].current_optical_depth_index, :, :],
                    origin='lower', cmap=sire.T_CT[0])
        dividerT = make_axes_locatable(sire.sc1.ax5)
        sire.caxT = dividerT.append_axes("right", size="3%", pad=0)
        sire.cbar_T = sire.sc1.fig1.colorbar(T_map, cax=sire.caxT, pad=0)
        sire.cbar_T.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax5.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax5.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax5.set_title("T [K]", fontsize=sire.fontsize_titles)
        sire.sc1.ax5.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax5.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax5.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax5.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.B_checkbutton.isChecked():
        if sire.model2_checkbutton.isChecked():
            if sire.B_CT[3] == 0:
                B_map = sire.sc1.ax6.imshow(
                    model1[4, sir["sir"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', vmin=sire.B_CT[1], vmax=sire.B_CT[2], cmap=sire.B_CT[0])
            elif sire.B_CT[3] == 1:
                B_map = sire.sc1.ax6.imshow(
                    model1[4, sir["sir"].current_optical_depth_index, :, :] * mac1_file[1, :, :] * binary_map,
                    origin='lower', cmap=sire.B_CT[0], interpolation='none')
            sire.sc1.ax6.set_title("$\\alpha$ B [G]", fontsize=sire.fontsize_titles)
        else:
            if sire.B_CT[3] == 0:
                B_map = sire.sc1.ax6.imshow(
                    model1[4, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=sire.B_CT[1], vmax=sire.B_CT[2], cmap=sire.B_CT[0])
            elif sire.B_CT[3] == 1:
                B_map = sire.sc1.ax6.imshow(
                    model1[4, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.B_CT[0], interpolation='none')
            sire.sc1.ax6.set_title("B [G]", fontsize=sire.fontsize_titles)
        dividerB = make_axes_locatable(sire.sc1.ax6)
        sire.caxB = dividerB.append_axes("right", size="3%", pad=0)
        sire.cbar_B = sire.sc1.fig1.colorbar(B_map, cax=sire.caxB, pad=0)
        sire.cbar_B.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax6.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax6.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax6.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax6.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax6.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax6.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.V_checkbutton.isChecked():
        if sire.model2_checkbutton.isChecked():
            combined_V = np.empty([sir["sir"].Attributes["y"], sir["sir"].Attributes["x"]]) * np.nan
            combined_V = (model2[5, sir["sir"].current_optical_depth_index, :, :] * mac2_file[1, :, :]) + (model1[5, sir["sir"].current_optical_depth_index, :, :] * mac1_file[1, :, :])
            if sire.V_CT[3] == 0:
                V_map = sire.sc1.ax7.imshow((combined_V / (100 * 1000)), origin='lower', cmap=sire.V_CT[0], vmin=sire.V_CT[1], vmax=sire.V_CT[2])
            elif sire.V_CT[3] == 1:
                V_map = sire.sc1.ax7.imshow((combined_V / (100 * 1000)), origin='lower', cmap=sire.V_CT[0])
        else:
            if sire.V_CT[3] == 0:
                V_map = sire.sc1.ax7.imshow(
                    (model1[5, sir["sir"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=sire.V_CT[0], vmin=sire.V_CT[1], vmax=sire.V_CT[2])
            elif sire.V_CT[3] == 1:
                V_map = sire.sc1.ax7.imshow(
                    (model1[5, sir["sir"].current_optical_depth_index, :, :] / (100 * 1000)),
                    origin='lower', cmap=sire.V_CT[0])
        dividerV = make_axes_locatable(sire.sc1.ax7)
        sire.caxV = dividerV.append_axes("right", size="3%", pad=0)
        sire.cbar_V = sire.sc1.fig1.colorbar(V_map, cax=sire.caxV, pad=0)
        sire.cbar_V.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax7.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax7.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax7.set_title("$v_\mathrm{{LOS}}$ [km/s]", fontsize=sire.fontsize_titles)
        sire.sc1.ax7.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax7.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax7.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax7.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.G_checkbutton.isChecked():
        if sire.model2_checkbutton.isChecked():
            if sire.G_CT[3] == 0:
                G_map = sire.sc1.ax8.imshow(
                    model1[6, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=sire.G_CT[1], vmax=sire.G_CT[2], cmap=sire.G_CT[0])
            elif sire.G_CT[3] == 1:
                G_map = sire.sc1.ax8.imshow(
                    model1[6, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.G_CT[0])
        else:
            if sire.G_CT[3] == 0:
                G_map = sire.sc1.ax8.imshow(
                    model1[6, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    vmin=sire.G_CT[1], vmax=sire.G_CT[2], cmap=sire.G_CT[0])
            if sire.G_CT[3] == 1:
                G_map = sire.sc1.ax8.imshow(
                    model1[6, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.G_CT[0])
        dividerG = make_axes_locatable(sire.sc1.ax8)
        sire.caxG = dividerG.append_axes("right", size="3%", pad=0)
        sire.cbar_G = sire.sc1.fig1.colorbar(G_map, cax=sire.caxG, pad=0)
        sire.cbar_G.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax8.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax8.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax8.set_title("$\\gamma$ [deg.]", fontsize=sire.fontsize_titles)
        sire.sc1.ax8.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax8.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax8.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax8.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    if sire.A_checkbutton.isChecked():
        if sire.model2_checkbutton.isChecked():
            if sire.A_CT[3] == 0:
                A_map = sire.sc1.ax9.imshow(
                    model1[7, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.A_CT[0], vmin=sire.A_CT[1], vmax=sire.A_CT[2])
            elif sire.A_CT[3] == 1:
                A_map = sire.sc1.ax9.imshow(
                    model1[7, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.A_CT[0])
        else:
            if sire.A_CT[3] == 0:
                A_map = sire.sc1.ax9.imshow(
                    model1[7, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.A_CT[0], vmin=sire.A_CT[1], vmax=sire.A_CT[2])
            elif sire.A_CT[3] == 1:
                A_map = sire.sc1.ax9.imshow(
                    model1[7, sir["sir"].current_optical_depth_index, :, :] * binary_map, origin='lower',
                    cmap=sire.A_CT[0])
        dividerA = make_axes_locatable(sire.sc1.ax9)
        sire.caxA = dividerA.append_axes("right", size="3%", pad=0)
        sire.cbar_A = sire.sc1.fig1.colorbar(A_map, cax=sire.caxA, pad=0)
        sire.cbar_A.ax.tick_params(labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax9.axvline(current_x, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax9.axhline(current_y, color='red', linestyle=':', linewidth=sire.line_widths)
        sire.sc1.ax9.set_title("$\\phi$ [deg.]", fontsize=sire.fontsize_titles)
        sire.sc1.ax9.set_xlabel("X [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax9.set_ylabel("Y [pix.]", fontsize=sire.fontsize_axislabels)
        sire.sc1.ax9.set_xlim(sir["sir"].x_min, sir["sir"].x_max)
        sire.sc1.ax9.set_ylim(sir["sir"].y_min, sir["sir"].y_max)

    del model1, model2, obs_prof, binary_map, mac1_file, mac2_file


def click(sire, sir):
    current_x = sir["sir"].current_x
    current_y = sir["sir"].current_y
    model1 = sir["sir"].model1
    obs_prof = sir["sir"].obs
    syn_prof = sir["sir"].syn

    if sire.click_increment == 1:
        sire.sc2.ax1.clear()
        sire.sc2.ax2.clear()
        sire.sc2.ax3.clear()
        sire.sc2.ax4.clear()
        sire.sc3.ax1.clear()
        sire.sc3.ax2.clear()
        sire.sc3.ax3.clear()
        sire.sc3.ax4.clear()

    # Stokes plots
    sire.sc2.ax1.plot(obs_prof[0, :, int(current_y), int(current_x)], label='Obs', linewidth=sire.line_widths)
    sire.sc2.ax1.axvline(sir["sir"].current_wl_index, linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc2.ax1.plot(syn_prof[0, :, int(current_y), int(current_x)], label='Syn', linewidth=sire.line_widths)
    sire.sc2.ax1.legend(frameon=False, fontsize=sire.fontsize_axislabels)
    sire.sc2.ax1.set_xlim(sir["sir"].wl_min, sir["sir"].wl_max)
    sire.sc2.ax2.plot(obs_prof[1, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax2.axvline(sir["sir"].current_wl_index, linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc2.ax2.plot(syn_prof[1, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax2.set_xlim(sir["sir"].wl_min, sir["sir"].wl_max)
    sire.sc2.ax3.plot(obs_prof[2, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax3.axvline(sir["sir"].current_wl_index, linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc2.ax3.plot(syn_prof[2, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax3.set_xlim(sir["sir"].wl_min, sir["sir"].wl_max)
    sire.sc2.ax4.plot(obs_prof[3, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax4.axvline(sir["sir"].current_wl_index, linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc2.ax4.plot(syn_prof[3, :, int(current_y), int(current_x)], linewidth=sire.line_widths)
    sire.sc2.ax4.set_xlim(sir["sir"].wl_min, sir["sir"].wl_max)

    # Model parameter plots
    sire.sc3.ax1.plot(model1[0, :, int(current_y), int(current_x)], model1[1, :, int(current_y), int(current_x)], label="mod 1",
        linestyle='solid',color='red', linewidth=sire.line_widths)
    sire.sc3.ax1.axvline(model1[0, sir["sir"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc3.ax1.set_xlim(model1[0, sir["sir"].optical_depth_min, int(current_y), int(current_x)], model1[0, sir["sir"].optical_depth_max, int(current_y), int(current_x)])

    sire.sc3.ax2.plot(model1[0, :, int(current_y), int(current_x)], model1[4, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=sire.line_widths)
    sire.sc3.ax2.axvline(model1[0, sir["sir"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc3.ax2.set_xlim(model1[0, sir["sir"].optical_depth_min, int(current_y), int(current_x)], model1[0, sir["sir"].optical_depth_max, int(current_y), int(current_x)])

    sire.sc3.ax3.plot(model1[0, :, int(current_y), int(current_x)], model1[5, :, int(current_y), int(current_x)] / (100 * 1000),
        linestyle='solid', color='red', linewidth=sire.line_widths)
    sire.sc3.ax3.axvline(model1[0, sir["sir"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc3.ax3.set_xlim(model1[0, sir["sir"].optical_depth_min, int(current_y), int(current_x)], model1[0, sir["sir"].optical_depth_max, int(current_y), int(current_x)])

    sire.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[6, :, int(current_y), int(current_x)],
        linestyle='solid', color='red', linewidth=sire.line_widths)  # inclination
    sire.sc3.ax4.axvline(model1[0, sir["sir"].current_optical_depth_index, int(current_y), int(current_x)],
        linestyle=':', color='gray', linewidth=sire.line_widths)
    sire.sc3.ax4.plot(model1[0, :, int(current_y), int(current_x)], model1[7, :, int(current_y), int(current_x)],
        linestyle=':', color='red', linewidth=sire.line_widths)  # azimuth
    sire.sc3.ax4.set_xlim(model1[0, sir["sir"].optical_depth_min, int(current_y), int(current_x)], model1[0, sir["sir"].optical_depth_max, int(current_y), int(current_x)])

    if sire.model2_checkbutton.isChecked():
        model2 = sir["sir"].model2
        sire.sc3.ax1.plot(model2[0, :, int(current_y), int(current_x)], model2[1, :, int(current_y), int(current_x)],
            label="mod 2", linestyle='solid', color='blue', linewidth=sire.line_widths)
        sire.sc3.ax1.legend(frameon=False, fontsize=sire.fontsize_axislabels)
        sire.sc3.ax2.plot(model2[0, :, int(current_y), int(current_x)], model2[4, :, int(current_y), int(current_x)],
            linestyle='solid', color='blue', linewidth=sire.line_widths)
        sire.sc3.ax3.plot(model2[0, :, int(current_y), int(current_x)], model2[5, :, int(current_y), int(current_x)] / (100 * 1000),
            linestyle='solid', color='blue', linewidth=sire.line_widths)
        sire.sc3.ax4.plot(model2[0, :, int(current_y), int(current_x)], model2[6, :, int(current_y), int(current_x)],
            linestyle='solid', color='blue', linewidth=sire.line_widths)  # inclination
        sire.sc3.ax4.plot(model2[0, :, int(current_y), int(current_x)], model2[7, :, int(current_y), int(current_x)],
            linestyle=':', color='blue', linewidth=sire.line_widths)  # azimuth
        del model2

    sire.sc3.ax1.set_title("T [K]", fontsize=sire.fontsize_titles)
    sire.sc3.ax2.set_title("B [G]", fontsize=sire.fontsize_titles)
    sire.sc3.ax3.set_title("$v_\mathrm{{LOS}}$ [km/s]", fontsize=sire.fontsize_titles)
    sire.sc3.ax4.set_title("$\\gamma$ (solid), $\\phi$ (dashed) [deg.]", fontsize=sire.fontsize_titles)
    sire.sc3.ax1.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=sire.fontsize_axislabels)
    sire.sc3.ax2.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=sire.fontsize_axislabels)
    sire.sc3.ax3.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=sire.fontsize_axislabels)
    sire.sc3.ax4.set_xlabel("log($\\tau_{5000\\AA}$)", fontsize=sire.fontsize_axislabels)
    sire.sc2.ax1.set_title("Stokes $I$ [$I_c$]", fontsize=sire.fontsize_titles)
    sire.sc2.ax2.set_title("Stokes $Q$ [$I_c$]", fontsize=sire.fontsize_titles)
    sire.sc2.ax3.set_title("Stokes $U$ [$I_c$]", fontsize=sire.fontsize_titles)
    sire.sc2.ax4.set_title("Stokes $V$ [$I_c$]", fontsize=sire.fontsize_titles)
    sire.sc2.ax1.set_xlabel("wavelength [pix.]", fontsize=sire.fontsize_axislabels)
    sire.sc2.ax2.set_xlabel("wavelength [pix.]", fontsize=sire.fontsize_axislabels)
    sire.sc2.ax3.set_xlabel("wavelength [pix.]", fontsize=sire.fontsize_axislabels)
    sire.sc2.ax4.set_xlabel("wavelength [pix.]", fontsize=sire.fontsize_axislabels)

    sire.sc2.fig2.canvas.draw()
    sire.sc3.fig3.canvas.draw()

    del model1, obs_prof, syn_prof


def create_figure1(sire):
    index=1
    total=0
    if sire.Stokes_checkbutton.isChecked():
        total+=1
    if sire.Stokes_Q_checkbutton.isChecked():
        total+=1
    if sire.Stokes_U_checkbutton.isChecked():
        total+=1
    if sire.Stokes_V_checkbutton.isChecked():
        total+=1
    if sire.T_checkbutton.isChecked():
        total+=1
    if sire.B_checkbutton.isChecked():
        total+=1
    if sire.V_checkbutton.isChecked():
        total+=1
    if sire.G_checkbutton.isChecked():
        total+=1
    if sire.A_checkbutton.isChecked():
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
    if sire.Stokes_checkbutton.isChecked():
        sire.sc1.ax1 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax1.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.Stokes_Q_checkbutton.isChecked():
        sire.sc1.ax2 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax2.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.Stokes_U_checkbutton.isChecked():
        sire.sc1.ax3 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax3.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.Stokes_V_checkbutton.isChecked():
        sire.sc1.ax4 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax4.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.T_checkbutton.isChecked():
        sire.sc1.ax5 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax5.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.B_checkbutton.isChecked():
        sire.sc1.ax6 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax6.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.V_checkbutton.isChecked():
        sire.sc1.ax7 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax7.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.G_checkbutton.isChecked():
        sire.sc1.ax8 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax8.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax8.set_facecolor('xkcd:black')
        index+=1
    if sire.A_checkbutton.isChecked():
        sire.sc1.ax9 = sire.sc1.fig1.add_subplot(rows,columns,index)
        sire.sc1.ax9.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        sire.sc1.ax9.set_facecolor('xkcd:black')
        index+=1


def clear_fig1(sire):
    sire.sc1.fig1.clf()
    create_figure1(sire)
    sire.flag=False
    sire.get_all_values(sire.dataset_dict,0,sire.select_model1.currentText())
    if sire.flag == True:
        i=str(sire.match)
        if sire.click_increment == 1:
            sire.change_canvas()
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def create_figure2(sire):
    index=1
    total=0
    if sire.pI_checkbutton.isChecked():
        total+=1
    if sire.pQ_checkbutton.isChecked():
        total+=1
    if sire.pU_checkbutton.isChecked():
        total+=1
    if sire.pV_checkbutton.isChecked():
        total+=1

    if sire.pI_checkbutton.isChecked():
        sire.sc2.ax1 = sire.sc2.fig2.add_subplot(total,1,index)
        sire.sc2.ax1.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.pQ_checkbutton.isChecked():
        sire.sc2.ax2 = sire.sc2.fig2.add_subplot(total,1,index)
        sire.sc2.ax2.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.pU_checkbutton.isChecked():
        sire.sc2.ax3 = sire.sc2.fig2.add_subplot(total,1,index)
        sire.sc2.ax3.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.pV_checkbutton.isChecked():
        sire.sc2.ax4 = sire.sc2.fig2.add_subplot(total,1,index)
        sire.sc2.ax4.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1


def clear_fig2(sire):
    sire.sc2.fig2.clf()
    create_figure2(sire)
    sire.flag=False
    sire.get_all_values(sire.dataset_dict,0,sire.select_model1.currentText())
    if sire.flag == True:
        i=str(sire.match)
        if sire.click_increment == 1:
            click(sire,sire.dataset_dict[i])
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def create_figure3(sire):
    index=1
    total=0
    if sire.mT_checkbutton.isChecked():
        total+=1
    if sire.mB_checkbutton.isChecked():
        total+=1
    if sire.mV_checkbutton.isChecked():
        total+=1
    if sire.mG_checkbutton.isChecked():
        total+=1
    if total <= 2:
        rows = 1
        columns = total
    else:
        rows = 2
        columns = 2
    if sire.mT_checkbutton.isChecked():
        sire.sc3.ax1 = sire.sc3.fig3.add_subplot(columns,rows,index)
        sire.sc3.ax1.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.mB_checkbutton.isChecked():
        sire.sc3.ax2 = sire.sc3.fig3.add_subplot(columns,rows,index)
        sire.sc3.ax2.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.mV_checkbutton.isChecked():
        sire.sc3.ax3 = sire.sc3.fig3.add_subplot(columns,rows,index)
        sire.sc3.ax3.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1
    if sire.mG_checkbutton.isChecked():
        sire.sc3.ax4 = sire.sc3.fig3.add_subplot(columns,rows,index)
        sire.sc3.ax4.tick_params(axis='both', labelsize=sire.fontsize_ticklabels)
        index+=1


def clear_fig3(sire):
    sire.sc3.fig3.clf()
    create_figure3(sire)
    sire.flag=False
    sire.get_all_values(sire.dataset_dict,0,sire.select_model1.currentText())
    if sire.flag == True:
        i=str(sire.match)
        if sire.click_increment == 1:
            click(sire,sire.dataset_dict[i])
        else:
            print("you have to load something first")
    else:
        print("error!! dataset not found...")


def clear_maps_and_remove_cbars(sire):
    sire.sc1.ax1.clear()
    sire.sc1.ax2.clear()
    sire.sc1.ax3.clear()
    sire.sc1.ax4.clear()
    sire.sc1.ax5.clear()
    sire.sc1.ax6.clear()
    sire.sc1.ax7.clear()
    sire.sc1.ax8.clear()
    sire.sc1.ax9.clear()
    try:
        sire.caxStkI.remove()
    except:
        pass
    try:
        sire.caxStkQ.remove()
    except:
        pass
    try:
        sire.caxStkU.remove()
    except:
        pass
    try:
        sire.caxStkV.remove()
    except:
        pass
    try:
        sire.caxT.remove()
    except:
        pass
    try:
        sire.caxB.remove()
    except:
        pass
    try:
        sire.caxV.remove()
    except:
        pass
    try:
        sire.caxG.remove()
    except:
        pass
    try:
        sire.caxA.remove()
    except:
        pass


def set_wavelength_range(sire):
    i = str(sire.match)
    if int(sire.wl_min_entry.text()) >= 0 and int(sire.wl_max_entry.text()) < sire.dataset_dict[i]["sir"].Attributes['wl']:
        sire.dataset_dict[i]["sir"].wl_min = int(sire.wl_min_entry.text())
        sire.dataset_dict[i]["sir"].wl_max = int(sire.wl_max_entry.text())
        click(sire, sire.dataset_dict[i])
    else:
        msg = QMessageBox()
        msg.setText("Selected range out of bounds.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        sire.wl_min_entry.setText(str(sire.dataset_dict[i]["sir"].wl_min))
        sire.wl_max_entry.setText(str(sire.dataset_dict[i]["sir"].wl_max))


def set_xy_lim(sire):
    i = str(sire.match)
    if int(sire.x_min_entry.text()) >= 0 and int(sire.x_max_entry.text()) < sire.dataset_dict[i]["sir"].Attributes['x'] and int(sire.y_min_entry.text()) >= 0 and int(sire.y_max_entry.text()) < sire.dataset_dict[i]["sir"].Attributes['y']:
        sire.dataset_dict[i]["sir"].x_min = int(sire.x_min_entry.text())
        sire.dataset_dict[i]["sir"].x_max = int(sire.x_max_entry.text())
        sire.dataset_dict[i]["sir"].y_min = int(sire.y_min_entry.text())
        sire.dataset_dict[i]["sir"].y_max = int(sire.y_max_entry.text())
        sire.change_canvas()
        click(sire, sire.dataset_dict[i])
        update_pixel_info(sire, sire.dataset_dict[i])
    else:
        msg = QMessageBox()
        msg.setText("Selected range out of bounds.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        sire.x_min_entry.setText(str(sire.dataset_dict[i]["sir"].x_min))
        sire.x_max_entry.setText(str(sire.dataset_dict[i]["sir"].x_max))
        sire.y_min_entry.setText(str(sire.dataset_dict[i]["sir"].y_min))
        sire.y_max_entry.setText(str(sire.dataset_dict[i]["sir"].y_max))

def reset_xy_lim(sire):
    i = str(sire.match)
    sire.dataset_dict[i]["sir"].x_min = 0
    sire.dataset_dict[i]["sir"].x_max = int(sire.dataset_dict[i]["sir"].Attributes['x'])
    sire.dataset_dict[i]["sir"].y_min = 0
    sire.dataset_dict[i]["sir"].y_max = int(sire.dataset_dict[i]["sir"].Attributes['y'])
    sire.x_min_entry.setText(str(sire.dataset_dict[i]["sir"].x_min))
    sire.x_max_entry.setText(str(sire.dataset_dict[i]["sir"].x_max))
    sire.y_min_entry.setText(str(sire.dataset_dict[i]["sir"].y_min))
    sire.y_max_entry.setText(str(sire.dataset_dict[i]["sir"].y_max))
    sire.change_canvas()
    click(sire, sire.dataset_dict[i])
    update_pixel_info(sire, sire.dataset_dict[i])

def set_optical_depth_range(sire):
    i = str(sire.match)
    if int(sire.optical_depth_min_entry.text()) >= 0 and int(sire.optical_depth_max_entry.text()) < sire.dataset_dict[i]["sir"].Attributes['optical_depth']:
        sire.dataset_dict[i]["sir"].optical_depth_min = int(sire.optical_depth_min_entry.text())
        sire.dataset_dict[i]["sir"].optical_depth_max = int(sire.optical_depth_max_entry.text())
        click(sire, sire.dataset_dict[i])
    else:
        msg = QMessageBox()
        msg.setText("Selected range out of bounds.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        sire.optical_depth_min_entry.setText(str(sire.dataset_dict[i]["sir"].optical_depth_min))
        sire.optical_depth_max_entry.setText(str(sire.dataset_dict[i]["sir"].optical_depth_max))


def change_frame(sire):
    if sire.increment == 1:
        sire.frame_changed_flag=1
        i = str(sire.match)
        sire.dataset_dict[i]['sir'].current_frame_index = int(sire.frame_scale.value())
        sire.change_canvas()
        click(sire, sire.dataset_dict[i])
        update_pixel_info(sire, sire.dataset_dict[i])
        sire.frame_changed_flag=0


def change_wl(sire):
    if sire.increment == 1:
        i = str(sire.match)
        sire.dataset_dict[i]['sir'].current_wl_index = int(sire.wl_scale.value())
        sire.change_canvas()
        click(sire, sire.dataset_dict[i])
        update_pixel_info(sire, sire.dataset_dict[i])


def change_optical_depth(sire):
    if sire.increment == 1:
        optical_depth = int(sire.optical_depth_scale.value())
        i = str(sire.match)
        sire.dataset_dict[i]['sir'].current_optical_depth_index = int(optical_depth)
        sire.change_canvas()
        click(sire, sire.dataset_dict[i])
        update_pixel_info(sire, sire.dataset_dict[i])


def update_pixel_info(sire, sir):
    T1 = sir["sir"].model1[1,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
    G1 = sir["sir"].model1[6,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
    B1 = sir["sir"].model1[4,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
    A1 = sir["sir"].model1[7,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
    V1 = sir["sir"].model1[5,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]/(100*1000)
    mic1 = sir["sir"].model1[3,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
    if sire.mac1_checkbutton.isChecked():
        ff1 = sir["sir"].mac1[1, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        mac1 = sir["sir"].mac1[0, int(sir["sir"].current_y), int(sir["sir"].current_x)]
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
        T2 = sir["sir"].model2[1,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        G2 = sir["sir"].model2[6,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        B2 = sir["sir"].model2[4,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        A2 = sir["sir"].model2[7,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        V2 = sir["sir"].model2[5,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]/(100*1000)
        mic2 = sir["sir"].model2[3,sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)]
        if sire.mac2_checkbutton.isChecked():
            mac2 = sir["sir"].mac2[0, int(sir["sir"].current_y), int(sir["sir"].current_x)]
            sire.mod2_mac_value.setText(str(round(mac2,3)))
        sire.mod2_ff_value.setText(str(round(1-ff1,3)))
        sire.mod2_T_value.setText(str(round(T2,3)))
        sire.mod2_B_value.setText(str(round(B2,3)))
        sire.mod2_V_value.setText(str(round(V2,3)))
        sire.mod2_G_value.setText(str(round(G2,3)))
        sire.mod2_A_value.setText(str(round(A2,3)))
        sire.mod2_mic_value.setText(str(round(mic2,3)))

    Z = round(sir["sir"].model1[8, sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)], 3)
    OD = round(sir["sir"].model1[0, sir["sir"].current_optical_depth_index, int(sir["sir"].current_y), int(sir["sir"].current_x)], 3)
    sire.pixel_values.setText("X: %s Y: %s Z: %s [cm] OD: %s" %(str(int(sir["sir"].current_x)), str(int(sir["sir"].current_y)), str(Z), str(OD)))

def set_font_sizes(self,sire):
    sire.fontsize_titles = int(self.fontsize_titles_map_entry.text())
    sire.fontsize_axislabels = int(self.fontsize_axislabels_map_entry.text())
    sire.fontsize_ticklabels = int(self.fontsize_ticklabels_map_entry.text())

def set_plotting_preferences(self,sire):
    sire.line_widths = float(self.line_widths_entry.text())
