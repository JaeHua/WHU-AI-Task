
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

    # nums = [int(num) for num in line.split()[1:]]#特殊切片用法
    # citys.append(nums)

# print(citys)
#城市数量
city_count = len(citys)
# 信息素初始值
init_pheromone = 0
# 信息素挥发率
rho = 0.5
# 信息素重要程度参数
# alpha = 3
# # 期望值启发因子
# beta = 5
# 蚁群数量
num_ants = 50
# 迭代次数
num_iter = 1000
#城市距离矩阵
dist_map = [[0]*(len(citys)) for i in range(len(citys)) ]
#Q为常数
Q = 100
# #贪心初始化的路径
# tanxin = [30, 68, 34, 69, 12, 28, 35, 0, 22, 46, 15, 36, 57, 49, 50, 55, 64, 63, 10, 66, 47, 53, 61, 32, 33, 20, 11, 59, 51, 9, 4, 52, 5, 40, 42, 16, 8, 39, 60, 38, 44, 24, 45, 26, 67, 43, 29, 19, 13, 27, 7, 25, 48, 54, 18, 6, 31, 2, 41, 17, 3, 1, 23, 14, 56, 65, 62, 21, 58, 37]
# #信息矩阵
pheromone = [[1.0]*len(citys) for i in range(len(citys))]
# for i in range(len(tanxin)-1):
#     pheromone[tanxin[i]][tanxin[i+1]] = 100
#候选集列表,存放每一只蚂蚁的路径
candidate = [[0]*len(citys) for i in range(num_ants) ]
#记录每次距离
dis_path = []
'''计算城市距离'''
def cacl_dist(i, j):
    return math.sqrt((citys[i][0] - citys[j][0])**2+ (citys[i][1] - citys[j][1])**2)
#print(cacl_dist(0,1))
# print(len(citys))


'''城市距离矩阵'''
def cacl_dist_map(citys):
    for i in range(len(citys)):
        for j in range(i,len(citys)):
            if(i!=j):
             dist_map[i][j] = dist_map[j][i] = cacl_dist(i,j)
            else:
                # 设置一个很大的值，后面翻转过来相当于自己的可见度为0
                dist_map[i][j] = 10000

'''计算城市间的距离'''
cacl_dist_map(citys)
# print(dist_map)
# print(pheromone)
# print(candidate[0][0])

#能见度矩阵
vispos = [[0]*len(citys) for i in range(len(citys))]
'''计算可见度矩阵'''
for i in range(len(citys)):
  for j in range(i+1, len(citys)):
    vispos[i][j] = vispos[j][i] = 1 / dist_map[i][j]
# print(vispos)
# #生成一些的城市访问顺序
# randon_citys = list(range(len(citys)))
# print(randon_citys)

