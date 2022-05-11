import shapefile  # 使用pyshp
from matplotlib import pyplot as plt
file = shapefile.Reader("/home/yezi/zhy/map_change/shp2lanelet2/maps/demo_shp/demo_shp_20211217/Junction.shp")

border_shape = file
print(str(border_shape.shapeType))  # 输出shp类型
# 通过创建reader类的对象进行shapefile文件的读取
# border_points
border_points = []
border = border_shape.shapes() # 读取几何数据
# .shapes()读取几何数据信息，存放着该文件中所有对象的几何数据
# border是一个列表
for bor in border:
    border_points.append(bor.points)
    print(bor.points)
#     x, y = zip(*bor.points)
# # x=(x1,x2,x3,…)
# # y=(y1,y2,y3,…)

    # fig, ax = plt.subplots()  # 生成一张图和一张子图
    # # plt.plot(x,y,'k-') # x横坐标 y纵坐标 ‘k-’线性为黑色
    # plt.plot(x, y, color='#6666ff', label='fungis')  # x横坐标 y纵坐标 ‘k-’线性为黑色
    # ax.grid()  # 添加网格线
    # ax.axis('equal')
    # plt.show()

# border_points = border[0].points
# 返回第1个对象的所有点坐标
# border_points = [(x1,y1),(x2,y2),(x3,y3),…]

