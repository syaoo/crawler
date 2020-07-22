import pandas as pd
import matplotlib.pyplot as plt
import os,math

def norm_data(data):
    """
    # 归一化数据集
    data : pandas.DataFrame
    """
    return (data-data.mean())/(data.max()-data.min())

def bgd(var_dat,res_dat,alpha,theta=None):
    """
    # batch_gradient _descent 批量梯度下降
    var_dat: 变量数据集
    res_dat: 因变量数据集
    alpha: learning rate 学习率参数
    theta: 变量系数的初始值, 默认为1
    返回：
        theta：list，新参数列表
        cost：新参数的损失函数值
    """
    if theta == None:
        theta = [i/i for i in range(1,var_dat.shape[1]+1)]
    diff=var_dat.dot(theta)-res_dat
    i=0
#     求各项的参数
    for key in var_dat.columns:
#         print(key)
        theta[i] = theta[i]-alpha*sum(var_dat[key]*diff)/len(diff)
        i+=1
    cost = sum(diff**2)/len(diff)/2 # 损失函数值
    return (theta,cost)  # 返回新的参数列表及此时的损失函数值
# new_theta,cost = bgd(feature_value,score,alpha)

fpath = r'./spdider/szfdc/data/202003061747.txt'
dat=pd.read_csv(fpath,delimiter='\t',skiprows=1)
print(dat.columns)
dat.set_index('rownum_',inplace=True)
# dat.columns=[i.lstrip() for i in dat.columns]
dat.sort_values(by='rent_price',ascending=False) # 按租金排序，不是必须
print(dat.head())
print(dat.describe())
# 分离变量与因变量，并归一化
x_label = 'houses_floor_space'
y_label = 'rent_price'
var_data = dat[x_label].copy()
price = dat[y_label].copy()

norm_var = norm_data(var_data)
# print(norm_var.head())
# norm_score = norm_data(score) 
norm_score = score # 不对分数进行归一化
# print(norm_score.head())

print("*"*30)
alpha = [0.0001,0.0003,0.001,0.003,0.01,0.03,0.1,0.3,1] # 学习率
alpha = [10,12,14,16,18,20] # 学习率 30~90之间
# alpha = [0.03,0.05,0.07,0.09,0.11]
alpha = [18]
alpha_save = './alpha'
if not os.path.exists(alpha_save):
    os.mkdir(alpha_save)
for i in alpha:
    theta = [i/i for i in range(1,norm_var.shape[1]+1)] #初始参均为1
    cost_list = []
    while True:
        new_theta,cost = bgd(norm_var,norm_score,i,theta)
        if cost < 0:
            print("损失函数小于0啦！")
            break
        else:
            theta = new_theta
            cost_list.append(cost)
            print("alpha = {},第{}次".format(i,len(cost_list)))
            if len(cost_list)>2:
                diff = cost_list[-2]-cost_list[-1]
                print(diff)
                if math.isnan(diff):
                    print(cost_list[-2])
                    print(cost_list[-1])
                    break
                if diff < 1e-7:
                    print("diff = {}".format(diff))
                    fullpath = os.path.join(alpha_save,str(i)+'.png')
                    # print(cost_list)
                    fig=plt.figure(figsize=(16,9),dpi=80)
                    plt.plot(cost_list)
                    tlt="alpha={}, Iteration times:{}\n min cost {}, max cost{}\n{}"
                    plt.title(tlt.format(i,len(cost_list),min(cost_list),max(cost_list),theta))
                    plt.show()
                    plt.savefig(fullpath,format='png')
                    break
# print('theta is:{}'.format(theta))
# fig=plt.figure(figsize=(16,9),dpi=80)
# plt.scatter(range(var_data.shape[0]),var_data.dot(theta)-score)
# plt.title("var_data-score")
# plt.show()
# fullpath = os.path.join(alpha_save,'err.png')
# plt.savefig(fullpath,format='png')
# fig=plt.figure(figsize=(16,9),dpi=80)
# plt.scatter(range(var_data.shape[0]),var_data.dot(theta))
# plt.scatter(range(var_data.shape[0]),score)
# plt.title("var_data&score")
# plt.show()
# fullpath = os.path.join(alpha_save,'scatter.png')
# plt.savefig(fullpath,format='png')

fig=plt.figure(figsize=(16,9),dpi=80)
plt.scatter(range(norm_var.shape[0]),norm_var.dot(theta)-norm_score)
plt.title("NORM:var_data-score")
plt.show()
fullpath = os.path.join(alpha_save,'NORM_err.png')
plt.savefig(fullpath,format='png')
fig=plt.figure(figsize=(16,9),dpi=80)
plt.scatter(range(norm_var.shape[0]),norm_var.dot(theta))
plt.scatter(range(norm_var.shape[0]),norm_score)
plt.title("NORM:var_data&score")
plt.show()
fullpath = os.path.join(alpha_save,'NORM_scatter.png')
plt.savefig(fullpath,format='png')
