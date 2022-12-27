from shp_parser.shp_parser import BuildingInfoShpReader
from util.visualize import visualize_projected_points, visualize_latlon_points
from coord_converter.coord_converter import convert_points_coord

if __name__ == '__main__':
    test_shp_path_bi = 'E:/dataset/3D_GIS/Building_Info/Daejeon/F_FAC_BUILDING_30_202212.shp'
    test_shp_path_dm = 'E:/dataset/3D_GIS/Digital_Map/36710058/B0010000.shp'

    # 건물정보 Shp 읽고 변환 후 가시화
    bi_reader = BuildingInfoShpReader(test_shp_path_bi)
    bi_points, bi_polygon_point_counts = bi_reader.get_points_array()
    bi_converted_points = convert_points_coord(bi_points, from_epsg='epsg:5174') # Bessel 타원체 중부원점, 5174
    visualize_latlon_points('bi_viz', bi_converted_points, bi_polygon_point_counts, limit=10000)

    # 수치지도 Shp 읽고 변환 후 가시화
    dm_reader = BuildingInfoShpReader(test_shp_path_dm, ['층수'])
    dm_points, dm_polygon_point_counts = dm_reader.get_points_array()
    dm_converted_points = convert_points_coord(dm_points, from_epsg='epsg:5186') # GSR80 TM, (5186:중부, 5185:서부, 5187:동부, 5188:동해)
    visualize_latlon_points('dm_viz', dm_converted_points, dm_polygon_point_counts, limit=10000)

    

