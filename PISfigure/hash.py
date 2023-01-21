# MIN 2^10
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1, 2, 3, 4, 5, 6,7,8])
md5 = np.array([11.79,11.6799,11.7178,11.8315,11.8315,11.7972,11.765,11.783])
sha1 = np.array([11.7609,11.8037,11.775,11.7891,11.8794,11.8303,11.8454,11.8655])
sha256 = np.array([11.7641,11.79438,11.7083,11.7768,11.8504,11.8125,11.8358,11.8571])
sha512 = np.array([11.7638,11.7222,11.7524,11.7369,11.7815,11.8177,11.7885,11.786])


# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(7, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 去掉上边框
ax.spines['right'].set_visible(False)  # 去掉右边框


plt.plot(x, md5, marker='s',  color="blue", label="MD5", linewidth=1.5)
plt.plot(x, sha1, marker='o',  color="green", label="SHA-1", linewidth=1.5)
plt.plot(x, sha256, marker='p', color="black", label="SHA-256", linewidth=1.5)
plt.plot(x, sha512, marker='v',  color="red", label="SHA-512", linewidth=1.5)

group_labels = ['25', '50', '75', '100', '125', '150','175','200']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=12, fontweight='light')  # 默认字体大小为10
plt.yticks(fontsize=12, fontweight='light')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Time of experiments", fontsize=13, fontweight='light')
plt.ylabel("Computation costs(s)", fontsize=13, fontweight='light')
plt.xlim(0.9, 8.1)  # 设置x轴的范围
plt.ylim(11, 12)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='light')  # 设置图例字体的大小和粗细

plt.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.11, hspace = 0, wspace = 0)
plt.margins(0,0)

plt.savefig('E:/A-paper/PIS/figure/exp/hash.pdf', format='pdf')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
plt.show()