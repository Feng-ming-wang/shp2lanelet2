import shapefile  # 使用pyshp
file = shapefile.Writer("/home/yezi/zhy/map_change/shp2lanelet2/maps/站点_2")#新建数据存放位置
#创建两个字段
file.field('FIRST_FLD')
file.field('SECOND_FLD','C','40')     #'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40

file.pointz(1,1,1)
file.record('First','Point')

file.pointz(300,10,1)
file.record('Second','Point')

file.pointz(400,30,1)
file.record('Third','Point')

file.pointz(200,200,1)
file.record('Fourth','Point')

#写入数据
file.close()