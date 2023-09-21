import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon



def make_arc_poly(center_point, radius, alpha, theta):
    centerx, centery = center_point[0], center_point[1]
    base = 90 - alpha
    base_start = base - theta / 2
    base_end = base + theta / 2

    # The coordinates of the arc by handmade
    theta_arc = np.radians(np.linspace(base_start, base_end, 1000))

    x = centerx + radius * np.cos(theta_arc)
    y = centery + radius * np.sin(theta_arc)

    core = np.array([centerx, centery])
    tmp = np.column_stack([x, y])

    arc_points = np.vstack((core, tmp, core))

    '''Key To Make Arc_Polygon'''
    arc_polygon = Polygon(arc_points)

    return arc_polygon

def get_pos_from_pose(cur):

    image_number = f"{cur:06d}"  # 格式化为三位数，例如001、002等
    rgb_image_path_cur = f"./seq-01/frame-{image_number}.color.png"
    depth_image_path_cur = f"./seq-01/frame-{image_number}.depth.png"
    poses_path1_cur = f"./seq-01/frame-{image_number}.pose.txt"

    # 假设camera_to_world是一个4x4的矩阵
    camera_to_world = np.loadtxt(poses_path1_cur)

    # 1. 获取camera在world坐标系下的位置
    o_w = camera_to_world[:3, 3]

    # 2. 获取坐标轴方向
    r_w = camera_to_world[:3, 2]

    return [o_w[0],o_w[2]],[r_w[0],r_w[2]]
    #return o_w,r_w

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

def draw_fov(x_1,y_1,x_2,y_2,x_in,y_in,IoU):
    fig, ax = plt.subplots()

    ax.fill(x_1, y_1, color='#0000ff', alpha=0.3)

    ax.fill(x_2, y_2, color='#00ccff', alpha=0.3)

    ax.fill(x_in, y_in, color='#ffccff', alpha=0.6)

    ax.set_aspect('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f"The IoU is {IoU :.2f}%")
    plt.grid(True)


def draw_fov_plus(x_1, y_1, x_2, y_2, x_in, y_in, IoU):
    fig, ax = plt.subplots()

    ax.fill(x_1, y_1, color='#0000ff', alpha=0.3)

    ax.fill(x_2, y_2, color='#00ccff', alpha=0.3)

    ax.fill(x_in, y_in, color='#ffccff', alpha=0.6)

    ax.set_aspect('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f"The IoU is {IoU :.2f}%")
    plt.grid(True)
    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)

    return img


def calculate_fov_between_check(cur,ref):
    theta = 60
    radius = 5.85

    o_w0, r_w0 = get_pos_from_pose(cur=cur)
    alpha_0 = angle_with_y_axis(r_w0)

    o_w1, r_w1 = get_pos_from_pose(cur=ref)
    alpha_1 = angle_with_y_axis(r_w1)

    arc_polygon1 = make_arc_poly(center_point=o_w0, radius=radius, alpha=alpha_0, theta=theta)
    arc_polygon2 = make_arc_poly(center_point=o_w1, radius=radius, alpha=alpha_1, theta=theta)
    '''Make Intersection'''
    new_poly = arc_polygon1.intersection(arc_polygon2)
    IoU = new_poly.area * 100 / (arc_polygon1.area + arc_polygon2.area - new_poly.area)

    x_1, y_1 = arc_polygon1.exterior.xy
    x_2, y_2 = arc_polygon2.exterior.xy
    x_in, y_in = new_poly.exterior.xy
    # draw_fov(x_1,y_1,x_2,y_2,x_in,y_in,IoU)






    return IoU

def calculate_fov_seq(cur):
    all_arr = []
    for ref in range(1000):
        print(f"Make: {ref} ...")
        all_arr.append(calculate_fov_between_check(cur,ref))

    return all_arr



def calculate_fov_and_save_npz():
    all_arr = []
    for num in range(0,1):
        all_arr.append(calculate_fov_seq(cur=num))
    result = np.stack(all_arr)
    np.savez('result_fov.npz', result/100)
    print("Finished Calulate And Save Into NPZ!")

if __name__ == "__main__":

    calculate_fov_and_save_npz()







