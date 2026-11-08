'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 8.11.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Sky View Factor s pomočjo metode RVT (v nadaljevanju bom uporabil besedo 'svf')
    - v tej kodi bosta definirani positive in negative opns
That algorithm was made for visualisation tecnique - Sky View Factor by a method RVT (in continute, I will use word 'svf')
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
#import rasterio as rio

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT 
#-----------------------------------------------------------------------------------------------------------------------------------

input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga")
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\Openness-RVT\output_data")
output_dir.mkdir(parents=True, exist_ok=True)

file = glob.glob('*.tiff' or '*.tif',
                 root_dir=input_dir,
                 recursive=True)
file = [f for f in file if '.tiff_checkpoint' not in f]
print(f'Files: {file}')

#-----------------------------------------------------------------------------------------------------------------------------------
#SKY VIEW FACTOR  
#-----------------------------------------------------------------------------------------------------------------------------------

def svf_run(input_data: Path, 
             output_data: Path,
             ve_factor=1.0,
             r_max=10,
             svf_n_dir=16,
             noise=0,
            ):

    data_dict = rvt.default.get_raster_arr(str(input_data))
    arr = np.asarray(data_dict['array'], dtype=np.float32)    

    if arr.ndim == 3:
        if arr.shape[0] == 1:
            arr = arr[0]
        elif arr.shape[-1] == 1:
            arr=arr[:,:,0]
        else: 
            arr=arr[0]

    dem = arr.astype(np.float32)

    no_data = data_dict['no_data']
    resolution = data_dict['resolution']
    resolution_x = resolution[0]
    #resolution_y = resolution[1]

    #with rio.open(input_data) as src:
    #    profile = src.profile
    #    raster_2d = src.read(1)
    #    no_data=src.nodata
        #resolution_x = abs(src.transform.a)
        #resolution_y = abs(src.transform.e)


    #if not np.isclose(resolution_x, resolution_y):
    #    raise ValueError('RVT need a single raster resolution')

    if dem.ndim != 2:
        raise ValueError(f'Input must be 2D, but got {dem.ndim}')
    if not (10000 >= ve_factor >= -10000):
        raise ValueError(f'Input ve_factor must be between -10000 and 10000, but got {ve_factor}.')
    
    svf_arr = rvt.vis.sky_view_factor(
        dem=dem,
        resolution=resolution_x,
        compute_svf=True,
        compute_opns=False,
        compute_asvf=False,
        svf_noise=noise,
        svf_n_dir=svf_n_dir,
        svf_r_max=r_max,
        ve_factor=ve_factor,
        no_data=no_data
    )

    svf = svf_arr['svf'].astype(np.float32)

    if output_data.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_data = output_data.with_stem(f'{output_data.stem}_{stamp}')

    rvt.default.save_raster(
        src_raster_path=str(input_data),
        out_raster_path=str(output_data),
        out_raster_arr=svf,
        no_data=np.nan
    )

    return output_data


    #profile.update(
    #    driver='GTiff',
    #    dtype='float32',
    #    count=1,
    #    compress='lzw',
    #    nodata=no_data
    #)

  
    #with rio.open(output_data, 'w', **profile) as dst:
    #    dst.write(result, 1)
    #
    #return output_data

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

for tif in input_dir.rglob('*.tiff' or '*.tif'):
    out = output_dir / f'{tif.stem}_svf.tiff'
    print(f'Processing: {svf_run(tif, output_data=out)}')
    break




    
