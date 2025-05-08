from astroquery.jplhorizons import Horizons
from astropy.time import Time
from astropy.io import fits
from astropy.coordinates import EarthLocation
import astropy.units as u

def get_apparent_mag(PATH):
    # Define the asteroid and observer details
    id = PATH[len(PATH)-22:len(PATH)-19]
    #print(id)
    asteroid_id = id 
    #location = EarthLocation(lat=40.5624 * u.deg, lon=22.9956 * u.deg, height=68 * u.m)
    location = EarthLocation(lat='34.932056', lon='32.840167', height=1411 * u.m)
    # Convert EarthLocation to the format required by Horizons: 'lat lon elev'
    location_str = f"{location.lat.value} {location.lon.value} {location.height.to(u.m).value}"

    # Open the FITS file and extract the observation time
    hdul = fits.open(PATH)
    header = hdul[0].header
    hdul.close()
    
    # Extract the observation time (assuming ISO format)
    date_avg = header['DATE-AVG']
    
    # Parse the ISO format date
    observation_time = Time(date_avg, format='isot')
    
    # Query JPL Horizons
    obj = Horizons(id=asteroid_id, location=location_str, epochs=observation_time.mjd)
    eph = obj.ephemerides()
    print(eph)
    # Extract apparent magnitude
    apparent_mag = eph['V'][0]  # V-band magnitude
    print(f"Apparent Magnitude of Asteroid {asteroid_id} at {observation_time.iso}: {apparent_mag}")

    return apparent_mag