from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.wcs import WCS
from astroquery.gaia import Gaia

def Query_FOV_stars(RA_deg,DEC_deg,width,height):
    Gaia.MAIN_GAIA_TABLE = "gaiaedr3.gaia_source"
    Gaia.ROW_LIMIT = 1000

    coord = SkyCoord(ra=RA_deg, dec=DEC_deg, unit='deg', frame='icrs')
    width = u.Quantity(width, u.deg)
    height = u.Quantity(height, u.deg)
    print(coord)
    r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
    return r

if __name__== "__main__" :
    width = 1.039723522973369
    height = 0.6498380685581704
    RA=312.74583333333334
    Deg=-5.170833333333333
    r=Query_FOV_stars(RA,Deg,width,height)  
    print(r) 
