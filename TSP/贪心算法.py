
import math
import random
import matplotlib.pyplot as plt
import time
time_start = time.time()  # 记录开始时间
# function()   执行的程序


citys = []
'''读取数据,记录城市坐标'''
with open('st70.tsp') as f:
    while True:
        line = f.readline()

        if line.startswith("NODE_COORD_SECTION"):
            break
    # 记得加上换行符号
    while line != "EOF\n":
        line = f.readline()
        if line == "EOF\n":
            break
        # 分割成多个字符串
        line = line.split(' ')
        # print(line)
        nums = []
        for num in line[1:]:
            nums.append(int(num))
        citys.append(nums)

#城市数量
city_count = len(citys)

# 迭代次数
num_iter = 1000
#城市距离矩阵
dist_map = [[0]*(len(citys)) for i in range(len(citys)) ]

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

                dist_map[i][j] = 0

'''计算城市间的距离'''
cacl_dist_map(citys)

def len_path(path):
    path_dis = 0
    for i in range(len(path) - 1):
        path_dis += dist_map[path[i]][path[i+1]]
    return path_dis
#记录每次迭代的最好值
dist_best = [0]*num_iter
#记录最好路径
path_best =[[0]*num_iter for i in range(num_iter)]
#迭代次数
cnt = 0
#记录每次距离


path = []

while cnt < num_iter:
    path = []
    dis_path = 0
    notVis = list(range(city_count))
    random.shuffle(notVis)
    start_city = random.choice(notVis)
    notVis.remove(start_city)
    last_city = notVis[len(notVis)-1]
    cur_city = start_city
    path.append(start_city)
    while notVis:
        MIN = 999999
        index = 0

        for next_city in notVis:
            if dist_map[cur_city][next_city] < MIN:
                MIN = dist_map[cur_city][next_city]
                index = next_city
        path.append(index)
        dis_path += dist_map[cur_city][index]
        # dis_path += dist_map[cur_city][index]
        # if len(path) >= 2:
        #     min_dist = float('inf')
        #     best_insert_pos = None
        #     for i in range(len(path)):
        #         temp_path = path[:i] + [index] + path[i:]
        #         temp_dist = len(temp_path)
        #         if temp_dist < min_dist:
        #             min_dist = temp_dist
        #             best_insert_pos = i
        #     path.insert(best_insert_pos, index)
        #     dis_path = len_path(path)
        # else:
        #     path.append(index)
        #     dis_path = len_path(path)
        notVis.remove(index)
        cur_city = index
    path_best[cnt] = path
    dis_path += dist_map[last_city][start_city]
    dist_best[cnt] = dis_path
    if cnt >=1 and dist_best[cnt-1] < dist_best[cnt]:
        dist_best[cnt] = dist_best[cnt-1]
        path_best[cnt] = path_best[cnt-1]
    cnt += 1
print("贪心算法的最优路径",path_best[cnt-1])
print("迭代", cnt,"次后","贪心算法求得最优解",dist_best[cnt-1])
# print(dist_best)
time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
print(time_sum)

'''绘制路径图'''
fig, ax = plt.subplots()  # 创建绘图对象
x = []
y = []
for i in path_best[num_iter - 1]:  # 遍历最优路径,提取城市x、y坐标
    x.append(citys[i][0])
    y.append(citys[i][1])
x.append(citys[path_best[num_iter - 1][0]][0])
y.append(citys[path_best[num_iter-1][0]][1])
ax.plot(x, y, 'r-')  # 绘制路径连线,红色
ax.scatter(x, y)  # 绘制城市散点

for i in range(len(x)):
    ax.annotate(i, (x[i], y[i]))  # 在各城市坐标处添加序号标注


plt.title("Ant Colony Optimization Path")
plt.xlabel("x coordinate")
plt.ylabel("y coordinate")
plt.show()  # 显示图像


# print(dis_path)
plt.figure()
plt.plot(range(len(dist_best)), dist_best)
plt.xlabel('Iteration')
plt.ylabel('Path Length')
plt.title('Optimization Process')
plt.show()
