import shapefile  # 使用pyshp
from matplotlib import pyplot as plt
file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/Junction.shp")

border_shape = file
# 通过创建reader类的对象进行shapefile文件的读取
# border_points
border = border_shape.shapes() # 读取几何数据
# .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
# border是一个列表
border_points = border[0].points
# for value in border_points:
#     print(value)
print(border_points[0][0])# 返回第1个对象的所有点坐标
print(border_points)# 返回第1个对象的所有点坐标
print(border_points[0][0])# 返回第1个对象的lon