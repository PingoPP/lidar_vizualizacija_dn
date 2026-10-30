'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 30.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - senčenja oz. hillshade s pomočjo RVT oz. Relief Visualization Toolbox (v nadaljevanju bom uporabil besedo 'hillshade')
That algorithm was made for visualisation tecnique - hillshade with the help by RVT or Relief Visualization Toolbox (in continute, I will use word 'hillshade')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.vis
import rvt.default
import numpy as np
from pathlib import Path
#import rasterio as rio
#import matplotlib.pyplot as plt 
import glob 
from datetime import datetime


#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

#vhod pot podatka, za katero imaš namen uporabiti za hillshade. Datoteka mora biti nujno shranjena pod .tiff ali .tif
input_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga')

#izhod podatkov, kjer se bo shranila v prostoru, kjer je definiran pot. Datoteka, naj se shrani pod .tiff (bolj priročno) ali .tif 
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\Hillshade-RVT\output_data")
output_dir.mkdir(parents=True, exist_ok=True)

files = glob.glob('*.tiff' or '*.tif',
                  root_dir=input_dir,
                  recursive=True)
files = [f for f in files if '.tiff_checkpoints' not in f]
print(files)



#-----------------------------------------------------------------------------------------------------------------------------------
#HILLSHADE
#-----------------------------------------------------------------------------------------------------------------------------------

# Uporaba metode hillshade z osnovnimi nastavitvami. Čeprav sta parametra
# slope in aspect nastavljena na None, to ne pomeni, da se ne uporabljata.
# Ravno nasprotno: funkcija ju izračuna sama, in sicer z osnovno formulo.
def run_hs(
        input_path,
        out_path
    ):

    data_dict = rvt.default.get_raster_arr(str(input_path))
    dem = np.asarray(data_dict['array'], dtype=np.float64)
    data_no_data = data_dict['no_data']
    resolution = data_dict['resolution']
    resolution_x = resolution[0]
    resolution_y = resolution[1]

    hs_arr = rvt.vis.hillshade(
            dem=dem,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
            sun_azimuth=215,
            sun_elevation=35,
            ve_factor=1,
            slope=None,
            aspect=None,
            no_data=data_no_data
        )

    if out_path.exists():
        stamp = datetime.now().strftime('%Y%m%d_%H%M')
        out_path = out_path.with_name(f'{out_path.stem}_{stamp}{out_path.suffix}')

    rvt.default.save_raster(
        src_raster_path = str(input_path),
        out_raster_path = str(out_path),
        out_raster_arr = hs_arr.astype(np.float64),
        no_data=np.nan
    )

    return out_path

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

for tif in input_dir.glob('*.tiff'):
    out = output_dir / f'{tif.stem}_hillshade.tiff'
    print(f'Shranjeno: {run_hs(tif, out)}')



#-----------------------------------------------------------------------------------------------------------------------------------
#HITER PRIKAZ HILLSHADE-ja z MATPLOTLIB-om
#-----------------------------------------------------------------------------------------------------------------------------------

#fig, ax = plt.subplots(figsize=(5, 5))
#im = ax.imshow(hs, cmap='gray', extent=ext),
#ax.set_title('Hillshade by RVT')
#plt.show()
