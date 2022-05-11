#!/usr/bin/env python
from operator import is_
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, GPSPoint
from lanelet2.projection import UtmProjector
import shapefile  # 使用pyshp
from dbfread import DBF
from matplotlib import pyplot as plt

path = "/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/"

#车道边界线
EdgeLink_file = shapefile.Reader(path + "HD_EdgeLink.shp") 

#车道边界线节点
EdgeNode_file = shapefile.Reader(path + "HD_EdgeNode.shp") 

#车道中心线
LaneLink_file = shapefile.Reader(path + "HD_LaneLink.shp") 

#车道标线
LaneMark_file = DBF(path + "HD_LaneMark.dbf")

# 车道转向
Arrow_file = shapefile.Reader(path + "OBJ_Arrow.shp")

#转换后的osm文件路径
lanelet2_path = os.path.join("/home/fmw/map/shp2lanelet2/lanelet2_map_simple.osm")

EdgeNode = [] # 存储车道边界线节点属性
EdgeLink = [] # 存储车道边界线属性
LaneLink = [] # 存储车道中心线属性
EdgeNodeId = [] #存储已经使用的节点的ID
EdgeLineId = [] #存储已经使用的车道边界线的ID
LaneMark = [] # 存储车道标线属性
Arrow = []    # 存储转向信息

def shp2lanelet2():
    map = LaneletMap() 
    Read_File.read_EdgeNode(EdgeNode_file) 
    Read_File.read_EdgeLink(EdgeLink_file)
    Read_File.read_LaneLink(LaneLink_file)
    Read_File.read_LaneMark(LaneMark_file)
    Read_File.read_Arrow(Arrow_file)
    origin_lon = EdgeNode[0]['lon']
    origin_lat = EdgeNode[0]['lat']
    projector = UtmProjector(lanelet2.io.Origin(origin_lat, origin_lon)) 
    write = Write()
    map = write.write_lanelets(map, projector)
    lanelet2.io.write(lanelet2_path, map, projector)

class Read_File:
    # 读取车道边界线节点信息
    def read_EdgeNode(file_path):
        borders = file_path.shapeRecords() # 读取ID属性
        # border_p = file_path.shapes() # 读取经纬度
        # i = 0
        print("----------------EdgeNode--------------------")
        for border in borders:
            node = {'id':border.record[0], 'lon':border.shape.points[0][0], 'lat':border.shape.points[0][1], 'h':border.shape.z[0]}
            EdgeNode.append(node)

    # 读取车道边界线信息
    def read_EdgeLink(file_path):
        borders = file_path.shapeRecords() # 读取ID等属性
        print("----------------EdgeLink--------------------")
        for border in borders:
            points = []
            border_points = border.shape.points
            border_z = border.shape.z
            i = 0
            for p in border_points:
                point = (p[0], p[1], border_z[i])
                i = i + 1
                points.append(point)
            # points
            edge = {'id':border.record[0], 'points': points, 'SE_NodeId':border.record[2], 'EE_NodeId':border.record[3], 'Edge_type':border.record[6], 'Edge_cross':border.record[8]} # 目前demo数据无type及跨越方向信息
            EdgeLink.append(edge)
    # 读取车道中心线信息
    def read_LaneLink(file_path):
        borders = file_path.shapeRecords() # 读取ID等属性
        for border in borders:
            lane = {'id':border.record[0], 'L_EdgeId':border.record[4], 'R_EdgeId':border.record[5], 'Direction':border.record[8], 'lane_type':border.record[11], 'Speed':border.record[12]} # 目前demo数据无type及direction信息
            LaneLink.append(lane)

    def read_LaneMark(file_path): 
        for record in file_path: 
            mark = {'id':record["MarkID"], 'EdgeId':record["EdgeID"], 'Mark_type':record["Mark_type"], 'Mark_color':record["Mark_color"]}
            LaneMark.append(mark)

    def read_Arrow(file_path):
        borders = file_path.shapeRecords()
        for border in borders:
            arrow = {'id':border.record[0], "LaneID":border.record[3],'Arrow_type':border.record[5]}
            Arrow.append(arrow)

class Judge:
    # 判断是否已经生成了lanelet2 node
    def node_not_exit(s_id):
        flag = True # 不存在
        for id in EdgeNodeId:
            if s_id == id['shp_id']:
                flag = False
                break
        return flag

    # 判断是否已经生成了lanelet2 node
    def linestring_not_exit(s_id):
        flag = True # 不存在
        for id in EdgeLineId:
            if s_id == id['shp_id']:
                flag = False
                break
        return flag

