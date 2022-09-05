import numpy as np

class SIR:
    def __init__(self):
        self.Attributes = {
            'wavelength': 0000, #rest wavelength, Angstroms
            'S': 4, #num Stokes pts
            'y': 100.0, #num y pts
            'x': 100.0, #num x pts
            'wl': 100.0, #number of wl points
            't':0, #num frames
            'optical_depth':100, #num optical depth points
            'pxscalex': 0.1, #arcsec/pixel
            'pxscaley': 0.1,
            'model2_flag': False,
            'mac1_flag': False,
            'mac2_flag': False,
            'binary_flag': False

        }
        self.obs = np.empty([int(self.Attributes['S']+2), int(self.Attributes['wl']), int(self.Attributes['y']), int(self.Attributes['x'])])
        self.syn = np.empty([int(self.Attributes['S']+2), int(self.Attributes['wl']), int(self.Attributes['y']), int(self.Attributes['x'])])
        self.model1 = np.empty([11, int(self.Attributes['optical_depth']),int(self.Attributes['y']), int(self.Attributes['x'])])
        self.model2 = np.empty([11, int(self.Attributes['optical_depth']),int(self.Attributes['y']), int(self.Attributes['x'])])
        self.mac1 = np.empty((int(self.Attributes['y']), int(self.Attributes['x'])))
        self.mac2 = np.empty((int(self.Attributes['y']), int(self.Attributes['x'])))
        self.binary = np.ones((int(self.Attributes['y']), int(self.Attributes['x'])))
        self.chi2 = np.ones((int(self.Attributes['y']), int(self.Attributes['x'])))
        self.current_wl_index = 0
        self.current_frame_index = 0
        self.current_optical_depth_index = 0
        self.current_x = 0
        self.current_y = 0
        self.wl_min = 0
        self.wl_max = 100
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.optical_depth_min = 0
        self.optical_depth_max = 100
    def update_binary(self,binary):
        self.binary=binary
    def update_chi2(self,chi2):
        self.chi2=chi2
    def update_model1(self,model1):
        self.model1=model1
    def update_model2(self,model2):
        self.model2=model2
    def update_mac1(self,mac1):
        self.mac1=mac1
    def update_mac2(self,mac2):
        self.mac2=mac2
    def update_obs(self,obs):
        self.obs=obs
    def update_syn(self,syn):
        self.syn=syn