#记录每次迭代的最好值
dist_best = [0]*num_iter
#记录最好路径
path_best =[[0]*num_iter for i in range(num_iter)]
#迭代次数
cnt = 0
'''进行迭代'''
while cnt < num_iter:
    '''城市初始点'''
    beta = [4 + 4 * random.random() for _ in range(num_ants)]
    alpha = [3 - random.random() * min(3, 2 + beta[i] / 3) for i in range(num_ants)]
    if num_ants <= city_count:
        cities = list(range(city_count))
        #打乱列表
        random.shuffle(cities)
        # print(cities)
        # 设置起点城市
        for i in range(num_ants):
            candidate[i][0] = cities[i]

            # print(candidate[i][0])
    else:
        '''蚂蚁数量大于城市的情况'''
        m = num_ants - city_count
        cities = list(range(city_count))
        random.shuffle(cities)
        # 设置起点城市
        for i in range(city_count):
            candidate[i][0] = cities[i]
        for i in range(m):
            #随机等概率选择一个
            candidate[city_count + i].append(random.choice(cities))
    # 每只蚂蚁走的距离
    length = [0]*num_ants
    # print(length)
    '''访问后续城市'''
    for i in range(num_ants):

        # 未访问城市
        invis = list(range(city_count))
        # print(invis)
        vis = candidate[i][0]
        # print(vis)
        # print(candidate)
        # print(vis)
        # 移去现在所在城市
        invis.remove(vis)
        # print(invis)
        '''除去起始点，继续遍历city_count - 1次'''
        for j in range(1,city_count):
            #可能性
            posibility = []
            #没访问的城市计算访问可能性
            for k in range(len(invis)):
                #信息素浓度
                pher = pheromone[vis][invis[k]]
                posibility.append(pow(pher,alpha[i])*pow(vispos[vis][invis[k]],beta[i]))
            # print(posibility)
            #轮盘赌
            total = 0
            for p in posibility:
                total += p
            posi = []
            summ = 0
            #进行切分
            for p in posibility:
                summ += p
                posi.append(summ / total)
            # if i==0 and j ==1:print(posi)
            #生成一个0~1的随机数，用于轮盘赌
            num = random.random()
            for it in range(len(posi)):
              posi[it] -= num
            # print(posi)
            # if i ==0 and j == 1:print(posi)
            # 记录第几个为0
            index_zero = 0
            #找到第一个大于0的
            for p in posi:
                if p > 0:
                    break
                index_zero = index_zero+1
            #k为要选择的
            k = invis[index_zero]
            # print(j)
            #第i只蚂蚁在第j个城市的时候选择了k作为下一个城市
            candidate[i][j] = k
            #移除访问的k
            invis.remove(k)
            #距离更新
            length[i] += dist_map[vis][k]
            #现在位于k城市,记得更新!!!
            vis = k
        # 最后一个城市和第一个城市,不要落下了
        length[i] += dist_map[vis][candidate[i][0]]

    '''更新路径'''
    if cnt == 0:
        min_dist_index = 0
        dist_best[cnt] = min(length)
        #找到最小的length下标
        for it in length:
            if it != min(length):
                min_dist_index = min_dist_index + 1
            else:break
        #相当于把第min_dist_index那一行，也就是路径copy过来，比较简便
        path_best[cnt] = candidate[min_dist_index].copy()
        dis_path.append(length[min_dist_index])
    else:
        #同上的操作
        if min(length) > dist_best[cnt - 1]:
            dist_best[cnt] = dist_best[cnt-1]
            path_best[cnt] = path_best[cnt-1].copy()

        else:
            #进行更新最小值与最佳路径
            min_dist_index = 0
            dist_best[cnt] = min(length)
            for it in length:
                if it != min(length):
                    min_dist_index = min_dist_index + 1
                else:
                    break
            path_best[cnt] = candidate[min_dist_index].copy()


    '''信息增量矩阵'''
    add_pheromone = [[1] * len(citys) for i in range(len(citys))]

    for ii in range(num_ants):

        for j in range(city_count - 1):
            add_pheromone[candidate[ii][j]][candidate[ii][j+1]] += Q/length[ii]
        add_pheromone[candidate[ii][city_count-1]][candidate[ii][0]] += Q/length[ii]

    '''信息素更新'''
    for i in range(len(citys)):
        for j in range(len(citys)):
            #更新公式
            pheromone[i][j] = (1 - rho) * pheromone[i][j] + add_pheromone[i][j]
    #迭代次数+1
    dis_path.append(min(length))
    cnt = cnt+1


print("蚁群算法的最优路径",path_best[cnt-1])
print("迭代", cnt,"次后","蚁群算法求得最优解",min(dist_best))

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
print(time_sum)

# 打开文件用于写入
file = open('out.txt','a')

# 将结果写入文件
file.write("蚁群算法的最优路径 %s \n" % path_best[cnt-1])
file.write("迭代 %d 次后,蚁群算法求得最优解 %f \n" % (cnt, dist_best[cnt-1]))
file.write("执行时间: %f 秒" % time_sum)

# 关闭文件
file.close()

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