class Get_Elements:
    # 获取节点id lat lon信息
    def get_node(node_id):
        nodes = []
        for node in EdgeNode:
            # print(node['id'])
            if node_id == node['id']:
                nodes.append(node)
                break
        return nodes
    # 获取车道左/右边界id 属性信息
    def get_Edge(lane, flag):
        edges = []
        id = lane[flag]
        for edge in EdgeLink:
            if id == edge['id']:
                edges.append(edge)
        return edges

    # 获取车道边界线起点和终点节点编号
    def get_ENId(edge_id, flag):
        id = -1
        for edge in EdgeLink:
            if edge_id == edge['id']:
                id = edge[flag]
                break
        return id

class Attributes:
    def lanelet_Type(lanelet, lane):
        if lane["lane_type"] == 0:
            lanelet.attributes["subtype"] = "not_investigated"
        elif lane["lane_type"] == 1:
            lanelet.attributes["subtype"] = "road"
        elif lane["lane_type"] == 2:
            lanelet.attributes["subtype"] = "entrance"
        elif lane["lane_type"] == 3:
            lanelet.attributes["subtype"] = "exit"
        elif lane["lane_type"] == 4:
            lanelet.attributes["subtype"] = "connecting_lane"
        elif lane["lane_type"] == 5:
            lanelet.attributes["subtype"] = "emergency_lane"
        elif lane["lane_type"] == 6:
            lanelet.attributes["subtype"] = "parking_lane"
        elif lane["lane_type"] == 7:
            lanelet.attributes["subtype"] = "emergency_parking_lane"
        elif lane["lane_type"] == 8:
            lanelet.attributes["subtype"] = "acceleration_lane"
        elif lane["lane_type"] == 9:
            lanelet.attributes["subtype"] = "deceleration_lane"
        elif lane["lane_type"] == 10:
            lanelet.attributes["subtype"] = "escape_lane"
        elif lane["lane_type"] == 11:
            lanelet.attributes["subtype"] = "intersection"
        elif lane["lane_type"] == 12:
            lanelet.attributes["subtype"] = "toll_lane"
        elif lane["lane_type"] == 13:
            lanelet.attributes["subtype"] = "checkpoint_lane"
        elif lane["lane_type"] == 14:
            lanelet.attributes["subtype"] = "turn_around"
        elif lane["lane_type"] == 15:
            lanelet.attributes["subtype"] = "bus_lane"
        elif lane["lane_type"] == 16:
            lanelet.attributes["subtype"] = "tidal_(variable)_Lane"
        elif lane["lane_type"] == 17:
            lanelet.attributes["subtype"] = "rail"
        elif lane["lane_type"] == 18:
            lanelet.attributes["subtype"] = "rail_parking"
        elif lane["lane_type"] == 19:
            lanelet.attributes["subtype"] = "HOV_lane "
        elif lane["lane_type"] == 30:
            lanelet.attributes["subtype"] = "bicycle_lane"
        elif lane["lane_type"] == 40:
            lanelet.attributes["subtype"] = "crosswalk"
            lanelet.attributes["one_way"] = "no"
        elif lane["lane_type"] == 99:
            lanelet.attributes["subtype"] = "else_lane"

        for arrow in Arrow:
            if lane["id"] in arrow["LaneID"]:
                if arrow["Arrow_type"] == "B":
                    lanelet.attributes["turn_direction"] = "left"
                elif arrow["Arrow_type"] == "C":
                    lanelet.attributes["turn_direction"] = "straight"
                elif arrow["Arrow_type"] == "D":
                    lanelet.attributes["turn_direction"] = "right"
                elif arrow["Arrow_type"] == "BC":
                    lanelet.attributes["turn_direction"] = "straight_left"
                elif arrow["Arrow_type"] == "CD":
                    lanelet.attributes["turn_direction"] = "straight_right"

    def linestring_Type(linestring, flag):
        for edge in EdgeLink:
            if flag == edge["id"]:
                if edge["Edge_type"] == 0:
                    linestring.attributes["type"] = "not_investigated"
                elif edge["Edge_type"] == 1:
                    linestring.attributes["type"] = "no_line"
                elif edge["Edge_type"] == 2:
                    linestring.attributes["type"] = "line_thin"
                elif edge["Edge_type"] == 3:
                    linestring.attributes["type"] = "line_thin"
                elif edge["Edge_type"] == 4:
                    linestring.attributes["type"] = "guard_rail"
                elif edge["Edge_type"] == 5:
                    linestring.attributes["type"] = "wall"
                elif edge["Edge_type"] == 6:
                    linestring.attributes["type"] = "pavement_edge"
                elif edge["Edge_type"] == 7:
                    linestring.attributes["type"] = "curbstone"
                elif edge["Edge_type"] == 8:
                    linestring.attributes["type"] = "vegetation"
                elif edge["Edge_type"] == 99:
                    linestring.attributes["type"] = "else"
        for mark in LaneMark:
            if flag == mark["EdgeId"]:
                if mark["Mark_type"] == 1:
                    linestring.attributes["subtype"] = "solid"
                elif mark["Mark_type"] == 2:
                    linestring.attributes["subtype"] = "dashed"

