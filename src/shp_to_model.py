from shp_parser.shp_parser import BuildingInfoShpReader
from util.visualize import visualize_projected_points, visualize_latlon_points
from coord_converter.coord_converter import convert_points_coord

def shp_to_model(shp_path: str):
    bi_reader = BuildingInfoShpReader(test_shp_path)

    points, polygon_point_counts = bi_reader.get_points_array()

    # visualize_projected_points(points, polygon_point_counts, limit=1000)

    converted_points = convert_points_coord(points)
    visualize_latlon_points(converted_points, polygon_point_counts, limit=10000)

if __name__ == '__main__':
    test_shp_path = 'E:/dataset/3D_GIS/Building_Info/Daejeon/F_FAC_BUILDING_30_202212.shp'

    shp_to_model(test_shp_path)
