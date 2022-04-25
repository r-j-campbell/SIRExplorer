import numpy as np

class Imager: #files should be [y,x] or [t,y,x]
    def __init__(self):
        self.Attributes = {
            'wavelength': 0000, #Angstroms
            'x': 100.0,
            'y': 100.0,
            't': 100.0,
            'pxscalex': 0.1, #arcsec/pixel
            'pxscaley': 0.1,
        }
        self.im=np.zeros((int(self.Attributes['x']), int(self.Attributes['y'])))
        self.current_frame_index = 0
    def update_value(self,attribute,newvalue):
        self.Attributes[attribute] = newvalue
    def update_im(self,im):
        self.im = im

class IFU: #files should be [t,St,y,x,wl] or [St,y,x,wl]
    def __init__(self):
        self.Attributes = {
            'wavelength': 0000, #rest wavelength, Angstroms
            't': 100.0, #num frames
            'S': 4, #num Stokes pts
            'y': 100.0, #num y pts
            'x': 100.0, #num x pts
            'wl': 100.0, #number of wl points
            'pxscalex': 0.1, #arcsec/pixel
            'pxscaley': 0.1,
            'wl_off': 0,
            'wl_disp': 0,
            'wlscale': None

        }
        self.im=np.zeros((int(self.Attributes['x']), int(self.Attributes['y'])))
        self.current_x=0
        self.current_y=0
        self.current_frame_index = 0
        self.current_wl_index = 0
        self.current_Stokes_index = 0
        self.x0 = 0
        self.x1 = 1
        self.y0 = 0
        self.y1 = 1
        self.wl0 = 0
        self.wl1 = 1
        self.continuum_value=100000
    def update_value(self,attribute,newvalue):
        self.Attributes[attribute] = newvalue
    def update_im(self,im):
        self.im = im


class SSP: #files should be [St,wl,y,x]
    def __init__(self):
        self.Attributes = {
            'wavelength': 0000, #rest wavelength, Angstroms
            'S': 4, #num Stokes pts
            'y': 100.0, #num y pts
            'x': 100.0, #num x pts
            'wl': 100.0, #number of wl points
            'pxscalex': 0.1, #arcsec/pixel
            'pxscaley': 0.1,
            'wl_off': 0,
            'wl_disp': 0,
            'wlscale': None

        }
        self.img=np.zeros((int(self.Attributes['x']), int(self.Attributes['y'])))
        self.current_x=0
        self.current_y=0
        self.current_wl_index = 0
        self.x0 = 0
        self.x1 = 1
        self.y0 = 0
        self.y1 = 1
        self.wl0 = 0
        self.wl1 = 1
        self.continuum_value=100000
    def _updateValue(self,attribute,newvalue):
        self.Attributes[attribute] = newvalue
    def _updateim(self,im):
        self.im=im


class SIR: #files should be [t,St,y,x,wl]
    def __init__(self):
        self.Attributes = {
            'wavelength': 0000, #rest wavelength, Angstroms
            'S': 4, #num Stokes pts
            'y': 100.0, #num y pts
            'x': 100.0, #num x pts
            'wl': 100.0, #number of wl points
            'pxscalex': 0.1, #arcsec/pixel
            'pxscaley': 0.1,

        }
        self.img=np.zeros((int(self.Attributes['x']), int(self.Attributes['y'])))
        self.meanspectra=None
        self.window_x=0 #stores co-ords of clicked pixel in x
        self.window_y=0 #stores co-ords of clicked pixel in y
        self.current_wl_index = 0
        self.current_Stokes_index = 0
    def _updateValue(self,attribute,newvalue):
        self.Attributes[attribute] = newvalue
    def _updateimg(self,im):
        self.img=im
    def _updatemeanspectra(self,im):
        self.meanspectra=im


