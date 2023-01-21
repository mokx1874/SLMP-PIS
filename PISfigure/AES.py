# m=1024 w=631
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1, 2, 3, 4, 5, 6,7,8])
aes128 = np.array([11.1414,11.05548,11.129475,11.1253,11.1016,11.1148,11.1138,11.1172])
aes256 = np.array([11.4202,11.2796,11.4243,11.2328,11.3201,11.3374,11.3358,11.3371])
aes192= np.array([11.3113,11.2781,11.1955,11.2315,11.2554,11.265,11.2126,11.2125])


# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(7, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 去掉上边框
ax.spines['right'].set_visible(False)  # 去掉右边框


plt.plot(x, aes128, marker='s', color="blue", label="AES-128", linewidth=1.5)
plt.plot(x, aes192, marker='o', color="green", label="AES-192", linewidth=1.5)
plt.plot(x, aes256, marker='v', color="red", label="AES-256", linewidth=1.5)

group_labels = ['25', '50', '75', '100', '125', '150','175','200']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=12, fontweight='light')  # 默认字体大小为10
plt.yticks(fontsize=12, fontweight='light')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Time of experiments", fontsize=13, fontweight='light')
plt.ylabel("Computation costs(s)", fontsize=13, fontweight='light')
plt.xlim(0.9, 8.1)  # 设置x轴的范围
plt.ylim(10, 12)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='light')  # 设置图例字体的大小和粗细

plt.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.11, hspace = 0, wspace = 0)
plt.margins(0,0)

plt.savefig('E:/A-paper/PIS/figure/exp/AES.pdf', format='pdf')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
plt.show()