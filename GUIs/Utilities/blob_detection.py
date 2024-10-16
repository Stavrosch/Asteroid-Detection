from skimage.feature import blob_log
from skimage import exposure
from astropy.table import QTable
import numpy as np

def blob_detection(data,t):
    # Convert data to float for skimage processing
    data_float = data.astype(float)

    # Normalize the data to improve detection accuracy
    data_normalized = exposure.rescale_intensity(data_float)

    # Detect blobs using the Laplacian of Gaussian (LoG) method
    blobs_log = blob_log(data_normalized, max_sigma=10, num_sigma=10, threshold=t)

    # Compute radii from sigma values (LoG provides sigma, but we want radii)
    blobs_log[:, 2] = blobs_log[:, 2] * np.sqrt(2)

    # Extract x, y positions and radii
    xcentroid_blob = blobs_log[:, 1]
    ycentroid_blob = blobs_log[:, 0]
    radii_blob = blobs_log[:, 2]
    detected_sources = QTable([xcentroid_blob, ycentroid_blob, radii_blob], names=('xcentroid', 'ycentroid', 'radius'))
    
    return detected_sources