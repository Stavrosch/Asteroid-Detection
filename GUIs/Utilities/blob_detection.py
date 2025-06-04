from skimage.feature import blob_log
from skimage import exposure
from astropy.table import QTable
import numpy as np
from .zero_point_calc import zero_point_calc
from photutils.background import Background2D, MedianBackground
from astropy.stats import SigmaClip

def blob_detection(data,t, image,ZMAG,EXPTIME, aperture_radius=5):
    min_radius=1.5
    data_float = data.astype(float)

    data_normalized = exposure.rescale_intensity(data_float)

    blobs_log = blob_log(data_normalized, max_sigma=10, num_sigma=10, threshold=t)
    blobs_log[:, 2] = blobs_log[:, 2] * np.sqrt(2)

    median_background = np.median(data_float)
    std_background = np.std(data_float)
    background_threshold = median_background + 2 * std_background
    sigma_clip = SigmaClip(sigma=3.0)
    bkg_estimator = MedianBackground()
    bkg = Background2D(data_float, box_size=(50, 50), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
    
    xcentroid_blob = blobs_log[:, 1]
    ycentroid_blob = blobs_log[:, 0]
    radii_blob = blobs_log[:, 2]
    valid_blobs = []
    magnitudes = []
    magnitudes2 = []

    zero_point_mags= []
    z1=1
    z2=0
    fluxes=[]
    #max_pixel_count = 40000
    for i in range(len(radii_blob)):
        radius = radii_blob[i]
        x = int(xcentroid_blob[i])
        y = int(ycentroid_blob[i])
        pixel_value = data_float[y, x]
        
        ### CHECK FOR HOT PIXELS####
        if (np.isclose(radius, 1.414, atol=0.01)):
            neighbors = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and 0 <= y + dy < data_float.shape[0] and 0 <= x + dx < data_float.shape[1]:
                        neighbors.append(data_float[y + dy, x + dx])
            
            if neighbors:
                neighbor_value = max(neighbors)
                #print(neighbor_value)
                if neighbor_value<0.2*pixel_value or neighbor_value<background_threshold: #->median background
                    continue

        valid_blobs.append(i)
        
        ### CALCULATE FLUX WITHIN AN APERTURE ###
        y_min = max(0, y - aperture_radius)
        y_max = min(data_float.shape[0], y + aperture_radius + 1)
        x_min = max(0, x - aperture_radius)
        x_max = min(data_float.shape[1], x + aperture_radius + 1)
        local_background = bkg.background[y_min:y_max, x_min:x_max]
        aperture = data_float[y_min:y_max, x_min:x_max]
        flux = np.sum(aperture-local_background)
        if i < 20 and ZMAG==0:
            zero_point_mag = zero_point_calc(xcentroid_blob[i],ycentroid_blob[i],image,flux)
            #print(f"Zero-point magnitude: {zero_point_mag}")
            #print(i)
            if zero_point_mag is not None:
                zero_point_mags.append(zero_point_mag)

        fluxes.append(flux)
    magnitudes = []
    
    
    for i in range(len(fluxes)):    
        ### CONVERT FLUX TO MAGNITUDE ###
        flux = fluxes[i]
        if flux > 0:
            if ZMAG == 0:
                z = np.mean(zero_point_mags)
                mag = z - 2.5 * np.log10(flux)
                magnitudes.append(mag)
            else:
                z = ZMAG
                mag= -2.5 * np.log10(flux/EXPTIME)+ZMAG
                magnitudes.append(mag)
                
            #print(mag2,mag)
        else:
            mag = np.nan  # Handle cases where flux is zero or negative

        
    print(f"Zero-point magnitude: {z}")
    
    #print(f"Lengths: xcentroid_blob={len(xcentroid_blob)}, ycentroid_blob={len(ycentroid_blob)}, radii_blob={len(radii_blob)}, magnitudes={len(magnitudes)}")
    # Filter the blobs using the valid indices
    xcentroid_blob = xcentroid_blob[valid_blobs]
    ycentroid_blob = ycentroid_blob[valid_blobs]
    radii_blob = radii_blob[valid_blobs]
    magnitudes = np.array(magnitudes)
    detected_sources = QTable([xcentroid_blob, ycentroid_blob, radii_blob, magnitudes],
                            names=('xcentroid', 'ycentroid', 'radius','magnitude'))
    
    return detected_sources