import requests
import numpy as np
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
def residual_calc(hdu,JOB_ID):

    wcs = WCS(hdu.header)
    pixel_scales_deg = proj_plane_pixel_scales(wcs)
    pixel_scales_arcsec = pixel_scales_deg * 3600 
    mean_pixel_scale_arcsec = np.mean(pixel_scales_arcsec)
    #print(wcs)
    ANNOTATION_URL = f"http://nova.astrometry.net/api/jobs/{JOB_ID}/annotations/"
    print(ANNOTATION_URL)


    response = requests.get(ANNOTATION_URL,timeout=10)
    print(response.status_code)  # Should be 200
    #print(response.text)
    #print(response.headers)
    data = response.json()
    #print('hi')
    #print(data)
    annotations = data.get("annotations", [])


    star_positions = []
    for entry in annotations:
        if "pixelx" in entry and "pixely" in entry:
            star_positions.append((entry["names"], entry["pixelx"], entry["pixely"]))
    print(star_positions)
    Gaia.ROW_LIMIT = 100  
    residuals = []
    for name, x, y in star_positions:
        if len(residuals) == 10:
            break
        if name[0]!='': 
            print(f"Querying Gaia for star {name[0]}...")
            star_id = name[0].split(" ")[1]      
            print(star_id)     
            gaia_query = f"""
            SELECT g.ra, g.dec 
            FROM gaiadr3.gaia_source AS g
            JOIN gaiadr3.tycho2tdsc_merge_best_neighbour AS t
            ON g.source_id = t.source_id
            WHERE t.original_ext_source_id = '{star_id}'
            """
            
            job = Gaia.launch_job(gaia_query)
            #print(job)
            results = job.get_results()
            print(results)
            print("Hello World")
            #print(results.status_code)  # Should be 200

            if len(results) > 0:

                gaia_ra, gaia_dec = results["ra"][0], results["dec"][0]
                print(gaia_dec, gaia_ra)

                gaia_coord = SkyCoord(ra=gaia_ra * u.deg, dec=gaia_dec * u.deg, frame="icrs")
                print(gaia_coord)
                x_gaia, y_gaia = wcs.wcs_world2pix(gaia_coord.ra.deg, gaia_coord.dec.deg, 0)               
                print(type(x_gaia),x_gaia, y_gaia)
                x_gaia = float(x_gaia)
                y_gaia = float(y_gaia)
                print(type(x),x,y)
                x = float(x)
                y = float(y)
                delta_x = x - x_gaia  
                delta_y = y - y_gaia
                residual = np.sqrt(delta_x**2 + delta_y**2)
                residual_pix = np.sqrt(delta_x**2 + delta_y**2)
                residual_arcsec = residual_pix * mean_pixel_scale_arcsec
                residuals.append((name[0], residual_arcsec))

            
    for star, res in residuals:
       print(f"Star {star}: Residual = {res:.5f} arcsec")
    
    if residuals :
        m_res = np.mean([r[1] for r in residuals])
        if abs(m_res) > 10:
            m_res = np.nan
    else:
        m_res = np.nan
    return m_res