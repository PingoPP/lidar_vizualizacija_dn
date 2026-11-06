'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 6.11.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - odprtost oz. Openness s pomočjo metode RVT (v nadaljevanju bom uporabil besedo 'opns')
    - v tej kodi bosta definirani positive in negative opns
That algorithm was made for visualisation tecnique - Openness by a method RVT (in continute, I will use word 'opns')
    - in this code will be defined positive and negative opns

Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.vis
import rvt.default
import numpy as np
from pathlib import Path
import glob 
from datetime import datetime



input_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga")
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\Openness-RVT\output_data")
output_dir.mkdir(parents=True, exist_ok=True)

files = glob.glob('*.tiff' or '*.tif',
                  root_dir=input_dir,
                  recursive=True)

files = [f for f in file if '.tiff_checkpoint' not in f]
print(f'Files: {file}')


def opennes():
    data_dict = rvt.default.get_raster_arr(str(input_dir))
    arr = np.asanyarray(data_dict['array'], dtype=np.float32)

    if arr.ndim == 3:
        if arr.shape[0] == 1:
            arr = arr[0]
        elif arr.shape[-1] == 1:
            arr = arr[:,:, 0]
        else: 
            arr=arr[0]

    dem = arr.astype(np.float32)
        
    resolution = data_dict['resolution']
    resolution_x = resolution[0]
    no_data=np.nan

    print(f'arr{dem}')
    print(f'arr.ndim= {dem.ndim}')

    if dem.ndim != 2:
        raise ValueError(f'Input must be 2D, but got {dem.ndim}')


    opns_arr = rvt.vis.sky_view_factor(
        dem=arr,
        resolution=resolution_x,
        compute_svf=False,
        compute_opns=True,
        compute_asvf=False,
        svf_noise=0,
        svf_n_dir=16,
        svf_r_max=10,
        ve_factor=1,
        no_data=no_data
    )

    opns = opns_arr['opns'].astype(np.float32)

#NEG OPNS 
    #Če želiš definiriati oz. uporabiti Negative OPNS moraš positivie zbrisati in ohraniti samo ta del postopka
    #If you want define or use Negative OPNS, you must positive OPNS delete and saving just that part
    neg_arr = -arr
    if no_data is not None is not np.isnan(no_data):
        neg_arr[arr == no_data] = no_data
    neg_opns = opns_arr['opns']
    
    output = rvt.default.save_raster(
        src_raster_path=str(input_dir),
        out_raster_path=str(output_dir),
        out_raster_arr=opns,  # za negative opns moraš spremeniti v neg_opns! // for negative opns you need change to neg_opns!
        no_data=np.nan
    )

    if output.exists():
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = output.with_stem(f'{output.stem}_{stamp}') 

    return output

for tif in input_dir.rglob('*.tiff' or '*.tif'):
    out = output_dir / f'{tif.stem}_opns.tiff'  # Priporočam, da zraven dodaš še neg_, da se lažje znajdeš v datoteki // I recommend, you added neg_, for easier organization in your data saving
    print(f'Processing: {opns_run(tif, output_data=out)}')
    break
    
