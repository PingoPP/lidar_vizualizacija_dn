'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 9.11.2026

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
from datetime import datetime
import glob

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

input_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga')
output_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM\output-data')
output_dir.mkdir(parents=True, exist_ok=True)

files = glob.glob('*.tiff',
                  root_dir=input_dir,
                  recursive=True)
files=[f for f in files if '.tiff_checkpoints' not in f]

input_files = input_dir / files[0]

with rio.open(input_files) as src:
    data_arr = src.read(1).astype(np.float64)
    data_no_data = src.nodata
    profile = src.profile
    ext = [
        src.bounds.left,
        src.bounds.right,
        src.bounds.bottom,
        src.bounds.top
    ]

dict_array = {
    'profile': profile
}

#-----------------------------------------------------------------------------------------------------------------------------------
#CUMULATIVE MIN in MAX
#-----------------------------------------------------------------------------------------------------------------------------------

def cumulative_min_max(band, min_per=2, max_per=98, zero=False):
    mask = np.isfinite(band)
    if zero:
        mask &=(band != 0)
    valid = band[mask]
    a_min = np.nanpercentile(valid, min_per)
    a_max = np.nanpercentile(valid, max_per)
    return min, max

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

def slrm (dem=data_arr, 
        radius_cell=20, 
        ve_factor=1,
        no_data=None
    ):

    if np.ndim(dem) == 3: 
        if dem.shape[0] == 1:
            dem[0]
        elif dem.shape[-1] == 1: 
            dem[:, :, 0]
        else: 
            dem[0]

    dem = np.array(dem, dtype='float32')
    print(dem)

    if np.ndim(dem) !=2:
        raise Exception('mora biti 2d np.array')
    if radius_cell < 10 or radius_cell > 50:
        raise Exception('Radij mora biti v določenem intervalu')
    if not (10000 >= ve_factor >= -10000):
        raise Exception('ve_factor mora biti med 10000 in -10000')

    dem = dem.astype(np.float64, copy=True)
    if no_data is not None and np.isnan(no_data):
        dem[dem == no_data] = np.nan
    
    dem = np.clip(dem)
    dem *= ve_factor
    slrm_out = dem - mediana_filter(dem, radius_cell)
    print (type(slrm_out))
    return slrm_out

print(np.array(slrm))

#-----------------------------------------------------------------------------------------------------------------------------------
# SHRANJEVANJE
#-----------------------------------------------------------------------------------------------------------------------------------


def rasterio_save(arr, profile, output_dir, nodata=None):
    profile=profile.copy()
    count = 1 if arr.ndim == 2 else arr.shape[0]
    profile.update(count=count, dytpe=arr.dtype, nodata=nodata)

    with rio.open(output_dir, 'w', **profile) as dst:
        if arr.ndim == 2:
            dst.write(arr, 1)
        else:
            dst.write(1) 


for tif in input_dir.glob('*.tiff'):
    stamp = datetime.now().strftime('%Y%m%d_%H%M') 
    out = output_dir / f'{tif.stem}_slrm_median_{stamp}.tiff'
    out_raw = output_dir / f'{tif.stem}_raw_slrm.tiff'
            
    with rio.open(tif) as src:
        dem = src.read(1).astype(np.float32)
        file_nodata=src.nodata
        profile=src.profile.copy()
    dem [dem == -9999] = np.nan
    if file_nodata is not None and not np.isnan(file_nodata):
      dem [dem == file_nodata] = np.nan
      
    result = slrm(dem, radius_cell=20, ve_factor=1, no_data=file_nodata)

    a_min, a_max = cumulative_min_max(result, min_per=2, max_per=98)
    clipped = np.clip(result, a_min, a_max)
    norm = (clipped - a_min) / (a_max - a_min)

    rasterio_save(norm.astype(np.float32), profile, out, nodata=np.nan)
    print('shranjeno', out)

    rasterio_save(result.astype(np.float32), profile, out_raw, nodata=np.nan)
    print('shranjeno', out_raw)
    break

#slrm_saving = slrm(
#    dem=data_arr,
#    radius_cell=20,
#    ve_factor=1,
#    output_data=output_data,
#    save_float=True,
#    no_data=data_no_data
#)

#slrm_arr = slrm(data_arr, radius_cell=20, ve_factor=1, no_data=data_no_data)

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

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
