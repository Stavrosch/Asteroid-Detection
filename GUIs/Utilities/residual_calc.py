import requests
import numpy as np
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales

def residual_calc(hdu, JOB_ID):
    wcs = WCS(hdu.header)
    pixel_scales_deg = proj_plane_pixel_scales(wcs)
    pixel_scales_arcsec = pixel_scales_deg * 3600 
    mean_pixel_scale_arcsec = np.mean(pixel_scales_arcsec)

    ANNOTATION_URL = f"http://nova.astrometry.net/api/jobs/{JOB_ID}/annotations/"
    print(ANNOTATION_URL)

    response = requests.get(ANNOTATION_URL, timeout=10)
    print(response.status_code)  # Should be 200

    data = response.json()
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
        if name[0] != '': 
            print(f"Querying Gaia for star {name[0]}...")
            star_id = name[0].split(" ")[1]      
            print(star_id)
            if name[0].startswith('HD '):
                from astroquery.simbad import Simbad
                try:
                    result = Simbad.query_object(name[0])
                    if result is None:
                        print(f"Simbad could not resolve {name[0]}")
                        continue
                    ra = result["RA"][0]
                    dec = result["DEC"][0]
                    coord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
                    gaia_result = Gaia.query_object_async(coordinate=coord, radius=5*u.arcsec)
                    results = gaia_result
                except Exception as e:
                    print(f"Error resolving {name[0]}: {e}")
                    continue
            elif name[0].startswith('TYC '):
                # Tycho-2 star query
                gaia_query = f"""
                SELECT g.ra, g.dec 
                FROM gaiadr3.gaia_source AS g
                JOIN gaiadr3.tycho2tdsc_merge_best_neighbour AS t
                ON g.source_id = t.source_id
                WHERE t.original_ext_source_id = '{star_id}'
                """
                job = Gaia.launch_job(gaia_query)
                results = job.get_results()
            else:
                print(f"Unknown star catalog for {name[0]}")
                continue
            
            print('Results are:',results)
            print(len(results))
            if len(results) > 0:
                gaia_ra, gaia_dec = results["ra"][0], results["dec"][0]
                print(f"Gaia coordinates for {name[0]}: RA = {gaia_ra}, DEC = {gaia_dec}")
                gaia_coord = SkyCoord(ra=gaia_ra * u.deg, dec=gaia_dec * u.deg, frame="icrs")
                x_gaia, y_gaia = wcs.wcs_world2pix(gaia_coord.ra.deg, gaia_coord.dec.deg, 0)               
                x_gaia = float(x_gaia)
                y_gaia = float(y_gaia)
                x = float(x)
                y = float(y)
                delta_x = x - x_gaia  
                delta_y = y - y_gaia
                residual_pix = np.sqrt(delta_x**2 + delta_y**2)
                residual_arcsec = residual_pix * mean_pixel_scale_arcsec
                residuals.append(residual_arcsec)

    for i, res in enumerate(residuals):
       print(f"Star {i+1}: Residual = {res:.5f} arcsec")
    
    if residuals:
        rms_residual = np.sqrt(np.mean(np.array(residuals)**2))
        if abs(rms_residual) > 10: 
            rms_residual = np.nan
    else:
        rms_residual = np.nan
        
    return rms_residual