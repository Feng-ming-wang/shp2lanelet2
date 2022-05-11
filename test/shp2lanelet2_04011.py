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
# from matplotlib import pyplot as plt

#车道边界线
EdgeLink_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/HD_EdgeLink.shp") 

#车道边界线节点
EdgeNode_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/HD_EdgeNode.shp") 

#车道中心线
LaneLink_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/HD_LaneLink.shp") 

#车道标线
LaneMark_file = DBF("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/HD_LaneMark.dbf")

# 车道转向
Arrow_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_Arrow.shp")

# 交通标志
Sign_file = shapefile.Reader("/home/fmw/map/shp2lanelet2/demo_HD_SHP_20220402/OBJ_TrafficSign.shp")

#转换后的osm文件路径
lanelet2_path = os.path.join("/home/fmw/map/shp2lanelet2/lanelet2_map_sign.osm")

EdgeNode = [] # 存储车道边界线节点属性
EdgeLink = [] # 存储车道边界线属性
LaneLink = [] # 存储车道中心线属性
EdgeNodeId = [] #存储已经使用的节点的ID
EdgeLineId = [] #存储已经使用的车道边界线的ID
LaneMark = [] # 存储车道标线属性
Arrow = []
Traffic_Sign = []
def shp2lanelet2():
    map = LaneletMap() 
    read_EdgeNode(EdgeNode_file) 
    read_EdgeLink(EdgeLink_file)
    read_LaneLink(LaneLink_file)
    read_LaneMark(LaneMark_file)
    read_Arrow(Arrow_file)
    read_TrafficSign(Sign_file)
    origin_lon = EdgeNode[0]['lon']
    origin_lat = EdgeNode[0]['lat']
    print("初始经纬度")
    print(origin_lon)
    print(origin_lat)
    projector = UtmProjector(lanelet2.io.Origin(origin_lat, origin_lon)) 
    map = write_lanelets(map, projector)
    # map = write_cross(map, projector)
    # print(map)
    lanelet2.io.write(lanelet2_path, map, projector)

# 读取车道边界线节点信息
def read_EdgeNode(file_path):
    borders = file_path.shapeRecords() # 读取ID属性
    # border_p = file_path.shapes() # 读取经纬度
    # i = 0
    # print("----------------EdgeNode--------------------")
    for border in borders:
        node = {'id':border.record[0], 'lon':border.shape.points[0][0], 'lat':border.shape.points[0][1]}
        # print(node)
        EdgeNode.append(node)
   
# 读取车道边界线信息
def read_EdgeLink(file_path):
    borders = file_path.shapeRecords() # 读取ID等属性
    # print("----------------EdgeLink--------------------")
    for border in borders:
        edge = {'id':border.record[0], 'points': border.shape.points, 'SE_NodeId':border.record[2], 'EE_NodeId':border.record[3], 'Edge_type':border.record[6], 'Edge_cross':border.record[8]} # 目前demo数据无type及跨越方向信息
        # print(edge)
        EdgeLink.append(edge)
    
# 读取车道中心线信息
def read_LaneLink(file_path):
    borders = file_path.shapeRecords() # 读取ID等属性
    # print("----------------LaneLink--------------------")
    for border in borders:
        lane = {'id':border.record[0], 'L_EdgeId':border.record[4], 'R_EdgeId':border.record[5], 'RoadID':border.record[6], 'Direction':border.record[8], 'lane_type':border.record[11], 'Speed':border.record[12]} # 目前demo数据无type及direction信息
        # print(lane)
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

def read_TrafficSign(file_path):
    borders = file_path.shapeRecords()
    for border in borders:
        sign = {'id':border.record[0], "RoadID":border.record[2],'Shape':border.record[3],'Type1':border.record[5],'Type2':border.record[6],'lon':border.shape.points[0][0],'lat':border.shape.points[0][1]}
        Traffic_Sign.append(sign)

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

# 获取节点id lat lon信息
def get_node(node_id):
    nodes = []
    for node in EdgeNode:
        # print(node['id'])
        if node_id == node['id']:
            nodes.append(node)
            break
    return nodes

# 判断是否生成lanelet 起止node,并返回node
def write_node(node_id, project):
    # print("-----------------------------------write_node----------------------------------")
    # print(node_not_exit(node_id))    
    node = get_node(node_id)
    # print("shp node")
    # print("------------node------------------")
    # print(node)
    if node:
        # print("shp pose")
        # print(node)
        lon = node[0]['lon']
        lat = node[0]['lat']
        projection = project.forward(GPSPoint(lat, lon, 0))
        point = Point3d(getId(), projection.x, projection.y, 0) # poit_id:生成的node的Id
        # print("shp pose")
        # print(node)
        used_edgeNodeId = {'shp_id':node[0]['id'], 'lanelet2_node':point}
        # print(node_id)
        # print('id: %d lon: %.8f lat: %.8f' %(point.id, point.y, point.x))
        EdgeNodeId.append(used_edgeNodeId) 
        # print("节点编号 node")
        # print(node_id, point)
        return point
    # else:
    #     print("无法获取shp节点信息")
    #     return -1


