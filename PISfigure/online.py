import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1,2,3,4])

# offline_m512 = np.array([1.3642,1.711,2.2922,2.9369,4.3522])
# online_m512 = np.array([1.3548,1.5011,1.9066,2.6989,3.208])
# offline_m2048 = np.array([10.337,12.9304,16.2405,19.7185,23.1709])
# #online_m512 = np.array([0.3857,0.7675,1.2332,1.5394,2.0684])
# online_m2048 = np.array([7.4219,7.6304,8.305,9.116,10.809])

offline_m512 = np.array([1.711,2.2922,2.9369,4.3522])
online_m512 = np.array([1.5011,1.9066,2.6989,3.208])
offline_m2048 = np.array([12.9304,16.2405,19.7185,23.1709])
#online_m512 = np.array([0.3857,0.7675,1.2332,1.5394,2.0684])
online_m2048 = np.array([7.6304,8.305,9.116,10.809])

# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(7, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线

ax = plt.gca()
ax.spines['top'].set_visible(False)  # 去掉上边框
ax.spines['right'].set_visible(False)  # 去掉右边框
group_labels = ['2', '3', '4','5']  # x轴刻度的标识
#plt.plot(x, w350, marker='s', olor="bluec", label="Request Submission", linewidth=1.5)
#plt.plot(x, w631, marker='o', color="red", label="Data Submission", linewidth=1.5)
#plt.subplot(131)
#plt.bar(x, w350 ,width = 0.2, facecolor='lightsteelblue',  label="w=350", edgecolor = 'black', hatch=".")

#plt.bar(x, online_m512 ,width=0.2, label="online_512",hatch="///",edgecolor='black' )
#width:柱的宽度
#plt.bar(x+0.2,offline_m512, width=0.2, label="offline_512", hatch="--",edgecolor='black')
#plt.bar(x+0.4,online_m2048,width=0.2, color='gainsboro', label="online_2048", hatch="\\\\\\",edgecolor='black')
#plt.bar(x+0.6,offline_m2048,width=0.2, color='orange', label="offline_2048", hatch="|||", edgecolor='black')
width=0.2

plt.bar(x - 1.5 * width, online_m512 ,width=0.2, color='orange',label="online_512",hatch="///",edgecolor='black' )
#width:柱的宽度
plt.bar(x - 0.5 * width,offline_m512, width=0.2, label="offline_512", hatch="--",edgecolor='black')
plt.bar(x + 0.5 * width,online_m2048,width=0.2,   label="online_2048", hatch="\\\\\\",edgecolor='black')
plt.bar(x + 1.5 * width,offline_m2048,width=0.2,  color='gainsboro', label="offline_2048", hatch="|||", edgecolor='black')

#group_labels1 = ['10', '20', '30', '40', '50']
plt.xticks(x, group_labels, fontsize=12, fontweight='light')  # 默认字体大小为10
plt.yticks(fontsize=12, fontweight='light')
#plt.yticks(np.arange(0,40,10) ,fontsize=12, fontweight='light')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("The number of DOs", fontsize=13, fontweight='light')
plt.ylabel("Computation costs(s)", fontsize=13, fontweight='light')
#ax.set_xticks(x +0.2*1.5)
#plt.xlim(0.9, 8.1)  # 设置x轴的范围
plt.ylim(0,25)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='light')  # 设置图例字体的大小和粗细

plt.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.97, left = 0.10, hspace = 0, wspace = 0)
plt.margins(0,0)

plt.savefig('E:/A-paper/PIS/figure/exp/online.pdf', format='pdf')
plt.show()