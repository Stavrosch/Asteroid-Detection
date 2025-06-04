import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

def residual_calc_local(corr_file_path):
    with fits.open(corr_file_path) as hdul:
        data = hdul[1].data

        field_coords = SkyCoord(ra=data['field_ra'], dec=data['field_dec'], unit='deg')
        index_coords = SkyCoord(ra=data['index_ra'], dec=data['index_dec'], unit='deg')

        separations = field_coords.separation(index_coords).arcsecond


        rms_residual = np.sqrt(np.mean(separations**2))
        return rms_residual
