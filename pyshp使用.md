# python-shapefile库读取shapefile文件信息



shapefile是GIS中非常重要的一种数据类型，在[ArcGIS](https://so.csdn.net/so/search?q=ArcGIS&spm=1001.2101.3001.7020)中被称为要素类(Feature Class)，主要包括点(point)、线(polyline)和多边形(polygon)。



## 1. 开发准备



安装命令：pip install pyshp

使用导入：import shapefile



## 2. Shapefile文件的读操作



通过创建Reader类的对象进行shapefile文件的读操作。

```python
file = shapefile.Reader('shapefile name')
```



“几何数据”通过Reader类的shapes( )和[shape](https://so.csdn.net/so/search?q=shape&spm=1001.2101.3001.7020)( )方法来读取，二者的区别在于：shapes()方法不需要指定参数，其返回值是一个列表，包含该文件中所有的"几何数据"对象，而shape( )方法则需要通过指定参数返回所需要的"几何数据"对象。

```python
shape = file.shape(i)#读取第i+1个要素，索引序列从0开始(参数是整数类型)
shapes = file.shapes()#读取全部要素
```



完整的读取操作

```python
# -*- coding: utf-8 -*-
import shapefile# 使用pyshp
file = shapefile.Reader("E://arcgisData//行政区划数据//省界_region.shp")#读取
#读取元数据
print(str(file.shapeType))  # 输出shp类型
print(file.encoding)# 输出shp文件编码
print(file.bbox)  # 输出shp的文件范围（外包矩形）
print(file.numRecords)  # 输出shp文件的要素数据
print(file.fields)# 输出所有字段信息
# print(file.records())  # 输出所有属性表
```



shp类型信息

![img](https://img-blog.csdnimg.cn/20200115140720922.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNDQxODk2,size_16,color_FFFFFF,t_70)



变长记录的内容由图形的类型决定。Shapefile支持以下的图形类型：

| 值   | 图形类型                        | 字段                                                         |
| ---- | ------------------------------- | ------------------------------------------------------------ |
| 0    | 空图形                          | 无                                                           |
| 1    | Point（点）                     | X, Y                                                         |
| 3    | Polyline（折线）                | （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点 |
| 5    | Polygon（多边形）               | （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点 |
| 8    | MultiPoint（多点）              | （最小包围矩形）MBR，点的数目，所有点                        |
| 11   | PointZ（带Z与M坐标的点）        | X, Y, Z, M                                                   |
| 13   | PolylineZ（带Z或M坐标的折线）   | *必须的*: （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点，Z坐标范围, Z坐标数组 *可选的*: M坐标范围, M坐标数组 |
| 15   | PolygonZ（带Z或M坐标的多边形）  | *必须的*: （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点，Z坐标范围, Z坐标数组 *可选的*: M坐标范围, M坐标数组 |
| 18   | MultiPointZ（带Z或M坐标的多点） | *必须的*: （最小包围矩形）MBR，点的数目，所有点， Z坐标范围, Z坐标数组 *可选的*: M坐标范围, M坐标数组 |
| 21   | PointM（带M坐标的点）           | X, Y, M                                                      |
| 23   | PolylineM（带M坐标的折线）      | *必须的*: （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点 *可选的*: M坐标范围, M坐标数组 |
| 25   | PolygonM（带M坐标的多边形）     | *必须的*: （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点 *可选的*: M坐标范围, M坐标数组 |
| 28   | MultiPointM（带M坐标的多点）    | *必须的*: （最小包围矩形）MBR，点的数目，所有点 *可选的*: M坐标范围, M坐标数组 |
| 31   | MultiPatch                      | *必须的*: （最小包围矩形）MBR，组成部分数目，点的数目，所有组成部分，所有点，Z坐标范围, Z坐标数组 *可选的*: M坐标范围, M坐标数组 |



 shp属性表字段信息

| 字段索引 | 字段类型                                       |
| -------- | ---------------------------------------------- |
| C        | 字符，文字                                     |
| N        | 数字，带或不带小数                             |
| F        | 浮动（与“N”相同）                              |
| L        | 逻辑，表示布尔值True / False值                 |
| D        | 日期                                           |
| M        | 备忘录，在GIS中没有意义，而是xbase规范的一部分 |



展示单个要素

```python
import shapefile  # 使用pyshp
from matplotlib import pyplot as plt
file = shapefile.Reader("E://arcgisData//行政区划数据//省界_region.shp")

border_shape = file
# 通过创建reader类的对象进行shapefile文件的读取
# border_points
border = border_shape.shapes() # 读取几何数据
# .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
# border是一个列表
border_points = border[0].points
print(border_points)# 返回第1个对象的所有点坐标
# border_points = [(x1,y1),(x2,y2),(x3,y3),…]

x, y = zip(*border_points)
# x=(x1,x2,x3,…)
# y=(y1,y2,y3,…)

fig, ax = plt.subplots()  # 生成一张图和一张子图
# plt.plot(x,y,'k-') # x横坐标 y纵坐标 ‘k-’线性为黑色
plt.plot(x, y, color='#6666ff', label='fungis')  # x横坐标 y纵坐标 ‘k-’线性为黑色
ax.grid()  # 添加网格线
ax.axis('equal')
plt.show()
```



展示效果：

![img](https://img-blog.csdnimg.cn/20200115142121264.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNDQxODk2,size_16,color_FFFFFF,t_70)



## 3. shapefile文件的写操作 

- 创建点状要素类

  ```python
  import shapefile  # 使用pyshp
  file = shapefile.Writer("E://arcgisData//test//站点_2")#新建数据存放位置
  #创建两个字段
  file.field('FIRST_FLD')
  file.field('SECOND_FLD','C','40')     #'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40
  
  file.point(1,1)
  file.record('First','Point')
  
  file.point(300,10)
  file.record('Second','Point')
  
  file.point(400,30)
  file.record('Third','Point')
  
  file.point(200,200)
  file.record('Fourth','Point')
  
  #写入数据
  file.close()
  ```

- 创建线状要素类

  ```python
  import shapefile  # 使用pyshp
  file = shapefile.Writer("E://arcgisData//test//polyline")#新建数据存放位置
  #创建两个字段
  file.field('FIRST_FLD')
  file.field('SECOND_FLD','C','40')     #'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40
  
  file.line([[[1,5],[5,5],[5,1],[3,3],[1,1]]])
  file.record('First','polyline')
  file.line([[[1,500],[300,30],[1,16]]])
  file.record('Second','polyline')
  
  #写入数据
  file.close()
  ```

- 创建面状要素类

  ```python
  import shapefile  # 使用pyshp
  file = shapefile.Writer("E://arcgisData//test//polygon")#新建数据存放位置
  #创建两个字段
  file.field('FIRST_FLD')
  file.field('SECOND_FLD','C','40')     #'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40
  
  file.poly([[[1,5],[5,5],[5,1],[3,3],[1,1]]])
  file.record('First','polygon')
  
  file.poly([[[1,500],[300,30],[1,16],[1,500]]])
  file.record('Second','polygon')
  
  #写入数据
  file.close()
  ```