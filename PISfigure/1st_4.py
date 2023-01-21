#w=631
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei Arial（英文）
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# x = np.array([1, 2, 3, 4, 5])
# m256 = np.array([0.1025,0.132,0.3898,0.7801,1.5504])
# m512 = np.array([0.2067,0.3011,0.4666,0.8589,1.7080])
# m1024 = np.array([0.3057,0.4108,0.5999,0.9022,1.8160])
# m2048 = np.array([0.4127,0.5294,0.6945,1.1105,1.9931])
# m4096= np.array([0.5236,0.6304,0.8305,1.2995,2.1092])


# x = np.array([1, 2, 3, 4])
# m256 = np.array([0.132,0.3898,0.7801,1.4504])
# m512 = np.array([0.2011,0.4666,0.8589,1.7080])
# m1024 = np.array([0.4108,0.5999,0.9022,1.8160])
# m2048 = np.array([0.5294,0.6945,1.105,1.9931])
# m4096= np.array([0.7304,0.8305,1.2995,2.3092])

x = np.array([1, 2, 3, 4])
m256 = np.array([0.232, 0.3580, 0.4641, 0.5611])
m512 = np.array([0.4447,0.647,0.8653,1.1028])
m1024 = np.array([0.9455, 1.2542,1.87112,2.0307])
m2048 = np.array([1.8046,2.7028,3.4604,4.2624])
m4096= np.array([3.4672,4.9731,6.8973,8.4524])

# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(7, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 去掉上边框
ax.spines['right'].set_visible(False)  # 去掉右边框

plt.plot(x, m256, marker='s', color="blue", label="m$=2^8$", linewidth=1.5)
plt.plot(x, m512, marker='o', color="green", label="m$=2^9$", linewidth=1.5)
plt.plot(x, m1024, marker='p', color="black", label="m$=2^{10}$", linewidth=1.5)
plt.plot(x, m2048, marker='v', color="red", label="m$=2^{11}$", linewidth=1.5)
plt.plot(x, m4096, marker='d', color="purple", label="m$=2^{12}$", linewidth=1.5)


group_labels = [ '2', '3', '4', '5']  # x轴刻度的标识
#group_labels1 = ['10', '20', '30', '40', '50']
plt.xticks(x, group_labels, fontsize=12, fontweight='light')  # 默认字体大小为10
plt.yticks(fontsize=12, fontweight='light')
#plt.yticks(np.arange(0,40,10) ,fontsize=12, fontweight='light')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("The number of DOs", fontsize=13, fontweight='light')
plt.ylabel("computation costs(s)", fontsize=13, fontweight='light')
plt.xlim(0.9, 4.1)  # 设置x轴的范围
plt.ylim(0, 9)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='light')  # 设置图例字体的大小和粗细

plt.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.1, hspace = 0, wspace = 0)
plt.margins(0,0)

plt.savefig('E:/A-paper/PIS/figure/exp/DOs.pdf', format='pdf')
plt.show()