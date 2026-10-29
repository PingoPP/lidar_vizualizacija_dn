'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 29.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Simple Local Relief Model (v nadaljevanju bom uporabil besedo 'SLRM')
That algorithm was made for visualisation tecnique - Simple Local Relief Model (in continute, I will use word 'SLRM')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

#import os 
from pathlib import Path
import numpy as np
import rasterio as rio 
from scipy.ndimage import median_filter, distance_transform_edt
import glob 
from datetime import datetime

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga")
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM\output-data")
output_dir.mkdir(parents=True, exist_ok=True)

files = glob.glob('*.tif' or '*.tiff' or '*.TIF' or '*.TIFF',
                 root_dir=input_dir,
                 recursive=True)
files=[f for f in files if '.tiff_checkpoints' not in f]
print(files)

#-----------------------------------------------------------------------------------------------------------------------------------
#Dodaj še min, max cumulative
#Zaenkrat še ni potrebe!
#-----------------------------------------------------------------------------------------------------------------------------------

#def cumulative_count_cut(band, c_min=2.0, c_max=98.0):
#    min_val = np.nanpercentile(band, c_min),
#    max_val = np.nanpercentile(band, c_max)
#    return min_val, max_val

#-----------------------------------------------------------------------------------------------------------------------------------
#MEDIAN FILTER
#-----------------------------------------------------------------------------------------------------------------------------------

def mediana_filter(dem, radius_cell):
    nan_mask = np.isnan(dem)
    if nan_mask.any():
        idx = distance_transform_edt(nan_mask, return_distances=False, return_indices=True)
        dem = dem[tuple(idx)]          
    out = median_filter(dem, size=2 * radius_cell + 1, mode='nearest')
    out[nan_mask] = np.nan     

    return out

#-----------------------------------------------------------------------------------------------------------------------------------
#SLRM
#-----------------------------------------------------------------------------------------------------------------------------------


def slrm(
        dem, 
        radius_cell=20, 
        ve_factor=1, 
        no_data=None
        ):
    
    if dem.ndim != 2:
        raise ValueError("dem must be a 2D array")
    if radius_cell < 1:
        raise ValueError("radius_cell must be positive")
    if dem.shape[0] <= 2 * radius_cell or dem.shape[1] <= 2 * radius_cell:
        raise ValueError(f"DEM shape {dem.shape} is too small for radius_cell {radius_cell}")
    if not -10000 <= ve_factor <= 10000:
        raise ValueError("ve_factor must be between -10000 and 10000")

    dem = dem.astype(np.float64, copy=True)
    if no_data is not None and not np.isnan(no_data):
        dem[dem == no_data] = np.nan

    dem *= ve_factor

    return dem - mediana_filter(dem, radius_cell)


raster_paths = [
    path for path in input_dir.rglob("*")
    if path.is_file() and path.suffix.lower() in {".tif" or ".tiff" or '.TIF' or '.TIFF'}
    and ".tiff_checkpoints" not in str(path)
]

for tif in raster_paths:
    with rio.open(tif) as src:
        dem = src.read(1)
        profile = src.profile.copy()
        no_data = src.nodata

    slrm_out = slrm(dem, radius_cell=20, ve_factor=1, no_data=no_data)

    output_path = output_dir / f"{tif.stem}_slrm_median_r20.tif"
    profile.update(dtype="float32", count=1, nodata=np.nan)

    if output_path.exists():
        stamp = datetime.now().strftime('%Y%m%d_%H%M')
        output_path = output_path.with_name(f'{output_path.stem}_{stamp}{output_path.suffix}')

    with rio.open(output_path, "w", **profile) as dst:
        dst.write(slrm_out.astype(np.float32), 1)

    print("Shranjeno:", output_path)
    break

#slrm_arr = slrm(data_arr, radius_cell=20, ve_factor=1, no_data=data_no_data)

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

for tif in input_dir.glob('*.tif' or '*.tiff' or '*.TIF' or '*.TIFF'):
    out = output_dir / f'{tif.stem}_slrm_median_r20.tiff' 
    print('Shranjeno:', slrm(tif, out, radius_cell=20))


#rvt.default.save_raster(
#    src_raster_path=str(input_data),
#    out_raster_path=str(output_data),
#    out_raster_arr=slrm_arr.astype(np.float32),
#    no_data=np.nan
#)
    

#-----------------------------------------------------------------------------------------------------------------------------------
#HITER PRIKAZ SLMR-ja Z MATPLOTLIB-om
#-----------------------------------------------------------------------------------------------------------------------------------

#lo, hi = np.nanpercentile(slrm_arr, [2, 98])
#fig, ax = plt.subplots(figsize=(10, 10))
#ax.imshow(slrm_arr, extent=ext, cmap='gray', vmin=lo, vmax=hi)
#ax.set_title('SLRM by RVT')
#plt.show()
