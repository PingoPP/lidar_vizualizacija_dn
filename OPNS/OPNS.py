'''
Avtor / Author: Jaka Dacar
Nazadnje spremenjeno / Last changed: 14.11.2026
Testirano / tested: NAN

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Openness (v nadaljevanju bom uporabil besedo 'OPNS')
That algorithm was made for visualisation tecnique - Openness (in continute, I will use word 'OPNS')


Algoritem je bil ustvarjen v sklopu diplomske naloge
Algorithm was made as part of bachelor thesis
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
        radius_max: int = 10,                #L_max [v dnevniku]
        radius_min: int = 1,                 #L_min [v dnevniku]
        n_directions: int = 8,               #D [v dnevniku]
):

    pad = int(np.ceil(radius_max))
    height = np.pad(dem, pad, mode='edge')   # če edge da nezaželen rezultat, probaj 'reflect'

    azimuths_deg = np.linspace(0, 360, n_directions, endpoints=False)
    azimuths_rad = np.radians(azimuths_deg)

    rad = np.arrange(radius_min, radius_max + 1)
    for az_rad in azimuths_rad:
        dx = np.sin(az_rad)
        dy = -np.cos(az_rad)

    for r in radi:
        x = int(np.round(r * dx))
        y = int(np.round(r * dy))

#---------------------------------------------
#---------------------------------------------

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
    dem = dem / resolution
    rad_min = max(np.round(radius_max * radius_min), 1)
    rad_max = max(np.round(radius_max * radius_min), 10)

    dict_opns = opns_comp(
        dem=dem,
        radius_max=int(rad_max),
        radius_min=int(rad_min),
        n_directions=n_directions,
    )

    for dem in dict_opns.values():
        dem[no_data] = np.nan

    return dict_opns


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
    out = output_dir / f"{tif.stem}_opns_{stamp}.tiff"

    with rio.open(tif) as src:
        dem = src.read(1).astype(np.float32)
        no_data = src.nodata
        profile = src.profile.copy()

    dem[dem == -9999] = np.nan
    if no_data is not None and not np.isnan(no_data):
        dem[dem == no_data] = np.nan

    results = opns(
        dem,
        resolution=0.5,
        radius_min=1,
        radius_max=10,
        n_directions=8,
        no_data=no_data
    )

    dem_opns = results.astype(np.float32)
    rasterio_save(dem_opns, profile, out, no_data=np.nan)
    print("shranjeno", out)
    break  
