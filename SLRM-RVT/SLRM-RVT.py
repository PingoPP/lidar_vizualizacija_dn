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
import glob
#from osgeo import gdal
#import os

#---------------------------------------------------------------
# INPUT in OUTPUT
#---------------------------------------------------------------

input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga")
out_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM-RVT\output-data")
out_dir.mkdir(parents=True, exist_ok=True)

#---------------------------------------------------------------
# INPUT tiff DATA 
#---------------------------------------------------------------

#image_tiff = []

#for i in glob.glob(os.path.join(input_dir, '*.tiff')):
#    im = gdal.Open(os.path.join(input_dir, i))
#    image_tiff.append(i)

#print(i)

files = glob.glob('*.tiff' or '*.tif' or '*.TIFF' or '*.TIF',
                  root_dir=input_dir,
                  recursive=True)
files=[f for f in files if '.tiff_checkpoints' not in f]
print(files)

#---------------------------------------------------------------
# SLRM 
#---------------------------------------------------------------

def run_slrm(input_path, 
             output_path, 
             radius_cell=20, 
             ve_factor=1
            ):
    
    data_dict = rvt.default.get_raster_arr(str(input_path))
    dem = np.asarray(data_dict['array'], dtype = np.float64)
    no_data = data_dict['no_data']

    if dem.ndim != 2: 
        raise Exception('dem.ndim need be 2D!')
    if no_data is not None and not np.isnan(no_data):
        dem[dem == no_data] = np.nan
    if dem.shape[0] <= 2 * radius_cell or dem.shape[1] <= 2 * radius_cell:
        raise ValueError(f'dem.shape: {dem.shape} is too few for radius cell: {radius_cell}')
    if radius_cell < 1:
        raise Exception('Radius_cell need be positive (same or more than 1)')
    if not (10000 >= ve_factor >= -10000):
        raise Exception('Ve_factor need be between 10000 and -10000')

    
    slrm_arr = rvt.vis.slrm(dem=dem,
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

for tif in input_dir.glob('*.tif*' or '*.tiff' or '*.TIF' or '*.TIFF'):
    out = out_dir / f'{tif.stem}_slrm_r20_rvt.tiff'
    print('Shranjeno:', run_slrm(tif, out, radius_cell=20))
