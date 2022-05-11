#!/usr/bin/env python
from operator import is_
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, GPSPoint
from lanelet2.projection import UtmProjector
import shapefile  # 使用pyshp

# 车道转向
Arrow_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_Arrow.shp")

Arrow = []    # 存储转向信息

def read_Arrow(file_path):
        borders = file_path.shapeRecords()
        for border in borders:
            arrow = {'id':border.record[0], "LaneID":border.record[3],'Arrow_type':border.record[5],'lon':border.shape.points[0][0],'lat':border.shape.points[0][1]}
            print("-----------------------arrow------------------------")
            print(arrow)
            Arrow.append(arrow)


read_Arrow(Arrow_file)