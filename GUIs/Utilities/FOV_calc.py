import math
from astropy.io import fits


def FOV_calc(NAXIS1,NAXIS2,XPIXSZ,YPIXSZ,focal_length):

    # Sensor dimensions in mm
    sensor_width_mm = NAXIS1 * XPIXSZ
    sensor_height_mm = NAXIS2 * YPIXSZ
    
    # Field of View trigonometry
    fov_width_deg = 2 * math.degrees(math.atan(sensor_width_mm / (2 * focal_length)))
    fov_height_deg = 2 * math.degrees(math.atan(sensor_height_mm / (2 * focal_length)))
    return fov_width_deg, fov_height_deg

if __name__== "__main__" :
    Img = r'C:\Users\stavr\OneDrive\Desktop\Asteroid Data\301_mpc\301_mpc_1.1\01_22_43\301_mpc_1.1_00001.fits'
    file = fits.open(Img)
    image = file[0]
    header = image.header
    NAXIS1 = image.header['NAXIS1']
    NAXIS2 = image.header['NAXIS2']
    NAXIS1 = 1600
    NAXIS2 = 1200
    XPIXSZ = 3.8 * 10**-3  # in mm
    YPIXSZ = 3.8 * 10**-3  # in mm
    pixel_size= 5.86 # in μm
    focal_length = 620  # Rasa 11 Cyprus in mm
    aspp =  (pixel_size/focal_length)*206.265
    #print('Image Scale',aspp)
    print(FOV_calc(NAXIS1,NAXIS2,XPIXSZ,YPIXSZ,focal_length))