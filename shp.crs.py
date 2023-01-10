import geopanda계 as gpd

#파일 읽기
sejong = gpd.read_file("C:/Users/홍사강/Desktop/공간정보/실험체/세종시/sejong.shp", encoding = 'euc-kr')

#좌표계 변환하기
sejong_change = sejong.to_crs(epsg=4326)
print(sejong_change.geometry[1]) #변환한 좌표계
#print(sejong.geometry[1]) #원본의 좌표계
