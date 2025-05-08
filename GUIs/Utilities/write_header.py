from astropy.io import fits
from astropy.wcs import WCS

# Compute the new WCS as before
def write_header(wcs,image_path):
    # Create a new header with the updated WCS
    new_header = wcs.to_header()

    # Open the original FITS file
    file = fits.open(image_path)

    with fits.open(image_path, mode='update') as file:
        # Update the header of the primary HDU
        file[0].header.update(new_header)
        
        # Write changes back to the same file
        file.flush()  # Ensures changes are saved to disk

