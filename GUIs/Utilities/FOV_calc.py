import math
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm
import matplotlib.patches as patches
from astropy.visualization import ZScaleInterval,LogStretch,ImageNormalize,LinearStretch


def FOV_calc(NAXIS1, NAXIS2, XPIXSZ, YPIXSZ, focal_length):
    # Sensor dimensions in mm
    sensor_width_mm = NAXIS2 * XPIXSZ
    sensor_height_mm = NAXIS1 * YPIXSZ

    # Field of View trigonometry
    fov_width_deg = 2 * math.degrees(math.atan(sensor_width_mm / (2 * focal_length)))
    fov_height_deg = 2 * math.degrees(math.atan(sensor_height_mm / (2 * focal_length)))
    return fov_width_deg, fov_height_deg


if __name__ == "__main__":
    # Load FITS file
    Img = r'c:\Users\stavr\OneDrive\Desktop\Asteroid Data\AUTH-2\253\253_mpc_1.1\22_17_14\253_mpc_1.1_00001.fits'
    
    file = fits.open(Img)
    image = file[0]
    data = image.data
    header = image.header

    # Set parameters
    NAXIS1 = header['NAXIS1']
    NAXIS2 = header['NAXIS2']
    XPIXSZ = 3.8 * 10 ** -3  # in mm
    YPIXSZ = 3.8 * 10 ** -3  # in mm
    focal_length = 620  # Rasa 11 Cyprus in mm

    # Calculate Field of View
    fov_width_deg, fov_height_deg = FOV_calc(NAXIS1, NAXIS2, XPIXSZ, YPIXSZ, focal_length)
    print(f"FOV Width: {fov_width_deg:.2f} degrees, FOV Height: {fov_height_deg:.2f} degrees")


    # Plot the image data for visual check
    plt.figure(figsize=(10, 10))
    norm = ImageNormalize(data, interval=ZScaleInterval(), stretch=LinearStretch())  # Log normalization for better visibility
    plt.imshow(data, cmap='Greys', origin='lower', norm=norm, interpolation='nearest')
    plt.colorbar(label='Pixel Value')
    plt.title('FITS Image Data with Log Normalization')
    plt.xlabel('X Pixels')
    plt.ylabel('Y Pixels')
    
    # Add Field of View rectangle using FOV in degrees
    fov_rect = patches.Rectangle((0, 0), fov_width_deg, fov_height_deg, linewidth=2, edgecolor='red', facecolor='none')
    plt.gca().add_patch(fov_rect)
    plt.text(10, 10, f'FOV: {fov_width_deg:.2f} x {fov_height_deg:.2f} deg', color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.show()
