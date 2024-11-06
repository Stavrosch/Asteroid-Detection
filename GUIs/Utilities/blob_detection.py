from skimage.feature import blob_log
from skimage import exposure
from astropy.table import QTable
import numpy as np

def blob_detection(data,t):
    min_radius=1.5
    # Convert data to float for skimage processing
    data_float = data.astype(float)

    # Normalize the data to improve detection accuracy
    data_normalized = exposure.rescale_intensity(data_float)

    # Detect blobs using the Laplacian of Gaussian (LoG) method
    blobs_log = blob_log(data_normalized, max_sigma=10, num_sigma=10, threshold=t)
    blobs_log[:, 2] = blobs_log[:, 2] * np.sqrt(2)
    # Calculate the median and standard deviation of the image for background estimation
    median_background = np.median(data_float)
    std_background = np.std(data_float)

    background_threshold = median_background + 2 * std_background

    # Extract x, y positions and radii
    xcentroid_blob = blobs_log[:, 1]
    ycentroid_blob = blobs_log[:, 0]
    radii_blob = blobs_log[:, 2]
    valid_blobs = []
    max_pixel_count = 40000
    for i in range(len(radii_blob)):
        radius = radii_blob[i]
        x = int(xcentroid_blob[i])
        y = int(ycentroid_blob[i])
        pixel_value = data_float[y, x]
        # Condition to filter out one-pixel blobs with high intensity
        if (np.isclose(radius, 1.414, atol=0.01)):
            neighbors = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and 0 <= y + dy < data_float.shape[0] and 0 <= x + dx < data_float.shape[1]:
                        neighbors.append(data_float[y + dy, x + dx])
            
            # Check if neighboring pixel values drop significantly
            if neighbors:
                neighbor_value = max(neighbors)
                print(neighbor_value)
                if neighbor_value<0.2*pixel_value or neighbor_value<background_threshold: #->median background
                    # This is likely a bad/hot pixel - skip this blob
                    continue

        # If passed the checks, add to the list of valid blobs
        valid_blobs.append(i)
            
    
        # Filter the blobs using the valid indices
    xcentroid_blob = xcentroid_blob[valid_blobs]
    ycentroid_blob = ycentroid_blob[valid_blobs]
    radii_blob = radii_blob[valid_blobs]
    detected_sources = QTable([xcentroid_blob, ycentroid_blob, radii_blob], names=('xcentroid', 'ycentroid', 'radius'))
    return detected_sources