"""
    date: 2023-02-12
    name: choiwooseok
    
    한 일:
    1. 시작점에 마지막점 중복생성
    2. 반복문 이용하여 shp파일의 모든 건물 생성 (1~n까지 생성)
    2-1. 건물 생성중 POLYGON에 기존 형식(()) 이 아닌 ((),())이 등장하여 오류발생
    2-2. 16325~16328까지 발생
    3. json파일으로 입력
    3-1. 첫번째 점의 위도와 경도를 저장
    4. 파일 저장 이름 변경 test(n번) -> N
    5. 위도 경도 epsg로 변경
    5-1. 위도 경도 변환시에 너무 차이가 적어서 obj 파일 확인이
        안되는것일 가능성이 있어 보류해둠 Line 146
    5-2. 해결방안: json 파일에만 위도경도를 변환하여 저장 or 둘다 변환 x

    할일
    1. json 파일 저장이름 정하기(현재 sample.json)
    2. flow차트 그려서 프로그램 이해 쉽게 만들기
    3. 변수명이나 함수명 직관적으로 변경

"""
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import triangulate
import matplotlib.pyplot as plt
import json
from  tkinter import *
from tkinter import filedialog
import os

def createDirectory(directory, Name):
    directory = directory+ "/" +Name
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

#삼각분할
def triangulate_within(polygon):
    return [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]

'''
POLYGON ((211292.527 360815.666, 211292.524 360817.347, 211293.32 360816.755, 211292.527 360815.666)
->
[(1, 2), (3, 4), (5, 6)]
'''
#Polygon 타입을 list안에 tuple이 들어간 형식으로 변형
def parser(polyStr):
    tmplist=list()
    polyStr = polyStr[10:len(polyStr)-2]
    polyStr = polyStr.split(', ')
    global xy
    xy = polyStr[0].split(' ')
    for i in range(len(polyStr)):
        tmp = [float(x.strip()) for x in polyStr[i].split()]
        tmplist.append(tuple(tmp))
    return tmplist

#Obj 파일 작성
def write_objfile(ext, filepath, height = 5):
    
    # 건물의 꼭짓점 갯수
    vNum = len(ext)-1

    # 파일에 저장할 내용(파일에 여러번 저장하는 것보다 한번에 저장하는게 더 빠를거 같아서 선택)
    fileStr = ""

    # f 생성시에 v의 index를 탐색하기 위하여 list에 저장해 두었다가 순차탐색으로 확인
    dp = list()

    # v 쓰기
    '''
    바닥
    v x 0 z
    형식으로 저장합니다.
    '''
    for i in range(vNum):
        fileStr += "v "+str(ext[i][0]) + " 0 " + str(ext[i][1])+"\n"
        tmp = str(ext[i][0]) + " " + str(ext[i][1])
        dp.append(tmp)
        # "1 3"     "1234.21312 1244.213213"

    # 시작위치에 점을 하나더 생성해줌 ex) 삼각형일때 1 2 3 후에 시작점에 4를 생성
    fileStr += "v "+str(ext[0][0]) + " 0 " + str(ext[0][1])+"\n"
    tmp = str(ext[0][0]) + " " + str(ext[0][1])
    dp.append(tmp)

    
    '''
    천장
    v x H z
    형식으로 저장합니다.
    '''
    for i in range(vNum):
        # print(ext[i])
        fileStr+="v "+str(ext[i][0]) + " "+str(height)+" " + str(ext[i][1])+"\n"
        tmp = str(ext[i][0]) + " " + str(ext[i][1])
        dp.append(tmp)
    # 시작위치에 점을 하나더 생성해줌 ex) 삼각형일때 1 2 3 후에 시작점에 4를 생성
    fileStr+="v "+str(ext[0][0]) + " "+str(height)+" " + str(ext[0][1])+"\n"
    tmp = str(ext[0][0]) + " " + str(ext[0][1])
    dp.append(tmp)

    fileStr+="\n"

    '''
    vt 바닥
    '''
    for i in range(vNum + 1):
        fileStr+="vt "+ str(i/vNum) +" 0 \n"
        
    for i in range(vNum + 1):
        fileStr+="vt "+ str(i/vNum) +" 1 \n"        

    fileStr+="\n"

    # f 쓰기
    for i in range (len(tris)):
        tmp = str(tris[i])      # polygon((1, 2),(1, 3))
        tmp = tmp[10:len(tmp)-2]
        tmpList = tmp.split(', ')
        # print(tmpList)
        floorStr = "f "
        ceilStr = "f "
        for j in range(3):
            curPoint = tmpList[j]

            for t in range(vNum):
                if(curPoint == dp[t]):
                    floorStr += (str(t+1)+" ")
                    ceilStr += (str(t+2+vNum)+" ")    
        fileStr+=floorStr+"\n"
        fileStr+=ceilStr+"\n"

    fileStr+="\n"

    # 벽제작
    '''
     1 2
     1+vNum 2+vNum
     위의 4개가 하나의 벽
     f 1 2 1+vNum
     f 1+vNum 2+vNum 2
    '''
    for i in range(vNum):
        # 사각형의 좌표 4개 
        a = i+1
        b = i+2
        c = i+2+vNum
        d = i+3+vNum
        fileStr+="f "+str(a)+" "+str(b)+" "+str(c)+"\n"
        fileStr+="f "+str(c)+" "+str(d)+" "+str(b)+"\n"

    # 파일 열기
    # filepath="C:/example2/testfile.obj"
    # filepathtxt="C:/example2/testfile.txt"

    file = open(filepath , mode='w')

    file.write(fileStr)
    file.close()


#파일 불러오기
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "C:",title = "choose your file",filetypes = (("shp files","*.shp"),("all files","*.*")))
print (root.filename)
root.withdraw()

test_shp_path_dm = root.filename

# 수치지도 Shp 읽고, Polygon만 추출
shapefile = gpd.read_file(test_shp_path_dm)
# shapefile = shapefile.to_crs(epsg=4326)
shapefileGeometry = shapefile.geometry

# poly = shapefileGeometry[2]

# json 데이터 저장할 변수 
jsonData = {}

xy =[]  # 위도경도 저장 전역 변수

#저장할 파일 위치 선택
root = Tk()
root.withdraw()
dir_path = filedialog.askdirectory(parent=root, initialdir="/",title='Please select a directory')
print(dir_path)

createDirectory(dir_path, "obj")
createDirectory(dir_path, "json")

#for i in range(len(shapefileGeometry)):
for i in range( 10):

    filepath = dir_path + "/obj/"+str(i+1)+".obj"
    poly = shapefileGeometry[i]
    # geometry 타입을 list로 변경
    polyStr = str(poly)
    ext = parser(polyStr)

    #삼각분할 후 geometry로 타입 변환
    tris = triangulate_within(poly)
    change = gpd.GeoSeries(tris)

    write_objfile(ext, filepath)

    jsonData[i+1]=[]
    jsonData[i+1].append({
        "filename": str(i+1)+".obj",
        "longitude": str(xy[1]),
        "latitude": str(xy[0])
        })

jsonfilepath = dir_path + "/json/sample.json"
with open(jsonfilepath, 'w') as outfile:
    json.dump(jsonData, outfile)


# 출력 확인용
#change.plot()
#plt.show()

'''
n+2각형일때 n개의 삼각형

1개당 3*(n+2)

3*n*(n+2)

3n^2+6n
'''
