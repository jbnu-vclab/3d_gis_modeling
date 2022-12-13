from shp_parser.shp_parser import BuildingInfoShpReader
from util.visualize import visualize_projected_points

def shp_to_model(shp_path: str):
    bi_reader = BuildingInfoShpReader(test_shp_path)

    points = []
    # for i in range(len(bi_reader)):
    for i in range(10000):
        building_data = bi_reader[i]
        points.append(building_data['POINT'])

    visualize_projected_points(points)

if __name__ == '__main__':
    test_shp_path = 'E:/dataset/3D_GIS/Building_Info/Daejeon/F_FAC_BUILDING_30_202212.shp'

    shp_to_model(test_shp_path)
