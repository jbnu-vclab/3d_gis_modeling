import shapefile

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

        self.num_shapes = len(self.sf)          # 지도에 들어있는 전체 shape(건물) 개수
        self.bbox = self.sf.bbox                # 지도에 들어있는 전체 지역의 Bounding box
        # self.shapes = self.sf.shapes()        # 전체 shape 데이터 참조. 각 index로 접근하면 개별 건물의 bbox와 point 등을 얻을 수 있음, 전체 indexing하면 느리므로 사용 안함

        self.required_field = required_field    # 정보를 가져올 field 목록
        self.field_names = [x[0] for x in self.sf.fields[1:]]   # 전체 field 목록(이름만)

        for f in self.required_field:
            assert f in self.field_names, 'Required field {} not exist in shp file'.format(f)

    def __getitem__(self, idx):
        res_point = self.sf.shape(idx).points
        res_record = {x:self.sf.record(idx)[x] for x in self.required_field}
        res_record['POINT'] = res_point
        return res_record

    def __len__(self):
        return self.num_shapes

if __name__ == "__main__":
    test_shp_path = 'E:/dataset/3D_GIS/Building_Info/Daejeon/F_FAC_BUILDING_30_202212.shp'
    bi_reader = BuildingInfoShpReader(test_shp_path)

    print(bi_reader[0])
