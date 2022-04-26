import numpy as np

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


