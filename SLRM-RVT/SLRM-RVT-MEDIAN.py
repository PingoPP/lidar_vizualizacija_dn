'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 26.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Simple Local Relief Model s pomočjo RVT oz. Relief Visualization Toolbox (v nadaljevanju bom uporabil besedo 'SLRM')
That algorithm was made for visualisation tecnique - Simple Local Relief Model with the help by RVT or Relief Visualization Toolbox (in continute, I will use word 'SLRM')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.default
from pathlib import Path
import numpy as np
import rasterio as rio 
import matplotlib.pyplot as plt 
from scipy.ndimage import median_filter, distance_transform_edt

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

input_data = Path(r"C:\Users\jakad\OneDrive\Desktop\3d_data\output\Pivola_klasificirano_in_rastirano.tiff")
output_data = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM-RVT\output-data\SLRM_5.tiff")

with rio.open(input_data) as src:
    data_arr = src.read(1).astype(np.float64)
    data_no_data = src.nodata
    profile = src.profile
    ext = [
        src.bounds.left,
        src.bounds.right, 
        src.bounds.bottom, 
        src.bounds.top
    ]

#-----------------------------------------------------------------------------------------------------------------------------------
#TEMNENJE in / ali SVETLJENJE 
#-----------------------------------------------------------------------------------------------------------------------------------

#definiraj še zraven, ker ne dela 

def cumulative_count_cut(band, min_percentile=2, max_percentile=98):
    min_val = np.nanpercentile(band, min_percentile)
    max_val = np.nanpercentile(band, max_percentile)

    return min_val, max_val

#-----------------------------------------------------------------------------------------------------------------------------------
#MEDIAN FILTER
#-----------------------------------------------------------------------------------------------------------------------------------

#tole še preglej 

def mediana_filter(dem, radius_cell):
    nan_mask = np.isnan(dem)
    if nan_mask.any():
        idx = distance_transform_edt(nan_mask, return_distances=False, return_indices=True)
        dem = dem[tuple(idx)]          
    out = median_filter(dem, size=2 * radius_cell + 1, mode="nearest")
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

#tole še malo popravi

    if dem.ndim !=2:
        raise Exception('mora biti 2d np.array')
    if radius_cell < 10 or radius_cell > 50:
        raise Exception('Radij mora biti v določenem intervalu')
    if not (10000 >= ve_factor >= -10000):
        raise Exception('ve_factor mora biti med 10000 in -10000')

    dem = dem.astype(np.float64, copy=True)
    if no_data is not None:
        dem[dem == no_data] = np.nan

    low, high = cumulative_count_cut(dem)
    dem = np.clip(dem, low, high)
    dem *= ve_factor
    slrm_out = dem - mediana_filter(dem, radius_cell)

    return slrm_out

slrm_arr = slrm(data_arr, radius_cell=20, ve_factor=1, no_data=data_no_data)

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

rvt.default.save_raster(
    src_raster_path=str(input_data),
    out_raster_path=str(output_data),
    out_raster_arr=slrm_arr.astype(np.float32),
    no_data=np.nan
)

#-----------------------------------------------------------------------------------------------------------------------------------
#HITER PRIKAZ SLMR-ja Z MATPLOTLIB-om
#-----------------------------------------------------------------------------------------------------------------------------------

lo, hi = np.nanpercentile(slrm_arr, [2, 98])
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(slrm_arr, extent=ext, cmap='gray', vmin=lo, vmax=hi)
ax.set_title('SLRM by RVT')
plt.show()
