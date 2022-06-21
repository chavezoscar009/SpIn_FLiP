import numpy as np
from astropy import units as u
from astropy.modeling import models, fitting
import matplotlib.pyplot as plt
from specutils import Spectrum1D, SpectralRegion
from specutils.manipulation import extract_region
from astropy.nddata import StdDevUncertainty

class Spectra():

    def __init__(self, wavelength, flux, error = False):
        
        '''
        
        '''
        #self.wavelength = wavelength
        #self.flux = flux
        self.voigt_params = None
        self.sub_spectrum = None

        if error:
            spec_error = StdDevUncertainty(error)
            self.spectrum = Spectrum1D(spectral_axis= wavelength * u.AA, 
                                       flux = flux * u.dimensionless_unscaled, 
                                       uncertainty = spec_error) 
        else:
            self.spectrum = Spectrum1D(spectral_axis= wavelength * u.AA, 
                                       flux = flux * u.dimensionless_unscaled)
            
    def plotting_spec(self):

        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (5, 7), constrained_layout = True)
        ax.plot(self.sub_spectrum.wavelength, self.sub_spectrum.flux, color = 'black')
        ax.plot(self.sub_spectrum.wavelength, self.voigt_params(self.sub_spectrum.wavelength))

        return ax

    def Fitting(self, line_wavelength, window):
        '''
        Function to fit a Voigt profile to line center provided and window region
        '''
        
        #Setting the sub region
        sub_region = SpectralRegion(line_wavelength - window, line_wavelength + window)
        
        #extracting the sub_region above
        self.sub_spectrum = extract_region(self.spectrum, sub_region)

        voigt_model = models.Voigt1D(x_0 = line_wavelength)
        voigt_fitter = fitting.LevMarLSQFitter()

        self.voigt_params = voigt_fitter(model = voigt_model, 
                                         x = self.sub_spectrum.wavelength, 
                                         y = self.sub_spectrum.flux)

        

