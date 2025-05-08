from astroquery.gaia import Gaia

def gaia_query():
    residuals = []
    star_positions = [(['Tycho-2 2453-1599-1'], 1325.5195004975303, 759.7476653927449)]
    for name, x, y in star_positions:
        if len(residuals) == 10:
            break
        if name[0]!='': 
            name[0]='Tycho-2 2453-1599-1'
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

gaia_query()