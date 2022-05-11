# -*- coding: utf-8 -*-
import shapefile# 使用pyshp
file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/HD_LaneLink.shp")#读取
#读取元数据
print(str(file.shapeType))  # 输出shp类型
print(file.encoding)# 输出shp文件编码
print(file.bbox)  # 输出shp的文件范围（外包矩形）
print(file.numRecords)  # 输出shp文件的要素数据
print(file.fields)# 输出所有字段信息
# print(file.records())  # 输出所有属性表