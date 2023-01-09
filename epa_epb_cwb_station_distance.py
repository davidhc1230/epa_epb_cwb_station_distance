#本程式以氣象局測站、環保署空品測站以及地方環保局空品測站進行距離比對，計算對應最近的測站及其距離
#包含：
#1.計算距離及對應測站(每個氣象局測站對應到最近的環保署測站
#2.每個環保署測站對應到最近的氣象局測站
#3.每個地方環保局測站對應到最近的氣象局測站
#除此之外也達到分別以.shp和.csv進行不同資料格式處理的練習

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np

##############讀氣象局測站座標檔##############
cwb_xy = pd.read_csv('data/氣象局現有測站彙整_20220831更新.csv')
cwb = gpd.GeoDataFrame(cwb_xy, geometry=gpd.points_from_xy(cwb_xy.經度, cwb_xy.緯度))
cwb.crs = {'init' :'epsg:4326'}
cwb = cwb.to_crs('epsg:3826')
cwb = cwb[cwb['類型'] == '自動站'] #指定測站類型，若不指定則把整行標註掉
##############讀環保署空品測站位置shp檔##############
epa = gpd.read_file('data/環保署測站彙整/空氣品質監測站位置圖_121_10704.shp')
epa = epa.to_crs('epsg:3826')
##############讀環保局測站座標檔##############
epb_xy = pd.read_csv('data/地方環保局現有測站彙整_20220901更新.csv')
epb = gpd.GeoDataFrame(epb_xy, geometry=gpd.points_from_xy(epb_xy.經度, epb_xy.緯度))
epb.crs = {'init' :'epsg:4326'}
epb = epb.to_crs('epsg:3826')
#############計算距離及對應測站(每個氣象局測站對應到最近的環保署測站)##############
list_station = list(cwb_xy.iloc[:, 1])
list_lon = list(cwb_xy.iloc[:, 3])
list_lat = list(cwb_xy.iloc[:, 4])
list_0 =[]
list_1 =[]
list_2 =[]
for station, lon, lat in zip(list_station, list_lon, list_lat):
    point = Point(lon, lat)
    point_gdf = gpd.GeoDataFrame(geometry=[point], crs='epsg: 4326') #
    point_gdf = point_gdf.to_crs('epsg:3826')
    point_gdf2 = Point(*list(point_gdf.geometry[0].coords)[0])
    epa_station = epa.distance(point_gdf2).sort_values().index[0] #抓出離該點最近的測站
    epa_station = epa.iloc[:, 0][epa_station] #列出最近測站名稱
    distance = np.round(np.min(epa.distance(point_gdf2))/1000, 2)
    list_0.append(station)
    list_1.append(epa_station)
    list_2.append(distance)
    distance_df = pd.DataFrame(zip(list_0, list_1, list_2),  columns=['氣象局測站名稱' ,'對應最近環保署測站名稱','距離(km)'])
    distance_df.to_csv('cwb_epa_distance.csv', sep = ',', index=False, encoding='utf_8_sig') #輸出csv 
#############計算距離及對應測站(每個環保署測站對應到最近的氣象局測站)##############
#cwb_point = cwb['geometry']
list_0 =[]
list_1 =[]
list_2 =[]
for i, j in zip(epa['SiteName'],epa['geometry']):
    cwb_station = cwb.distance(j).sort_values().index[0] #抓出離該點最近的測站(在矩陣中的位置)
    cwb_station = cwb.iloc[:, 1][cwb_station] #抓出測站名稱
    distance = np.round(np.min(cwb.distance(j))/1000, 2) #計算最短距離(m)
    list_0.append(i)
    list_1.append(cwb_station)
    list_2.append(distance)
    distance_df = pd.DataFrame(zip(list_0, list_1, list_2),  columns=['環保署測站名稱','對應最近氣象局測站名稱','距離(km)'])
    distance_df.to_csv('epa_cwb_distance.csv', sep = ',', index=False, encoding='utf_8_sig') #輸出csv
#############計算距離及對應測站(每個地方環保局測站對應到最近的氣象局測站)##############
#cwb_point = cwb['geometry']
list_0 =[]
list_1 =[]
list_2 =[]
for i, j in zip(epb['站名'], epb['geometry']):
    cwb_station = cwb.distance(j).sort_values().index[0] #抓出離該點最近的測站(在矩陣中的位置)
    cwb_station = cwb.iloc[:, 1][cwb_station] #抓出測站名稱
    distance = np.round(np.min(cwb.distance(j))/1000, 2) #計算最短距離(m)
    list_0.append(i)
    list_1.append(cwb_station)
    list_2.append(distance)
    distance_df = pd.DataFrame(zip(list_0, list_1, list_2),  columns=['地方環保局測站名稱','對應最近氣象局測站名稱','距離(km)'])
    distance_df.to_csv('epb_cwb_distance.csv', sep = ',', index=False, encoding='utf_8_sig') #輸出csv