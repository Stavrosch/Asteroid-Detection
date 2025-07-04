from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

def Query_FOV_stars3(RA_deg, DEC_deg, width, height, query_length,NAXIS1, NAXIS2, wcs,
                    rotation_angle=0, mag_column="phot_g_mean_mag"):
    """Query Gaia within a rotated rectangular FOV."""
    Gaia.MAIN_GAIA_TABLE = "gaiaedr3.gaia_source"
    Gaia.ROW_LIMIT = query_length
    
    # Calculate the four corners
    # Get the four corners of the image in sky coordinates
    corners_pixels = [
        [0, 0],          # Bottom-left
        [0, NAXIS2],     # Top-left
        [NAXIS1, NAXIS2],# Top-right
        [NAXIS1, 0]      # Bottom-right
    ]
    
    # Convert pixel coordinates to RA/Dec
    corners_sky = wcs.pixel_to_world_values(corners_pixels)

    polygon = "POLYGON('ICRS', " + ", ".join([f"{ra}, {dec}" for ra, dec in corners_sky]) + ")"    
    
    query = f"""
    SELECT TOP {10* query_length}*
    FROM gaiaedr3.gaia_source
    WHERE 1=CONTAINS(
        POINT('ICRS', ra, dec),
        {polygon}
    )
    ORDER BY {mag_column} ASC
    """
    
    
    try:
        job = Gaia.launch_job_async(query)
        results = job.get_results()
        print(f"Number of stars in FOV: {len(results)}")
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return None