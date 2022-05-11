import shapefile  # 使用pyshp
from matplotlib import pyplot as plt
file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/HD_LaneNode.shp")

border_shape = file
# 通过创建reader类的对象进行shapefile文件的读取
# border_points
border = border_shape.shapeRecords() # 读取几何数据
border_p = border_shape.shapes() # 读取几何数据
# .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
# border是一个列表
border_shapetype = border[0].shape.shapeType
print(border_shapetype)# 返回第1个对象的shp类型
border_points = border_p[0].points
print(border_points)# 返回第1个对象的所有点坐标
# border_points = [(x1,y1),(x2,y2),(x3,y3),…]
print(border[0].record[1])# 返回第1个对象的”属性数据”的第1个属性值 -- ID