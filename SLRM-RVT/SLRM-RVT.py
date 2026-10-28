'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 28.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Simple Local Relief Model s pomočjo RVT oz. Relief Visualization Toolbox (v nadaljevanju bom uporabil besedo 'SLRM')
That algorithm was made for visualisation tecnique - Simple Local Relief Model with the help by RVT or Relief Visualization Toolbox (in continute, I will use word 'SLRM')

Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.vis
import rvt.default
from pathlib import Path
import numpy as np
from datetime import datetime
from scipy.ndimage import gaussian_filter 

#---------------------------------------------------------------
# INPUT in OUTPUT
#---------------------------------------------------------------

input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\3d_data\output")
out_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM-RVT\output-data")
out_dir.mkdir(parents=True, exist_ok=True)

#---------------------------------------------------------------
# SLRM in zrihti da bo brez tega gaussian filter in z gaussian filter
#Exception: dem.ndim need be 2D!
#---------------------------------------------------------------

def run_slrm(input_path, output_path, radius_cell=20, ve_factor=1):
    data_dict = rvt.default.get_raster_arr(str(input_path))
    dem = data_dict['array'].astype('float64')
    no_data = data_dict['no_data']

    dem[dem == no_data] = np.nan
    mean_value = np.nanmean(dem)
    dem[np.isnan(dem)] = mean_value
    twod = gaussian_filter(dem, float(radius_cell))


    if dem.ndim != 2: 
        raise Exception('dem.ndim need be 2D!')
    if radius_cell < 10 or radius_cell > 50:
        raise Exception('Radius_cell need be between 10 and 50')
    if not (10000 >= ve_factor >= -10000):
        raise Exception('Ve_factor need be between 1000 and -1000')
    
    slrm_arr = rvt.vis.slrm(dem=twod,
                            radius_cell=radius_cell,
                            ve_factor=ve_factor,
                            no_data=no_data)

 

    if output_path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = output_path.with_name(f"{output_path.stem}_{stamp}{output_path.suffix}")

    rvt.default.save_raster(
        src_raster_path=str(input_path),
        out_raster_path=str(output_path),
        out_raster_arr=slrm_arr.astype(np.float32),
        no_data=np.nan
    )
    return output_path

#---------------------------------------------------------------
# ZANKA ZA SHRANJEVANJE 
#---------------------------------------------------------------

for tif in input_dir.glob('*.tif*'):
    out = out_dir / f'{tif.stem}_slrm_r20.tiff'
    print('Shranjeno:', run_slrm(tif, out, radius_cell=20))
