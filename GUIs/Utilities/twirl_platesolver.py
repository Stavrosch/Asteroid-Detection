import twirl
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
from Utilities import RA_deg,Decl_deg, FOV_calc


def plate_solve(image_path,fov,RA,Dec):
    file = fits.open(image_path)
    image_data = fits.getdata(image_path)

   
    center = SkyCoord(RA, Dec, unit=["deg", "deg"])

    stars = twirl.find_peaks(image_data)[0:15]
    radec = twirl.gaia_radecs(center,1.5*fov,limit=20)

    wcs = twirl.compute_wcs(stars, radec[0:30], tolerance=10)
    
    
    return wcs,radec,stars

if __name__== "__main__" :    
    image_path = r'C:\Users\stavr\OneDrive\Desktop\Asteroid Data\301_mpc\301_mpc_1.1\01_22_43\301_mpc_1.1_00001.fits'
    file = fits.open(image_path)
    image = file[0]

    image_data = fits.getdata(image_path)
    RA = image.header['RA']
    DEC = image.header['DEC']
    NAXIS1 = image.header['NAXIS1']
    NAXIS2 = image.header['NAXIS2']
    XPIXSZ = 3.8 * 10**-3  # in mm
    YPIXSZ = 3.8 * 10**-3  # in mm

    focal_length = 620  # Rasa 11 Cyprus in mm
    #print('Image Scale',aspp)
    h,w = FOV_calc(NAXIS1,NAXIS2,XPIXSZ,YPIXSZ,focal_length)
    RA=RA_deg(RA)
    Dec=Decl_deg(DEC)


    shape = image_data.shape
    pixel_in_deg = (1.26 * u.arcsec).to(u.deg).value
    fov = max(h,w)

    med = np.median(image_data)
    wcs,radec,stars=plate_solve(image_path,fov,RA,Dec)
    print('ok')

    plt.figure(figsize=(8,8))
    gaias_pixel = np.array(SkyCoord(radec, unit="deg").to_pixel(wcs)).T
    plt.imshow(image_data, cmap="Greys_r", vmax=np.std(image_data)*2 + med, vmin=med)
    plt.plot(*stars.T, "o", fillstyle="none", c="w", ms=12)
    plt.plot(*gaias_pixel.T, "o", fillstyle="none", c="C1", ms=18)
    plt.show()

    wcs1= WCS(image.header)
    print(wcs,wcs1)