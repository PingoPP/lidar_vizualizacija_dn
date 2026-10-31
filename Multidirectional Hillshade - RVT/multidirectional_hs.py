'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 31.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - večsmerno senčenje oz. Multidirect Hillshade s pomočjo RVT oz. Relief Visualization Toolbox(v nadaljevanju bom uporabil besedo 'multidirectional hillshade')
That algorithm was made for visualisation tecnique - Multidirectional hillshade with help by RVT or Relief Visualization Toolbox (in continute, I will use word 'multidirectional hillshade')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

#-----------------------------------------------------------------------------------------------------------------------------------
#OSGEO - pregled (v preteklosti sem imel, kar nekaj problemov s tem)
#-----------------------------------------------------------------------------------------------------------------------------------

from osgeo import gdal

print(gdal.__version__)
print(gdal.GetDriverByName('GTiff'))
print(gdal.GetDriverCount())
gdal.AllRegister()
print(gdal.GetDriverCount(), gdal.GetDriverByName("GTiff"))

import rvt.vis
import rvt.default
from pathlib import Path
import numpy as np
#import rasterio as rio
#import matplotlib.pyplot as plt 
import glob
from datetime import datetime

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT 
#-----------------------------------------------------------------------------------------------------------------------------------

#vhod pot podatka, za katero imaš namen uporabiti multidirectional hillshade. Datoteka mora biti nujno shranjena pod .tiff ali .tif
input_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga')

#izhod podatkov, kjer se bo shranila v prostoru, kjer je definiran pot. Datoteka, naj se shrani pod .tiff (bolj priročno) ali .tif 
output_dir = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\Multidirectional Hillshade - RVT\output_data")
output_dir.mkdir(parents=True, exist_ok=True)

files = glob.glob('*tiff' or '*tif',
                  root_dir=input_dir,
                  recursive=True)
files = [f for f in files if '.tiff.checkpoints' not in f]
print(files)

#-----------------------------------------------------------------------------------------------------------------------------------
#MULTIDIRECTIONAL HILLSHADE
#-----------------------------------------------------------------------------------------------------------------------------------

# Uporaba metode multidirectional hillshade z osnovnimi nastavitvami. Čeprav sta parametra
# slope in aspect nastavljena na None, to ne pomeni, da se ne uporabljata.
# Ravno nasprotno: funkcija ju izračuna sama, in sicer z osnovno formulo.
def mh(
    input_data,
    output_data
    ):


    data_dict = rvt.default.get_raster_arr(str(input_data))
    dem = np.asarray(data_dict['array'], dtype=np.float64)
    no_data = data_dict['no_data']
    resolution = data_dict['resolution']
    resolution_x = resolution[0]
    resolution_y = resolution[1]



    mh_run = rvt.vis.multi_hillshade(
      dem=dem,
      resolution_x=resolution_x,
      resolution_y=resolution_y,
      nr_directions=16,
      sun_elevation=35,
      slope=None,
      aspect=None,
      ve_factor=1,
      no_data=no_data

    )

    if output_data.exists():
      stamp=datetime.now().strftime('%Y%m%d_°%H%M')
      output_data = output_data.with_name(f'{output_data.stem}_{stamp}{output_data.suffix}')

    rvt.default.save_raster(
        src_raster_path=str(input_data),
        out_raster_path=str(output_data),
        out_raster_arr=mh_run.astype(np.float64),
        no_data=np.nan     
        )

    return output_data

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

for tif in input_dir.glob('*tiff' or '*tif'):
   out = output_dir / f'{tif.stem}_mhs.tiff'
   print(f'Shranjeno: {mh(tif, out)}')

#-----------------------------------------------------------------------------------------------------------------------------------
#HITER PRIKAZ MULTIDIRECTIONAL HILLSHADE-ja z MATPLOTLIB-om
#-----------------------------------------------------------------------------------------------------------------------------------

#fig, ax = plt.subplots(figsize=(10, 10))
#mhs_display = np.nanmin(mhs, axis=0)
#mhs_display = data_arr, mhs_display
#im = ax.imshow(mhs_display, extent=ext)
#ax.set_title("Multidirectional hillshade by RVT")
#plt.show()


