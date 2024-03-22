import heapq
import math
import random

from matplotlib import pyplot as plt

citys = []
#读入数据
with open('st70.tsp') as f:
    while True:
        line = f.readline()

        if line.startswith("NODE_COORD_SECTION"):
            break
    #开始读入需要的数据
    while line != "EOF\n":
        line = f.readline()
        if line == "EOF\n":
            break
        #分割成多个字符串
        line = line.split(' ')
        # print(line)
        nums = []

        for num in line[1:]:
            nums.append(int(num))
        citys.append(nums)
# print(citys)

#参数
#城市数目
city_count = len(citys)
#城市距离矩阵
dist_map = [[0]*(len(citys)) for i in range(len(citys)) ]

#迭代次数
iter_num = 500
iter = 0
#保存最优距离
dis_min = 999999
#保存最优路径
path_best = []
# 存储每次迭代得到的路径长度
path_lens = []
'''计算城市距离'''
def cacl_dist(i, j):
    return math.sqrt((citys[i][0] - citys[j][0])**2+ (citys[i][1] - citys[j][1])**2)

'''城市距离矩阵'''
def cacl_dist_map(citys):
    for i in range(len(citys)):
        for j in range(i,len(citys)):
            if(i!=j):
             dist_map[i][j] = dist_map[j][i] = cacl_dist(i,j)
            else:
                # 设置一个很大的值，后面翻转过来相当于自己的可见度为0
                dist_map[i][j] = 0

'''计算城市间的距离'''
cacl_dist_map(citys)
# print(dist_map)
#计算路径的距离和
def len_path(path):
    path_dis = 0
    for i in range(len(path) - 1):
        path_dis += dist_map[path[i]][path[i+1]]
    return path_dis + dist_map[path[0]][path[len(path) -1]]
#用于交换产生路径的邻域
def change_path(path,i,j):
    path_new = []
    for p in path:
        path_new.append(p)
    a = path_new[i]
    path_new[i] = path_new[j]
    path_new[j] = a
    return path_new
#爬山法
def pashan(path):
    old_len = len_path(path)
    next_path = path
    cnt = 0
    while cnt < len(path)**2:
        #随机交换
        i = random.randint(0, len(path) - 1)
        j = random.randint(0, len(path) - 1)
        path_new = change_path(path, i, j)
        cnt = cnt+1
        #更新数据
        if len_path(path_new) < old_len:
            old_len = len_path(path_new)
            next_path = path_new
    return next_path
#迭代主循环
while iter < iter_num:

    cities = list(range(city_count))
    random.shuffle(cities)
    path = []
    for  it in cities:
        path.append(it)
    path_goal = pashan(path)
    dis = len_path(path_goal)
    if dis_min > dis:
        dis_min = dis
        path_best = []
        for it in path_goal:
            path_best.append(it)
    path_lens.append(len_path(path_best))  # 记录路径长度

    iter += 1
dis_min = min(path_lens)
print( '共迭代',iter_num,'次，搜索到这种方法的最优解')
print('最优路径：',path_best)
print('最短距离：',len_path(path_best))


'''绘制路径图'''
fig, ax = plt.subplots()  # 创建绘图对象
x = []
y = []
for i in path_best:  # 遍历最优路径,提取城市x、y坐标
    x.append(citys[i][0])
    y.append(citys[i][1])

ax.plot(x, y, 'r-')  # 绘制路径连线,红色
ax.scatter(x, y)  # 绘制城市散点

for i in range(len(x)):
    ax.annotate(i, (x[i], y[i]))  # 在各城市坐标处添加序号标注

plt.title("Ant Colony Optimization Path")
plt.xlabel("x coordinate")
plt.ylabel("y coordinate")
plt.show()  # 显示图像

# 绘制路径长度变化趋势图
plt.figure()
plt.plot(range(len(path_lens)), path_lens)
plt.xlabel('Iteration')
plt.ylabel('Path Length')
plt.title('Path Optimization Process')
plt.show()