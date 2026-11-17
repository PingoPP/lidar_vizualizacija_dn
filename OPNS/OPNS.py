'''
Avtor / Author: Jaka Dacar
Nazadnje spremenjeno / Last changed: 17.11.2026
Testirano / tested: NAN

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Openness (v nadaljevanju bom uporabil besedo 'OPNS')
That algorithm was made for visualisation tecnique - Openness (in continute, I will use word 'OPNS')


Algoritem je bil ustvarjen v sklopu diplomske naloge
Algorithm was made as part of bachelor thesis

Problem: vizualizacija mi ne prikaže + min_elevatio je enako kot prikazuje dejanski max_elevation, samo, da je negativno
'''

from pathlib import Path
from datetime import datetime
import rasterio as rio
import numpy as np
import glob

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

input_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga')
output_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga\OPNS\output')
output_dir.mkdir(parents=True, exist_ok=True)

#-----------------------------------------------------------------------------------------------------------------------------------
#OPNS - computing and making dream true!
#-----------------------------------------------------------------------------------------------------------------------------------

def opns_comp(
        dem,
        cell_size: float = 0.5,       
        radius_max: int = 10,
        radius_min: int = 1,
        n_directions: int = 8
        ):

    pad = int(np.ceil(radius_max))

    #hb
    height = np.pad(dem, pad, mode='reflect')   # če edge da nezaželen rezultat, probaj 'edge'


    rows, columns = dem.shape

    #ha
    center = height[pad : pad + rows, pad :  pad + columns]

    def elevation ( radius_max: int = 10,                #L_max [v dnevniku]
                    radius_min: int = 1,                 #L_min [v dnevniku]
                    n_directions: int = 8                #D [v dnevniku]   
    ):
                                            
        #directions = {
        #N = 0,
        #NW = 45,
        #W = 90,
        #SW = 135,
        #S = 180,
        #SE = 225,
        #E = 270,
        #NE = 315
        #}
        
        azimuths_deg = np.linspace(0, 360, n_directions, endpoint=False)
        azimuths_rad = np.radians(azimuths_deg)
        radi = np.arange(radius_min, radius_max + 1)

        return azimuths_rad, radi

    azimuths_rad, radi = elevation(
        radius_max=radius_max,
        radius_min=radius_min,
        n_directions=n_directions
    )

    nadir_sum = np.zeros(dem.shape, dtype=np.float32)
    zenith_sum = np.zeros(dem.shape, dtype=np.float32)
    count = np.zeros(dem.shape, dtype=np.int32)

    for az_rad in azimuths_rad:
        dx = np.sin(az_rad)
        dy = -np.cos(az_rad)

        max_angle = np.full(dem.shape, -np.inf)    

    for r in radi:
        x = int(np.round(r * dx))
        y = int(np.round(r * dy))
        if x == 0 and y == 0:
            continue

        neighbour = height [
            pad + y : pad + y + rows,
            pad + x : pad + x + columns,
        ]

        # hor_dist = ((ia-ib)**2 + (ja-jb)**2)**2
        dist = np.hypot(x, y) * cell_size

        #theta = tan^-1((hb - ha) / hor_dist)
        angle = np.arctan2(neighbour - center, dist)
        angle_max = np.maximum(max_angle, angle)

        zenith = np.pi / 2 - angle_max #Positive
        nadir = np.pi / 2 + angle_max #Negative

        valid = np.isfinite(max_angle)
        zenith_sum += np.where(valid, zenith, 0)
        nadir_sum += np.where(valid, nadir, 0) 
        count += valid

        with np.errstate(invalid='ignore', divide='ignore'):
            pos = np.where(count > 0, zenith_sum / count, np.nan)
            neg = np.where(count > 0, nadir_sum / count, np.nan)


        return pos, neg 


def opns(
        dem,
        resolution=0.5,
        radius_min=1,
        radius_max=10,
        n_directions=8,
        ve_factor=1,
        no_data=None
        ):

    if np.ndim(dem) == 3:
        if dem.shape[0] == 1:
            dem = dem[0]
        elif dem.shape[-1] == 1:
            dem = dem[:, :, 0]
        else:
            dem = dem[0]

    dem = np.asarray(dem, dtype=np.float32)

    if dem.ndim != 2:
        raise ValueError("Input DEM must be a 2D array.")

    if no_data is not None:
        dem = dem.copy()
        dem[dem == no_data] = np.nan
    no_data = np.isnan(dem)

    dem = dem * ve_factor
    rad_min = max(int(np.round(radius_min)), 1)
    rad_max = min(int(np.round(radius_max)), 10)

    pos_opns, neg_opns = opns_comp(
        dem=dem,
        radius_max=rad_max,
        radius_min=rad_min,
        n_directions=n_directions,
        cell_size=resolution,
    )

    mask = np.isnan(dem)
    pos_opns[mask] = np.nan
    neg_opns[mask] = np.nan

    return pos_opns, neg_opns

  

#-----------------------------------------------------------------------------------------------------------------------------------
# SHRANJEVANJE
#-----------------------------------------------------------------------------------------------------------------------------------

def rasterio_save(dem, profile, output_path, no_data=None):
    profile = profile.copy()
    count = 1 
    profile.update(count=count, dtype=dem.dtype, nodata=no_data)

    with rio.open(output_path, "w", **profile) as dst:
        if dem.ndim == 2:
            dst.write(dem, 1)
        else:
            dst.write(dem)

for tif in sorted(input_dir.glob("*.tiff")):
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    out_pos = output_dir / f"{tif.stem}_pos_opns_{stamp}.tiff"
    out_neg = output_dir / f"{tif.stem}_neg_opns_{stamp}.tiff"

    with rio.open(tif) as src:
        dem = src.read(1).astype(np.float32)
        no_data = src.nodata
        profile = src.profile.copy()

    dem[dem == -9999] = np.nan
    if no_data is not None and not np.isnan(no_data):
        dem[dem == no_data] = np.nan

    array = -dem

    pos_opnss = opns(
        dem=dem,
        resolution=0.5,
        radius_min=1,
        radius_max=10,
        n_directions=8,
        no_data=no_data
    )

    neg_opnss = opns(
        dem=array,
        resolution=0.5,
        radius_min=1,
        radius_max=10,
        n_directions=8,
        no_data=no_data
        
    )

    pos_opns = pos_opnss[0].astype(np.float32)
    rasterio_save(pos_opns, profile, out_pos, no_data=np.nan)

    neg_opns = neg_opnss[0].astype(np.float32)
    rasterio_save(neg_opns, profile, out_neg, no_data=np.nan)

    print("shranjeno", out_pos, out_neg)
    break  