# 判断是否生成lanelet linestring,并返回linestring
def write_linestring(edge_id, points):
    # print("---------------------------------write_linestring-------------------------------")

    linestring = LineString3d(getId(), [point for point in points]) # poit_id:生成的node的Id   缺少 中间点 
    used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    EdgeLineId.append(used_edgeLinkId)        
    return linestring 

    # print(linestring_not_exit(edge_id))
    # if linestring_not_exit(edge_id):
    #     print("line不存在")
        # print(edge_id)
    # if start == -1 and end == -1:
    #     linestring = LineString3d(getId(), [point for point in points]) # poit_id:生成的node的Id   缺少 中间点 
    #     used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    #     EdgeLineId.append(used_edgeLinkId)        
    #     return linestring 
    # elif start != -1 and end == -1:
    #     print(start)
    #     linestring = LineString3d(getId(), [start, (point for point in points)]) # poit_id:生成的node的Id   缺少 中间点 
    #     used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    #     EdgeLineId.append(used_edgeLinkId)        
    #     return linestring   
    # elif start == -1 and end != -1:
    #     linestring = LineString3d(getId(), [(point for point in points), end]) # poit_id:生成的node的Id   缺少 中间点 
    #     used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    #     EdgeLineId.append(used_edgeLinkId)        
    #     return linestring   
    # elif start != -1 and end != -1:
    #     linestring = LineString3d(getId(), [start, (point for point in points), end]) # poit_id:生成的node的Id   缺少 中间点 
    #     used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    #     EdgeLineId.append(used_edgeLinkId)        
    #     return linestring   
    
    # linestring = LineString3d(getId(), [Point3d(getId(), point.x, point.y, 0) for point in points]) # poit_id:生成的node的Id   缺少 中间点    
    # # print("边界线编号 linesting")
    # # print(edge_id, linestring)
    # used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
    # EdgeLineId.append(used_edgeLinkId)        
    # return linestring
    # else:
    #     print("line已存在")
    #     for id in EdgeLineId:
    #         if edge_id == id['shp_id']:
    #             # print("边界线编号 linesting")
    #             # print(edge_id, id['lanelet2_linestring'])
    #             return id['lanelet2_linestring']

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



# 生成lanelet2左/右车道线
def write_lane(lane, projector, flag):
    print("-----------------------------Write_Lane---------------------------")
    points = []
    # start_point = end_point = -1 # 不存在该点信息
    edge = get_Edge(lane, flag) # 获取边界线信息
    edge_id = edge[0]['id']
    if edge_id == -1:
        print("车道线左边界ID读取错误")
        return -1
    else:
        # print("边界编号： %d" %leftedge_id)
        # print("获取起始点信息")
        if linestring_not_exit(edge_id):
            print("line不存在")
            # edge = edge_link[:]
            # print(edge[0]['id'])
            # print(edge[0]['points'])
            # del edge[0]['points'][0]
            # del edge[0]['points'][-1]
            startnode_id = get_ENId(edge_id, 'SE_NodeId') # 获取边界起始节点编号
            if startnode_id == -1:
                print("车道线左边界起始节点ID读取错误")
                return -1
            else:
                if node_not_exit(startnode_id):
                    print("该点不存在，生成该点信息")
                    start_node = write_node(startnode_id, projector) # 获取lanelet2起始节点信息
                    points.append(start_node)
                else:
                    print("已生成该点，获取该点信息")
                    for node in EdgeNodeId:
                        if startnode_id == node['shp_id']:
                            points.append(node['lanelet2_node'])
                            # start_point = node['lanelet2_node']

        # print(points[0])

        # print("获取中间点信息")
            for gps_point in edge[0]['points'][1:-1]:
                lon = gps_point[0]
                lat = gps_point[1]
                projection = projector.forward(GPSPoint(lat, lon, 0))
                point = Point3d(getId(), projection.x, projection.y, 0)
                points.append(point)
                # print(point)

            # print("获取结束点信息")
            endnode_id = get_ENId(edge_id, 'EE_NodeId')
            if endnode_id == -1:
                print("车道线左边界终止节点ID读取错误") 
                return -1
            else: 
                if node_not_exit(endnode_id):
                    print("该点不存在，生成该点信息")
                    end_node = write_node(endnode_id, projector) # 获取lanelet2起始节点信息
                    points.append(end_node)
                else:
                    print("已生成该点，获取该点信息")
                    for node in EdgeNodeId:
                        if endnode_id == node['shp_id']:
                            points.append(node['lanelet2_node']) 
                            # end_point = node['lanelet2_node'] 
            
        # print(points[-1])

            linestring = write_linestring(edge_id, points)
            # print(linestring)
            return linestring
        else:
            print("line已存在,获取line信息")
            for id in EdgeLineId:
                if edge_id == id['shp_id']:
                    # print("边界线编号 linesting")
                    # print(edge_id, id['lanelet2_linestring'])
                    return id['lanelet2_linestring']
        