class Write:
    # 判断是否生成lanelet 起止node,并返回node
    def write_node(self, node_id, project): 
        node = Get_Elements.get_node(node_id)
        if node:
            print(node)
            lon = node[0]['lon']
            lat = node[0]['lat']
            projection = project.forward(GPSPoint(lat, lon, 0))
            point = Point3d(getId(), projection.x, projection.y, node[0]['h']) # poit_id:生成的node的Id
            # point.attributes["ele"] = str(node[0]['h'])
            # print("shp pose")
            print(point)
            used_edgeNodeId = {'shp_id':node[0]['id'], 'lanelet2_node':point}
            EdgeNodeId.append(used_edgeNodeId) 
            return point
        # else:
        #     print("无法获取shp节点信息")
        #     return -1

    # 判断是否生成lanelet linestring,并返回linestring
    def write_linestring(self, edge_id, points):
        linestring = LineString3d(getId(), [point for point in points]) # poit_id:生成的node的Id   缺少 中间点 
        used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
        EdgeLineId.append(used_edgeLinkId)        
        return linestring 
        
    # 生成lanelet2左/右车道线
    def write_lane(self, lane, projector, flag):
        # print("-----------------------------Write_Lane---------------------------")
        points = []
        # start_point = end_point = -1 # 不存在该点信息
        edge = Get_Elements.get_Edge(lane, flag) # 获取边界线信息
        edge_id = edge[0]['id']
        if edge_id == -1:
            print("车道线左边界ID读取错误")
            return -1
        else:
            if Judge.linestring_not_exit(edge_id):
                print("line不存在")
                startnode_id = Get_Elements.get_ENId(edge_id, 'SE_NodeId') # 获取边界起始节点编号
                if startnode_id == -1:
                    print("车道线左边界起始节点ID读取错误")
                    return -1
                else:
                    if Judge.node_not_exit(startnode_id):
                        print("该点不存在，生成该点信息")
                        start_node = self.write_node(startnode_id, projector) # 获取lanelet2起始节点信息
                        points.append(start_node)
                    else:
                        print("已生成该点，获取该点信息")
                        for node in EdgeNodeId:
                            if startnode_id == node['shp_id']:
                                points.append(node['lanelet2_node'])
                                # start_point = node['lanelet2_node']

            # print("获取中间点信息")
                for gps_point in edge[0]['points'][1:-1]:
                    lon = gps_point[0]
                    lat = gps_point[1]
                    projection = projector.forward(GPSPoint(lat, lon, 0))
                    point = Point3d(getId(), projection.x, projection.y, gps_point[2])
                    # point.attributes["ele"] = gps_point[2]
                    points.append(point)
                    print(point)

                # print("获取结束点信息")
                endnode_id = Get_Elements.get_ENId(edge_id, 'EE_NodeId')
                if endnode_id == -1:
                    print("车道线左边界终止节点ID读取错误") 
                    return -1
                else: 
                    if Judge.node_not_exit(endnode_id):
                        print("该点不存在，生成该点信息")
                        end_node = self.write_node(endnode_id, projector) # 获取lanelet2起始节点信息
                        points.append(end_node)
                    else:
                        print("已生成该点，获取该点信息")
                        for node in EdgeNodeId:
                            if endnode_id == node['shp_id']:
                                points.append(node['lanelet2_node']) 
                                # end_point = node['lanelet2_node'] 
                
            # print(points[-1])

                linestring = self.write_linestring(edge_id, points)
                # print(linestring)
                return linestring
            else:
                print("line已存在,获取line信息")
                for id in EdgeLineId:
                    if edge_id == id['shp_id']:
                        # print("边界线编号 linesting")
                        # print(edge_id, id['lanelet2_linestring'])
                        return id['lanelet2_linestring']
    
    # 生成车道lanelets
    def write_lanelets(self, map, projector):
        for lane in LaneLink:
            # print("-----------------------------LaneLink--------------------------------------------")
            # print(lane)
            left_linestring = self.write_lane(lane, projector, 'L_EdgeId')
            if left_linestring == -1:
                print("生成lanelet左边界错误")
                return

            right_linestring = self.write_lane(lane, projector, 'R_EdgeId')
            if right_linestring == -1:
                print("生成lanelet右边界错误")
                return

            Attributes.linestring_Type(left_linestring, lane["L_EdgeId"])            
            Attributes.linestring_Type(right_linestring, lane["R_EdgeId"])        
            lanelet = Lanelet(getId(), left_linestring, right_linestring)
            Attributes.lanelet_Type(lanelet, lane)
            lanelet.attributes["speed_limit"] = str(lane["Speed"])
            map.add(lanelet)
        
        return map



if __name__ == '__main__':
    shp2lanelet2()