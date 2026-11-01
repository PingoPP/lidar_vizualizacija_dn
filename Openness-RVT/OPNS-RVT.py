'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 1.11.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - odprtost oz. Openness s pomočjo metode RVT (v nadaljevanju bom uporabil besedo 'opns')
    - v tej kodi bosta definirani positive in negative opns
That algorithm was made for visualisation tecnique - Openness by a method RVT (in continute, I will use word 'opns')
    - in this code will be defined positive and negative opns

Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

from pathlib import Path
from datetime import datetime
import glob
import rvt.vis
import rvt.default
import numpy as np
import rasterio as rio

input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga")
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\Openness-RVT\output_data")
output_dir.mkdir(parents=True, exist_ok=True)

file = glob.glob('*.tiff' or '*.tif',
                 root_dir=input_dir,
                 recursive=True)
file = [f for f in file if '.tiff_checkpoint' not in f]
print(f'Files: {file}')

def opns_run(input_data, 
             output_data,
             ve_factor=1.0,
             r_max=10,
             svf_n_dir=16,
             noise=0):


    with rio.open(input_data) as src:
        profile = src.profile
        raster_2d = src.read(1)
        no_data=src.nodata
        resolution_x = abs(src.transform.a)
        resolution_y = abs(src.transform.e)

    dem = raster_2d.astype(np.float64)

    if not np.isclose(resolution_x, resolution_y):
        raise ValueError('RVT need a single raster resolution')

    if dem.ndim != 2:
        raise ValueError(f'Input raster must be 2D, but got {dem.ndim}.')
    if not (10000 >= ve_factor >= -10000):
        raise ValueError(f'Input ve_factor must be between -10000 and 10000, but got {ve_factor}.')
    
    opns = rvt.vis.sky_view_factor(
        dem=dem,
        resolution=resolution_x,
        compute_svf=False,
        compute_opns=True,
        compute_asvf=False,
        svf_noise=noise,
        svf_n_dir=svf_n_dir,
        svf_r_max=r_max,
        ve_factor=ve_factor,
        no_data=no_data
    )

    result = opns['opns'].astype(np.float64)

    if output_data.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_data = output_data.with_stem(f'{output_data.stem}_{stamp}')

    profile.update(
        driver='GTiff',
        dtype='float64',
        count=1,
        compress='lzw',
        nodata=no_data
    )

    with rio.open(output_data, 'w', **profile) as dst:
        dst.write(result, 1)

    return output_data


for tif in input_dir.rglob('*.tif' or '*.tiff'):
    out = output_dir / f'{tif.stem}_opns.tiff'
    print(f'Processing: {opns_run(tif, output_data=out)}')
    
results = opns_run(
    input_data=tif,
    output_data=out,
    ve_factor=1.0,
    r_max=10,
    svf_n_dir=16,
    noise=0
)

print(f"Saved: {results}")

if results is not None:
    print("Processing completed successfully.")
else:
    print("Processing completed with warnings or errors.")

    
