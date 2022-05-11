from operator import is_
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, GPSPoint
from lanelet2.projection import UtmProjector
import shapefile

Sign_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_TrafficSign.shp")

Node_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/HD_LaneNode.shp")


Traffic_Sign = []
Node = []

def read_TrafficSign(file_path):
    borders = file_path.shapeRecords()
    for border in borders:
        sign = {'id':border.record[0], "RoadID":border.record[2],'Shape':border.record[3],'Type1':border.record[5],'Type2':border.record[6],'lon':border.shape.points[0][0],'lat':border.shape.points[0][1]}
        print(sign["lat"])
        Traffic_Sign.append(sign)

def read_Node(file_path):
    borders = file_path.shapeRecords()
    for border in borders:
        node = {'id':border.record[0], 'lon':border.shape.points[0][0], 'lat':border.shape.points[0][1]}
        print(node)
        Node.append(node)

read_TrafficSign(Sign_file)
# read_Node(Node_file)