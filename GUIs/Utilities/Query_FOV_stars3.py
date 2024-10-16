import numpy as np
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.gaia import Gaia

def Query_FOV_stars3(wsc,RA,DEC,width,height):
    wsc=wsc
    Gaia.MAIN_GAIA_TABLE = "gaiaedr3.gaia_source"
    Gaia.ROW_LIMIT = 1000  # Adjust row limit as needed
    
    
    center = SkyCoord(ra=RA, dec=DEC, unit='deg', frame='icrs')
    dx = width / 2
    dy = height/ 2
    corners = np.array([[-dx, -dy], [dx, -dy], [dx, dy], [-dx, dy]])

    # Apply the CD matrix (rotation and scale)
    rotated_corners = np.dot(corners, wsc.wcs.cd)

    # Convert back to world coordinates (RA/DEC)
    world_coords = wsc.wcs_pix2world(rotated_corners, 1)
    rotated_ra_dec = SkyCoord(world_coords[:, 0], world_coords[:, 1], unit='deg')

    # Construct the polygon query
    polygon_query = ", ".join([f"{ra}, {dec}" for ra, dec in zip(rotated_ra_dec.ra.deg, rotated_ra_dec.dec.deg)])

    query = f"""
    SELECT *
    FROM gaiaedr3.gaia_source
    WHERE 1=CONTAINS(
        POINT('ICRS', gaiaedr3.gaia_source.ra, gaiaedr3.gaia_source.dec),
        POLYGON('ICRS', {polygon_query})
    )
    """
    
    job = Gaia.launch_job_async(query=query)
    results = job.get_results()
    
    return results