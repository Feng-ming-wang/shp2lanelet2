#!/usr/bin/env python
from operator import is_
import shapefile  # 使用pyshp
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, GPSPoint
from lanelet2.projection import UtmProjector

from matplotlib import pyplot as plt

#车道边界线
EdgeLink_file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/HD_EdgeLink.shp") 

#车道边界线节点
EdgeNode_file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/HD_EdgeNode.shp") 

#车道中心线
LaneLink_file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/HD_LaneLink.shp") 

#转换后的osm文件路径
lanelet2_path = os.path.join("/home/yezi/zhy/map_change/shp2lanelet2/test/lanelet2_map.osm")

EdgeNode = [] # 存储车道边界线节点属性
EdgeLink = [] # 存储车道边界线属性
LaneLink = [] # 存储车道中心线属性
EdgeNodeId = [] #存储已经使用的节点的ID
EdgeLineId = [] #存储已经使用的车道边界线的ID

def shp2lanelet2():
    map = LaneletMap() 
    read_EdgeNode(EdgeNode_file) 
    read_EdgeLink(EdgeLink_file)
    read_LaneLink(LaneLink_file)
    origin_lon = EdgeNode[0]['lon']
    origin_lat = EdgeNode[0]['lat']
    # print(origin_lon)
    projector = UtmProjector(lanelet2.io.Origin(origin_lat, origin_lon)) 
    for lane in LaneLink:
        print("-----------------------------LaneLink--------------------------------------------")
        print(lane)
        left_linestring = write_lane(lane, projector, 'L_EdgeId')
        if left_linestring == -1:
            print("生成lanelet左边界错误")
            return

        right_linestring = write_lane(lane, projector, 'R_EdgeId')
        if right_linestring == -1:
            print("生成lanelet右边界错误")
            return
                    
        lanelet = Lanelet(getId(), left_linestring, right_linestring)
        map.add(lanelet)

    lanelet2.io.write(lanelet2_path, map, projector)
    mapLoad, errors = lanelet2.io.loadRobust(lanelet2_path, projector)
    assert not errors
    assert mapLoad.laneletLayer.exists(lanelet.id)


        
 


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
    
# 获取节点id lat lon信息
def get_node(node_id):
    nodes = []
    for node in EdgeNode:
        # print(node['id'])
        if node_id == node['id']:
            nodes.append(node)
            break
    return nodes
        
   


# 读取车道边界线节点信息
def read_EdgeNode(file_path):
    border = file_path.shapeRecords() # 读取ID属性
    border_p = file_path.shapes() # 读取经纬度
    i = 0
    print("----------------EdgeNode--------------------")
    while i < len(border):
        node = {'id':border[i].record[1], 'lon':border_p[i].points[0][0], 'lat':border_p[i].points[0][1]}
        # print(node['lon'])
        i = i + 1
        print(node)
        EdgeNode.append(node)

# 读取车道边界线信息
def read_EdgeLink(file_path):
    border = file_path.shapeRecords() # 读取ID等属性
    i = 0
    print("----------------EdgeLink--------------------")
    while i < len(border):
        # edge = {'id':border[i].record[1], 'SE_NodeId':border[i].record[4], 'EE_NodeId':border[i].record[5]}
        edge = {'id':border[i].record[1], 'SE_NodeId':border[i].record[4], 'EE_NodeId':border[i].record[5], 'Edge_type':2, 'Edge_cross':1} # 目前demo数据无type及跨越方向信息
        # edge = {'id':border[i].record[1], 'SE_NodeId':border[i].record[4], 'EE_NodeId':border[i].record[5], 'Edge_type':border[i].record[5], 'Edge_cross':border[i].record[5]} # 目前demo数据无type及跨越方向信息
        i = i + 1
        print(edge)
        EdgeLink.append(edge)

# 读取车道中心线信息
def read_LaneLink(file_path):
    border = file_path.shapeRecords() # 读取ID等属性
    i = 0
    print("----------------LaneLink--------------------")
    while i < len(border):
        # lane = {'id':border[i].record[1], 'L_EdgeId':border[i].record[6], 'R_EdgeId':border[i].record[7]}
        lane = {'id':border[i].record[1], 'L_EdgeId':border[i].record[6], 'R_EdgeId':border[i].record[7], 'Direction':2, 'type':1} # 目前demo数据无type及direction信息
        # lane = {'id':border[i].record[1], 'L_EdgeId':border[i].record[6], 'R_EdgeId':border[i].record[7], 'Direction':border[i].record[7], 'type':border[i].record[7]} # 目前demo数据无type及direction信息
        i = i + 1       
        print(lane)
        LaneLink.append(lane)

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

# 判断是否生成lanelet node,并返回node
def write_node(node_id, project):
    # print("-----------------------------------write_node----------------------------------")
    # print(node_not_exit(node_id))
    if node_not_exit(node_id):
        # print("未生成该点，新生成该点")
        node = get_node(node_id)
        print("shp node")
        print(node)
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
            print("节点编号 node")
            print(node_id, point)
            return point
        else:
            print("无法获取shp节点信息")
            return -1
    else:
        # print("已生成该点，获取该点信息")
        for id in EdgeNodeId:
            if node_id == id['shp_id']:
                print("节点编号 node")
                print(node_id, id['lanelet2_node'])
                return id['lanelet2_node']

 # 判断是否生成lanelet linestring,并返回linestring
def write_linestring(edge_id, start_node, end_node):
    # print("---------------------------------write_linestring-------------------------------")
    # print(linestring_not_exit(edge_id))
    if linestring_not_exit(edge_id):
        print("line不存在")
        # print(edge_id)
        linestring = LineString3d(getId(), [start_node, end_node]) # poit_id:生成的node的Id       
        print("边界线编号 linesting")
        print(edge_id, linestring)
        used_edgeLinkId = {'shp_id':edge_id, 'lanelet2_linestring':linestring}
        EdgeLineId.append(used_edgeLinkId)        
        return linestring
    else:
        print("line已存在")
        for id in EdgeLineId:
            if edge_id == id['shp_id']:
                print("边界线编号 linesting")
                print(edge_id, id['lanelet2_linestring'])
                return id['lanelet2_linestring']

# 生成lanelet2左/右车道线
def write_lane(lane, projector, flag):
    print("-----------------------------Write_Lane---------------------------")
    leftedge_id = get_Edge(lane, flag) # 获取左边界线信息
    # print(leftedge_id)
    if leftedge_id == -1:
        print("车道线左边界ID读取错误")
        return -1
    else:
        print("边界编号： %d" %leftedge_id)
        startnode_id = get_ENId(leftedge_id, 'SE_NodeId') # 获取左边界起始节点编号
        if startnode_id == -1:
            print("车道线左边界起始节点ID读取错误")
            return -1
        else:
            start_node = write_node(startnode_id, projector) # 获取lanelet2起始节点信息
            # print(start_node)
            endnode_id = get_ENId(leftedge_id, 'EE_NodeId')
            if endnode_id == -1:
                print("车道线左边界终止节点ID读取错误") 
                return -1
            else:   
                end_node = write_node(endnode_id, projector)
                # print(end_node)
                left_linestring = write_linestring(leftedge_id, start_node, end_node)
                # print(left_linestring)
                return left_linestring


if __name__ == '__main__':
    shp2lanelet2()