def lanelet_Type(lanelet, lane):
    if lane["lane_type"] == 1:
        lanelet.attributes["subtype"] = "road"
    elif lane["lane_type"] == 2:
        lanelet.attributes["subtype"] = "entrance_road"
    elif lane["lane_type"] == 3:
        lanelet.attributes["subtype"] = "exit_road"
    elif lane["lane_type"] == 4:
        lanelet.attributes["subtype"] = "connecting_road"
    elif lane["lane_type"] == 5:
        lanelet.attributes["subtype"] = "emergency_lane"
    elif lane["lane_type"] == 6:
        lanelet.attributes["subtype"] = "parking_road"
    elif lane["lane_type"] == 7:
        lanelet.attributes["subtype"] = "emergency_parking_road"
    elif lane["lane_type"] == 8:
        lanelet.attributes["subtype"] = "acceleration_road"
    elif lane["lane_type"] == 30:
        lanelet.attributes["subtype"] = "bicycle_lane"
    elif lane["lane_type"] == 40:
        lanelet.attributes["subtype"] = "crosswalk"
        lanelet.attributes["one_way"] = "no"

    for arrow in Arrow:
        if lane["id"] in arrow["LaneID"]:
            if arrow["Arrow_type"] == "B":
                lanelet.attributes["turn_direction"] = "left"
            elif arrow["Arrow_type"] == "C":
                lanelet.attributes["turn_direction"] = "straight"
            elif arrow["Arrow_type"] == "D":
                lanelet.attributes["turn_direction"] = "right"


def linestring_Type(linestring, flag):
    for edge in EdgeLink:
        if flag == edge["id"]:
            if edge["Edge_type"] == 2:
                linestring.attributes["type"] = "line_thin"
            elif edge["Edge_type"] == 4:
                linestring.attributes["type"] = "guard_rail"
            elif edge["Edge_type"] == 5:
                linestring.attributes["type"] = "wall"
            elif edge["Edge_type"] == 7:
                linestring.attributes["type"] = "curbstone"
    for mark in LaneMark:
        if flag == mark["EdgeId"]:
            if mark["Mark_type"] == 1:
                linestring.attributes["subtype"] = "solid"
            elif mark["Mark_type"] == 2:
                linestring.attributes["subtype"] = "dashed"  

def regulator_Element(lane, lanelet, projector):
    for sign in Traffic_Sign:
        if lane["RoadID"] == sign["RoadID"]:
            projection = projector.forward(GPSPoint(sign["lat"], sign["lon"], 0))
            x1 = projection.x
            y = projection.y
            x2 = x1 + 1
            p1 = Point3d(getId(), x1, y, 0)
            p2 = Point3d(getId(), x2, y, 0)
            line = LineString3d(getId(), [p1, p2])
            line.attributes["type"] = "traffic_sign"
            regelem = TrafficLight(getId(), AttributeMap(), [line])
            regelem.attributes["type"] = "regulatory_element"
            regelem.attributes["subtype"] = "traffic_sign"
            lanelet.addRegulatoryElement(regelem)
        



# 生成车道lanelets
def write_lanelets(map, projector):
    for lane in LaneLink:
        print("-----------------------------LaneLink--------------------------------------------")
        # print(lane)
        left_linestring = write_lane(lane, projector, 'L_EdgeId')
        if left_linestring == -1:
            print("生成lanelet左边界错误")
            return

        right_linestring = write_lane(lane, projector, 'R_EdgeId')
        if right_linestring == -1:
            print("生成lanelet右边界错误")
            return
        linestring_Type(left_linestring, lane["L_EdgeId"])            
        linestring_Type(right_linestring, lane["R_EdgeId"])
        lanelet = Lanelet(getId(), left_linestring, right_linestring)
        lanelet_Type(lanelet, lane)
        regulator_Element(lane, lanelet, projector)
        lanelet.attributes["speed_limit"] = str(lane["Speed"])
        map.add(lanelet)
        # print("%d" %lane['Speed'])
        # if lane['lane_type'] == 5:
        #     lanelet.attributes["type"] = "lanelet"
        #     lanelet.attributes["subtype"] = "emergency_lane"
        #     lanelet.attributes["speed_limit"] = "lane['Speed']"
        # elif lane['lane_type'] == 40:
        #     lanelet.attributes["type"] = "lanelet"
        #     lanelet.attributes["subtype"] = "crosswalk"
        #     lanelet.attributes["speed_limit"] = "lane['Speed']"
        #     lanelet.attributes["location"] = "urban"
        #     lanelet.attributes["one_way"] = "no"
        # elif lane['lane_type'] == 30:
        #     lanelet.attributes["type"] = "lanelet"
        #     lanelet.attributes["subtype"] = "shared_walkway"
        #     lanelet.attributes["speed_limit"] = "lane['Speed']"
        #     lanelet.attributes["location"] = "urban"
        #     lanelet.attributes["one_way"] = "yes"
        # else:
        #     lanelet.attributes["type"] = "lanelet"
        #     lanelet.attributes["subtype"] = "road"
        #     lanelet.attributes["speed_limit"] = "lane['Speed']"
        #     lanelet.attributes["location"] = "urban"
        #     lanelet.attributes["one_way"] = "yes"
         
    return map




if __name__ == '__main__':
    shp2lanelet2()
