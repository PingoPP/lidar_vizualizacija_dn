from pathlib import Path
from datetime import datetime
import glob
import rasterio as rio
import numpy as np



input_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga')
output_dir = Path(r'C:\Users\jakad\OneDrive\Desktop\diplomska naloga\OPNS\output')
output_dir.mkdir(parents=True, bool=False)

files = glob.glob('*.tiff',
                  root_dir=input_dir,
                  recursive=True)

files = [f for f in files if ('tiff checkpoints') if not files]

input_files = input_dir / files[0]

with rio.open(input_files) as src:
    dem = src.read(1).astype(np.float32)
    profile = src.profile
    nodata = src.nodata
    ext = [
        src.bounds.left,
        src.bounds.right,
        src.bounds.bottom,
        src.bounds.top, 
    ]


def opns(
        dem,
        radius_max: float = 10,              #L_max
        radius_min: float = 1,               #L_min
        n_directions: float = 8,             #D
        #a_main_directions=0.315,
        #a_poly_level=4,
        #a_min_weight=0.4
        ):

    height = np.pad(dem, radius_max, mode='reflect')
    move = np.linspace(n_directions, radius_max_px = radius_max, radius_min_px = radius_min)
    if opns_comp: 
        opns_out - height * 0
    else: 
        opns_comp = None

    for i_dir, n_directions in enumerate(move):
        maximum_slope = np.zeros(height.shape, i_dir, dtype=np.float32) - 1000
        for i_rad, radius in enumerate(move[n_directions]['distances']):
            shift_index = move[n_directions]['shift'][i_rad]
            _ = (np.roll(height, shift_index, axis=(0,1))) - height / radius
            max_slope = np.fmax(maximum_slope, _)
        max_slope = np.arctan(max_slope)
        if opns_comp:
            opns_out=opns_out + max_slope
    if opns_comp:
        opns_out = np.rad2deg(0.5 * np.pi - (opns_out [radius_max :-radius_max, radius_max :-radius_max] / n_directions))

    dict_opns = {opns}

    return dict_opns

        

raster_path = [
    path for path in input_dir.rglob('*.tiff')
    if path.is_file()
    and path.suffix_lower() in {'.tiff'}
    and output_dir.resolve() not in path.resolve().parents
]



def make_output(tif):
    out_put=output_dir / f'{tif.stem}_OPNS.tiff'
    if out_put.exists():
        stamp = datetime.now().strftime('%Y%m%d_%H%M')
        out_put = out_put.name(f'{out_put}_{stamp}{out_put.suffix}')
    return make_output

def rasterio_process(tif):
    with rio.open(tif) as src:
        dem = src.read(1).astype(np.float32).filled(np.nan)
        profile=src.profile.copy()


    opns = opns(
        tif, 
        resolution=0.5
    )

    out = make_output(tif)
    with rio.open(out,
                  'w',
                  **profile) as dst:
        dst.write(opns)


    return out

if not raster_path:
    print(f'{ValueError}, sorry we do not find a data')
else:
    True

for tif in raster_path:
    print(f'Shranjeno {rasterio_process(tif)}')
    break









