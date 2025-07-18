from astropy.wcs import WCS
from astropy.io import fits
from astropy.coordinates import SkyCoord
def image_center(NAXIS1,NAXIS2,wcs):
    center_pixel_x = NAXIS1/2
    center_pixel_y = NAXIS2/2
    center_coord= wcs.pixel_to_world(center_pixel_x, center_pixel_y)
    print(type(center_coord))
    print(center_coord)
    if isinstance(center_coord, list):
        center_coord = center_coord[0]
    elif hasattr(center_coord, '__len__') and not isinstance(center_coord, SkyCoord):
        center_coord = center_coord[0]
    ra = center_coord.ra.deg  # Right Ascension in degrees
    dec = center_coord.dec.deg  # Declination in degrees
    return ra,dec