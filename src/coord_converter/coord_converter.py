# https://wooble52.tistory.com/32
# https://dabid.tistory.com/3

from pyproj import Proj, transform
import numpy as np

def convert_points_coord(points,
                        from_epsg:str = 'epsg:5174', # Bessel 타원체 중부원점, 5174
                        to_epsg:str = 'epsg:4326', # WGS84 위경도
                        ) -> (int, int):
    # TODO: convert to proj2 version code (https://pyproj4.github.io/pyproj/stable/gotchas.html#upgrading-to-pyproj-2-from-pyproj-1)
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    proj_from = Proj(init=from_epsg)
    proj_to = Proj(init=to_epsg)
    converted = transform(proj_from, proj_to, points[:,0], points[:,1])

    converted_array = np.array(converted).transpose((1,0)) # n x 2
    converted_array[:,[0,1]] = converted_array[:,[1,0]] # lon, lat -> lat, lon
    return converted_array
