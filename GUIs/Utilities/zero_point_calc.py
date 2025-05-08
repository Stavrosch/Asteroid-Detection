from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.gaia import Gaia
import numpy as np
from astropy.wcs import WCS
import contextlib
import io


def zero_point_calc(x,y,image,flux):
    wcs = WCS(image.header)
    coord = wcs.pixel_to_world(x, y)
    
    "Multiple Queries"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            gaia_data = Gaia.query_object_async(coord, radius=5 * u.arcsec)        #print(gaia_data)
        #print(gaia_data)
        r_mag = gaia_data['phot_g_mean_mag'][0] 
        #print(f"r_mag: {r_mag}") 
        #print(r_mag)
        star_flux = flux 

        zero_point_mag = r_mag + 2.5 * np.log10(star_flux)
        #print(f"Zero-point magnitude: {zero_point_mag}")
        return zero_point_mag
    except Exception:
        return None