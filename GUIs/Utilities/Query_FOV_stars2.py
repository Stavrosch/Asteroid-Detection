from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u

def Query_FOV_stars2(RA_deg, DEC_deg, width, height,query_length, mag_column="phot_g_mean_mag"):
    Gaia.MAIN_GAIA_TABLE = "gaiaedr3.gaia_source"
    Gaia_ROW_LIMIT = query_length 
    #print('hi')
    coord = SkyCoord(ra=RA_deg, dec=DEC_deg, unit='deg', frame='icrs')
    width = u.Quantity(width, u.deg)
    height = u.Quantity(height, u.deg)
    
    # Constructing the SQL query to order by magnitude
    query = f"""
    SELECT *
    FROM gaiaedr3.gaia_source
    WHERE 1=CONTAINS(
        POINT('ICRS', gaiaedr3.gaia_source.ra, gaiaedr3.gaia_source.dec),
        BOX('ICRS', {RA_deg}, {DEC_deg}, {width.to_value(u.deg)}, {height.to_value(u.deg)})
    )
    ORDER BY {mag_column} ASC
    """


    job = Gaia.launch_job_async(query=query)
    results = job.get_results()
    #print('hi')
    print(f"Number of stars in FOV: {len(results)}")
    #print('mag_column:', results["phot_g_mean_mag"][0])
    return results

if __name__== "__main__" :
    width = 1.039723522973369
    height = 0.6498380685581704
    RA=312.74583333333334
    Deg=-5.170833333333333
    r=Query_FOV_stars2(RA,Deg,width,height)   
    print(r) 