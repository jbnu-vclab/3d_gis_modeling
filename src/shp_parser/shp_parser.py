import shapefile
import numpy as np

class BuildingInfoShpReader:
    def __init__(self,
                 filepath: str,
                 required_field=None,
                 encoding='cp949'
                 ):
        if required_field is None:
            required_field = ['HEIGHT', 'REGIST_DAY', 'GRND_FLR', 'UGRND_FLR']

        self.sf = shapefile.Reader(filepath, encoding=encoding)
        assert self.sf.shapeType == shapefile.POLYGON, 'BuildingInfoShapeReader only handles polygon data'

        self.num_polygons = len(self.sf)          # 지도에 들어있는 전체 polygon(건물) 개수
        self.bbox = self.sf.bbox                # 지도에 들어있는 전체 지역의 Bounding box
        # self.shapes = self.sf.shapes()        # 전체 shape 데이터 참조. 각 index로 접근하면 개별 건물의 bbox와 point 등을 얻을 수 있음, 전체 indexing하면 느리므로 사용 안함

        self.required_field = required_field    # 정보를 가져올 field 목록
        self.field_names = [x[0] for x in self.sf.fields[1:]]   # 전체 field 목록(이름만)

        for f in self.required_field:
            assert f in self.field_names, 'Required field {} not exist in shp file'.format(f)

        # 내부 저장 데이터, numpy를 사용하지 않는 경우 좌표계 변환 등에 시간이 오래 걸림
        self.points = None # np.ndarray # 모든 polygon의 좌표를 담고있는 numpy array
        self.polygon_point_counts = None # list # 각 polygon의 좌표 개수를 담고있는 list

        self.records = None # dict

    def get_record_of(self, idx) -> dict:
        res_record = {x:self.sf.record(idx)[x] for x in self.required_field}
        return res_record

    def get_records(self) -> list:
        if self.records is not None:
            return self.records
        else:
            self.records = [{x:self.sf.record(idx)[x] for x in self.required_field} for _,idx in range(self.num_polygons)]
            return self.records

    def get_points_array(self):
        if self.points is not None:
            return self.points, self.polygon_point_counts
        else:
            self.polygon_point_counts = [len(self.sf.shape(i).points) for i in range(self.num_polygons)]

            num_total_point = sum(self.polygon_point_counts)
            self.points = np.empty((num_total_point, 2))
            start = 0
            for i in range(self.num_polygons):
                self.points[start:start+self.polygon_point_counts[i]] = np.array(self.sf.shape(i).points)
                start = start+self.polygon_point_counts[i]

            return self.points, self.polygon_point_counts

    def __getitem__(self, idx) -> list:
        return self.sf.shape(idx).points

    def __len__(self) -> int:
        return self.num_polygons

if __name__ == "__main__":
    test_shp_path = 'E:/dataset/3D_GIS/Building_Info/Daejeon/F_FAC_BUILDING_30_202212.shp'
    bi_reader = BuildingInfoShpReader(test_shp_path)

    print(bi_reader[0]) # print points of polygon of 0th building
