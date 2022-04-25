import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import astropy.io.fits as pyfits
import matplotlib
matplotlib.use("TkAgg")

def show_plot(self):
    self.sc1.ax1.imshow(np.random.randint(1,5,size=(4,4)))
    self.sc1.fig.canvas.draw()

def show_imager(self,class_object):
    print("show imager")

def show_IFU(self,class_object,click_increment,increment,frame_flag,flag):
    print("show IFU",click_increment,increment,frame_flag,flag)
    if increment ==1 or frame_flag == 1:
        print("clearing canvas")
        self.sc1.ax1.clear()
        self.sc1.ax2.clear()
        self.sc1.ax3.clear()
        self.sc1.ax4.clear()
        try:
            print("removing cbars")
            self.cax_I_im.remove()
            self.cax_Q_im.remove()
            self.cax_U_im.remove()
            self.cax_V_im.remove()
        except:
            print("Something went wrong")
        else:
            print("Nothing went wrong")
    if flag == False or frame_flag == 1:
        im = pyfits.open(class_object["file"])[0].data
        im = np.squeeze(im)
        print(im.shape)
        if im.ndim == 4:
            self.frame_flag=0
        if im.ndim == 5: #executed only if there are multiple frames of data
            self.frame_flag=1
            class_object["class_object"].Attributes["t"] = im.shape[0]
            im = im[class_object["class_object"].current_frame_index,:,:,:,:]
            #self.control_panel.framescale.configure(to=class_object['class_object'].Attributes['t']-1)
        class_object["class_object"].Attributes["y"] = im.shape[1]
        class_object["class_object"].Attributes["x"] = im.shape[2]
        class_object["class_object"].Attributes["wl"] = im.shape[3]
        #self.control_panel.wlscale.configure(to=class_object['class_object'].Attributes['wl']-1)
        class_object["class_object"].update_im(im)
        if self.continuum_flag == 1:
            class_object["class_object"].continuum_value = np.nanmean(class_object["class_object"].im[0,int(class_object["class_object"].y0):int(class_object["class_object"].y1), int(class_object["class_object"].x0):int(class_object["class_object"].x1), int(class_object["class_object"].wl0):int(class_object["class_object"].wl1)])
            im = class_object["class_object"].im/class_object["class_object"].continuum_value
            class_object["class_object"].update_im(im)

    if self.I_im_CT[3] == 0:
        I_im_map = self.sc1.ax1.imshow(im[0,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.I_im_CT[0],vmin=self.I_im_CT[1],vmax=self.I_im_CT[2])
    elif self.I_im_CT[3] == 1:
        I_im_map = self.sc1.ax1.imshow(im[0,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.I_im_CT[0])
    divider_I_im = make_axes_locatable(self.sc1.ax1)
    self.cax_I_im = divider_I_im.append_axes("right", size="3%",pad=0)
    self.cbar_I_im = self.sc1.fig.colorbar(I_im_map, cax=self.cax_I_im,pad=2)
    self.cbar_I_im.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.Q_im_CT[3] == 0:
        Q_im_map = self.sc1.ax2.imshow(im[1,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.Q_im_CT[0],vmin=self.Q_im_CT[1],vmax=self.Q_im_CT[2])
    elif self.Q_im_CT[3] == 1:
        Q_im_map = self.sc1.ax2.imshow(im[1,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.Q_im_CT[0])
    divider_Q_im = make_axes_locatable(self.sc1.ax2)
    self.cax_Q_im = divider_Q_im.append_axes("right", size="3%",pad=0)
    self.cbar_Q_im = self.sc1.fig.colorbar(Q_im_map, cax=self.cax_Q_im,pad=2)
    self.cbar_Q_im.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.U_im_CT[3] == 0:
        U_im_map = self.sc1.ax3.imshow(im[2,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.U_im_CT[0],vmin=self.U_im_CT[1],vmax=self.U_im_CT[2])
    elif self.U_im_CT[3] == 1:
        U_im_map = self.sc1.ax3.imshow(im[2,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.U_im_CT[0])
    divider_U_im = make_axes_locatable(self.sc1.ax3)
    self.cax_U_im = divider_U_im.append_axes("right", size="3%",pad=0)
    self.cbar_U_im = self.sc1.fig.colorbar(U_im_map, cax=self.cax_U_im,pad=2)
    self.cbar_U_im.ax.tick_params(labelsize=self.fontsize_axislabels)

    if self.V_im_CT[3] == 0:
        V_im_map = self.sc1.ax4.imshow(im[3,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.V_im_CT[0],vmin=self.V_im_CT[1],vmax=self.V_im_CT[2])
    elif self.V_im_CT[3] == 1:
        V_im_map = self.sc1.ax4.imshow(im[3,:,:,class_object["class_object"].current_wl_index],origin='lower',cmap=self.V_im_CT[0])
    divider_V_im = make_axes_locatable(self.sc1.ax4)
    self.cax_V_im = divider_V_im.append_axes("right", size="3%",pad=0)
    self.cbar_V_im = self.sc1.fig.colorbar(V_im_map, cax=self.cax_V_im,pad=2)
    self.cbar_V_im.ax.tick_params(labelsize=self.fontsize_axislabels)

    self.sc1.ax1.axvline(class_object["class_object"].current_x,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax1.axhline(class_object["class_object"].current_y,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax2.axvline(class_object["class_object"].current_x,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax2.axhline(class_object["class_object"].current_y,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax3.axvline(class_object["class_object"].current_x,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax3.axhline(class_object["class_object"].current_y,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax4.axvline(class_object["class_object"].current_x,color='red',linestyle=':',linewidth=self.linewidth)
    self.sc1.ax4.axhline(class_object["class_object"].current_y,color='red',linestyle=':',linewidth=self.linewidth)

    self.sc1.fig.canvas.draw()

def click_IFU(self,class_object,click_increment):
    current_x = class_object["class_object"].current_x
    current_y = class_object["class_object"].current_y
    print(current_x,current_y,click_increment)
#    if click_increment == 1:
    self.sc2.ax1.clear()
    self.sc2.ax2.clear()
    self.sc2.ax3.clear()
    self.sc2.ax4.clear()
    self.sc2.ax1.set_title("Stokes $I$ [$I_c$]",fontsize=self.fontsize_titles)
    self.sc2.ax2.set_title("Stokes $Q$ [$I_c$]",fontsize=self.fontsize_titles)
    self.sc2.ax3.set_title("Stokes $U$ [$I_c$]",fontsize=self.fontsize_titles)
    self.sc2.ax4.set_title("Stokes $V$ [$I_c$]",fontsize=self.fontsize_titles)
    self.sc2.ax1.set_xlabel("wavelength [pix.]",fontsize=self.fontsize_axislabels)
    self.sc2.ax2.set_xlabel("wavelength [pix.]",fontsize=self.fontsize_axislabels)
    self.sc2.ax3.set_xlabel("wavelength [pix.]",fontsize=self.fontsize_axislabels)
    self.sc2.ax4.set_xlabel("wavelength [pix.]",fontsize=self.fontsize_axislabels)

    im = class_object["class_object"].im

    self.sc2.ax1.plot(im[0,int(current_y),int(current_x),:],linewidth=self.linewidth)
    self.sc2.ax1.axvline(class_object["class_object"].current_wl_index,linestyle=':',color='gray',linewidth=self.linewidth)
    #self.canvas_frame.ax_I.set_xlim(self.wl_min,self.wl_max)

    self.sc2.ax2.plot(im[1,int(current_y),int(current_x),:],linewidth=self.linewidth)
    self.sc2.ax2.axvline(class_object["class_object"].current_wl_index,linestyle=':',color='gray',linewidth=self.linewidth)

    self.sc2.ax3.plot(im[2,int(current_y),int(current_x),:],linewidth=self.linewidth)
    self.sc2.ax3.axvline(class_object["class_object"].current_wl_index,linestyle=':',color='gray',linewidth=self.linewidth)

    self.sc2.ax4.plot(im[3,int(current_y),int(current_x),:],linewidth=self.linewidth)
    self.sc2.ax4.axvline(class_object["class_object"].current_wl_index,linestyle=':',color='gray',linewidth=self.linewidth)

    self.sc2.fig.canvas.draw()


def change_frame(self,frame):
    self.flag = False
    self.get_all_values(self.class_objects,0,self.select_file.currentText())
    if self.flag == True:
        i=str(self.match)
        self.class_objects[i]['class_object'].current_frame_index = int(frame)
        self.framescale.setMinimum(0)
        self.framescale.setMaximum(self.class_objects[i]['class_object'].Attributes['t']-1)
        self.change_canvas()
        if self.select_instrument.currentText() == "GREGOR/GRIS-IFU" or self.select_instrument.currentText() == "Integral field unit (IFU)":
            click_IFU(self,self.class_objects[i],self.click_increment)
    elif self.flag == False:
        print("ERROR")
