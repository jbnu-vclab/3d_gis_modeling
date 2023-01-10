import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = 'batang' #서체
plt.rcParams["figure.figsize"] = (10,10)

#파일 읽기
df = gpd.read_file('C:/Users/cjhh6/OneDrive/문서/공간정보 AI/AL_36_D010_20221203/AL_36_D010_20221203.shp', encoding='euc-kr')
df.head() #데이터 프레임에서 상위 5개 행 출력

#plot을 이용해 그리기
ax = df.convex_hull.plot(color='red', edgecolor="r")
ax.set_axis_off() #축제거

#예외처리
df = df[df.A4=="세종특별자치시 반곡동"]

ax = df.convex_hull.plot(color='blue', edgecolor="b")
ax.set_title("세종특별자치시 반곡동")
ax.set_axis_off() #축제거
plt.show()
