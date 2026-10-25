'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 25.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - senčenja oz. hillshade s pomočjo RVT oz. Relief Visualization Toolbox (v nadaljevanju bom uporabil besedo 'hillshade')
That algorithm was made for visualisation tecnique - hillshade with the help by RVT or Relief Visualization Toolbox (in continute, I will use word 'hillshade')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.vis
import numpy as np
from pathlib import Path
import rasterio as rio
import matplotlib.pyplot as plt 


#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

#vhod pot podatka, za katero imaš namen uporabiti za hillshade. Datoteka mora biti nujno shranjena pod .tiff ali .tif
input_data = Path(r"C:\Users\jakad\OneDrive\Desktop\3d_data\output\Pivola_klasificirano_in_rastirano.tiff")

#izhod podatkov, kjer se bo shranila v prostoru, kjer je definiran pot. Datoteka, naj se shrani pod .tiff (bolj priročno) ali .tif 
output_data = Path(r"C:\Users\jakad\OneDrive\Desktop\3d_data\output\Pivola_hillsajd_RVT_1.tiff")


with rio.open(input_data) as src:
    print(src.shape, src.res, src.nodata)

#uporaba vhodne date za pregled array (polja), resolucije in vpogled, kjer so prisotne NoData (lunkje) ter robove
with rio.open(input_data) as src:
    data_arr = src.read(1).astype(np.float32)
    data_no_data = src.nodata
    data_x_resolution, data_y_resolution = src.res
    profile = src.profile
    ext=[
        src.bounds.left,
         src.bounds.right,
         src.bounds.bottom,
         src.bounds.top
        ]

#-----------------------------------------------------------------------------------------------------------------------------------
#HILLSHADE
#-----------------------------------------------------------------------------------------------------------------------------------

# Uporaba metode hillshade z osnovnimi nastavitvami. Čeprav sta parametra
# slope in aspect nastavljena na None, to ne pomeni, da se ne uporabljata.
# Ravno nasprotno: funkcija ju izračuna sama, in sicer z osnovno formulo.
hs = rvt.vis.hillshade(
    dem=data_arr,
    resolution_x=data_x_resolution,
    resolution_y=data_y_resolution,
    sun_azimuth=215,
    sun_elevation=35,
    ve_factor=1,
    slope=None,
    aspect=None,
    no_data=data_no_data
)

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------


#ne dela mi GDAL okolje (neki me zajebava zadnje čase), kar pomeni, da moram preiti v rasterio
#rvt.default.save_raster(
#    src_raster_path=str(input_data),
#    out_raster_path=str(output_data),
#    out_raster_arr=hs,
#    no_data=np.nan
#)


if output_data is not None:
    if profile is None:
        AttributeError('definiraj profile')
    out_profile = profile.copy()
    out_profile.update(
        dtype='float64',
        count=1,
        compress='lzw',
        nodata=None
    )

    with rio.open(output_data, 'w', **out_profile) as dst:
        dst.write(hs.astype('float64'), 1)

#-----------------------------------------------------------------------------------------------------------------------------------
#HITER PRIKAZ HILLSHADE-ja z MATPLOTLIB-om
#-----------------------------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(5, 5))
im = ax.imshow(hs, cmap='gray', extent=ext),
ax.set_title('Hillshade by RVT')
plt.show()
