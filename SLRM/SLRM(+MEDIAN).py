'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 8.11.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Simple Local Relief Model (v nadaljevanju bom uporabil besedo 'SLRM')
That algorithm was made for visualisation tecnique - Simple Local Relief Model (in continute, I will use word 'SLRM')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import os 
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
#Dodaj še min, max cumulative
#-----------------------------------------------------------------------------------------------------------------------------------

def cumulative_min_max(band, min_per=2, max_per=98):
    new_band= band[band !=0]
    min = np.nanpercentile(new_band, min_per)
    max = np.nanpercentile(new_band, max_per)
    return min, max

#-----------------------------------------------------------------------------------------------------------------------------------
#SAVE_PATH_FLOAT in RASTERIO_SAVE - funkcija za shranjevanje 
#-----------------------------------------------------------------------------------------------------------------------------------

def save_path_float(save_path):
    base, ext = os.path.splitext(str(save_path))
    return f'{base}_float{ext}'

def rasterio_save(arr, profile, output_data, nodata=None):
    profile=profile.copy()
    count = 1 if arr.ndim == 2 else arr.shape[0]
    profile.update(count=count, dytpe=arr.dtype, nodata=nodata)
    with rio.open(output_data, 'w', **profile) as dst:
        if arr.ndim == 2:
            dst.write(arr, 1)
        else:
            dst.write(1) 

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
        output_data=None,
        save_float=False, 
        no_data=None
):

    if np.ndim(dem) == 3: 
        if dem.shape[0] == 1:
            arr = dem[0]
        elif dem.shape[-1] == 1: 
            arr = arr[:,:, 0]
        else: 
            arr = arr[0]

    dem = np.array(dem, dtype='float32')

    if np.ndim(dem) !=2:
        raise Exception('mora biti 2d np.array')
    if radius_cell < 10 or radius_cell > 50:
        raise Exception('Radij mora biti v določenem intervalu')
    if not (10000 >= ve_factor >= -10000):
        raise Exception('ve_factor mora biti med 10000 in -10000')

    dem = dem.astype(np.float64, copy=True)
    if no_data is not None:
        dem[dem == no_data] = np.nan

    
    dem = np.clip(dem)
    dem *= ve_factor
    slrm_out = dem - mediana_filter(dem, radius_cell)

    if slrm_out.exsist():
        stamp = datetime.now().strftime('%Y%m%d_%H%M') 
        slrm_path = slrm_out.with_name(f'{slrm_out.stem}_{stamp}{slrm_out.suffix}')
    
    
    out_profile = dict_array['profile'].copy()

    if save_float:
        rasterio_save(
            slrm_out,
            out_profile,
            output_data=save_path_float(output_data),
            nodata=np.nan
        )



    return slrm_path

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

for tif in input_dir.rglob('*.tiff'):
    out = output_dir / f'{tif.stem}_slrm_median.tiff'
    print('Shranjeno:', slrm(dem=data_arr, output_data=out))


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
