# import csv

# with open("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/LaneADAS.csv") as f:
#     f_csv = csv.DictReader(f)
#     # headers = next(f_csv)
#     # print(headers)
#     for row in f_csv:
#         print(row)
#         # print("LaneID:", row["LaneID"])

#  -------------------分隔线--------------------------------

from operator import is_
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, GPSPoint
from lanelet2.projection import UtmProjector
import shapefile  # 使用pyshp


Arrow_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_Arrow.shp")


Arrow = []
num = '1413129430'
def read_Arrow(file_path):
    borders = file_path.shapeRecords()
    for border in borders:
        arrow = {'id':border.record[0], "LaneID":border.record[3],'Arrow_type':border.record[5]}
        print(arrow)
        Arrow.append(arrow)

read_Arrow(Arrow_file)

# for arrow in Arrow:
#     if ";" in arrow["LaneID"]:
#         num1 = arrow["LaneID"].split(";", 1)[0]
#         num2 = arrow["LaneID"].split(";", 1)[1]
#         if num == num1 or num == num2:
#             print("yes", arrow["LaneID"], "存在；")
#         else:
#             print("none")
#     else:
#         if num == arrow["LaneID"]:
#             print("yes", arrow["LaneID"], arrow["Arrow_type"])
#         else:
#             print("none")

for arrow in Arrow:
    if num in arrow["LaneID"]:
        print("yes", arrow["LaneID"], arrow["Arrow_type"])
    else:
        print("none")

# ----------------------------------分隔线----------------------------------
# from dbfread import DBF

# Arrow_file = DBF("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_Arrow.dbf")

# Arrow = []

# def read_Arrow(file_path): 
#     for record in file_path: 
#         print(record)
#         #mark = {'id':record["MarkID"], 'EdgeId':record["EdgeID"], 'Mark_type':record["Mark_type"], 'Mark_color':record["Mark_color"]}
#         #Arrow.append(mark)

# read_Arrow(Arrow_file)




