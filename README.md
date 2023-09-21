# CalculateFOV
# Calculate2D

### 使用Shapely创建多边形

用于创建多边形，并在内部实现了计算面积的功能，个人认为只要给出需要绘制的图形轮廓，即可计算。

[The Shapely User Manual — Shapely 2.0.1 documentation](https://shapely.readthedocs.io/en/stable/manual.html#polygons)

对于圆锥计算也是如此，给出起点终点以及弧上的点就能构造圆弧。

```python
arc_polygon1 = make_arc_poly(center_point=o_w0, radius=radius, alpha=alpha_0, theta=theta)
arc_polygon2 = make_arc_poly(center_point=o_w1, radius=radius, alpha=alpha_1, theta=theta)
'''Make Intersection'''
new_poly = arc_polygon1.intersection(arc_polygon2)
IoU = new_poly.area * 100 / (arc_polygon1.area + arc_polygon2.area - **new_poly.area**)
```

## 获得相机在世界坐标系下坐标和朝向

[相机位置和朝向计算(世界坐标系下)_已知图像平面 相机朝向 求图像_夕阳染色的坡道的博客-CSDN博客](https://blog.csdn.net/weixin_43851636/article/details/126782704)

```python
camera_to_world = np.loadtxt(poses_path1_cur)
# 1. 获取camera在world坐标系下的位置
o_w = camera_to_world[:3, 3]
# 2. 获取坐标轴方向
r_w = camera_to_world[:3, 2]
'''这里取了选择X，Z坐标作为2D平面投影'''
return [o_w[0],o_w[2]],[r_w[0],r_w[2]]
```

## 绘制圆弧所需要的参数计算

[](https://arxiv.org/pdf/2103.06638.pdf)

参考文章4.1节2D Field-of-View overlap

我在处理角度部分做了一些工作，首先是计算alpha，构建如文章描述的角度需要进行调整

```python
def angle_with_y_axis(pos):
    x,y = pos
    if x == 0:
        if y > 0:
            return 0
        elif y < 0:
            return 180
        else:
            return 0  # 原点
    # 第一象限
    if x > 0 and y >= 0:
        return 90 - math.degrees(math.atan(y / x))

    # 第二象限
    if x < 0 and y > 0:
        return 270 + math.degrees(math.atan(y / abs(x)))

    # 第三象限
    if x < 0 and y <= 0:
        return 270 - math.degrees(math.atan(y / x))

    # 第四象限
    if x > 0 and y < 0:
        return 90 + math.degrees(math.atan(abs(y) / x))
```

在这个函数下也有所调整

```python
def make_arc_poly(center_point, radius, alpha, theta):
    centerx, centery = center_point[0], center_point[1]
    **base = 90 - alpha
    base_start = base - theta / 2
    base_end = base + theta / 2**
```

