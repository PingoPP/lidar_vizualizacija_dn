'''
Avtor / Author: Jaka Dacar 
Nazadnje spremenjeno / Last changed: 26.10.2026

Ta algoritem je uporabljen za uporabo vizualizacijske tehnike - Simple Local Relief Model s pomočjo RVT oz. Relief Visualization Toolbox (v nadaljevanju bom uporabil besedo 'SLRM')
That algorithm was made for visualisation tecnique - Simple Local Relief Model with the help by RVT or Relief Visualization Toolbox (in continute, I will use word 'SLRM')


Algoritem je bil ustvarjen v sklopu diplomske naloge 
Algorithm was made as part of bachelor thesis
'''

import rvt.vis
import rvt.default
from pathlib import Path
import numpy as np

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT in OUTPUT
#-----------------------------------------------------------------------------------------------------------------------------------

input_data = Path(r"C:\Users\jakad\OneDrive\Desktop\3d_data\output\Pivola_klasificirano_in_rastirano.tiff")
output_data = Path(r"C:\Users\jakad\OneDrive\Desktop\diplomska naloga\SLRM-RVT\output-data\SLRM_6.tiff")

#-----------------------------------------------------------------------------------------------------------------------------------
#ARRAY in NODATA
#-----------------------------------------------------------------------------------------------------------------------------------

data_dict = rvt.default.get_raster_arr(input_data)
data_arr = data_dict['array']
data_no_data=data_dict['no_data']

#-----------------------------------------------------------------------------------------------------------------------------------
#SLRM
#-----------------------------------------------------------------------------------------------------------------------------------

slrm_arr = rvt.vis.slrm(
    dem=data_arr,
    radius_cell=20,
    ve_factor=1,
    no_data=data_no_data
)

#-----------------------------------------------------------------------------------------------------------------------------------
#SHRANJEVANJE 
#-----------------------------------------------------------------------------------------------------------------------------------

rvt.default.save_raster(
    src_raster_path=str(input_data),
    out_raster_path=str(output_data),
    out_raster_arr=slrm_arr.astype(np.float32),
    no_data=np.nan
)
