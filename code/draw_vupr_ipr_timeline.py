import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # <=== 需要引入这个来完美定制图例
import seaborn as sns
import numpy as np
import pandas as pd
import json

cloudflare_nonrov_asns = {'6762', '12389', '20485', '7473', '16735', '52320', '10429', '262589', '37468', '4809', '7738', '4766', '18881', '4230', '5483', '267613', '7029', '26615', '28598', '7474', '13786', '9318', '7545', '22356', '577', '6128', '17676', '4788', '14840', '38195', '9121', '6327', '9009', '8447', '11404', '53013', '7303', '12874', '23106', '25933', '3269', '2764', '53087', '812', '2856', '12430', '6730', '12578', '8881', '9299', '5650', '45899', '263009', '28260', '3209', '31027', '4775', '9269', '11664', '14868', '9790', '1853', '28368', '15557', '52871', '12083', '25255', '53181', '43350', '40676', '19108', '29049', '7992', '35805', '9829', '55836', '25229', '9924', '6697', '24940', '21013', '5769', '264144', '199524', '50304', '6848', '23655', '8422', '30722', '4922', '5432', '28580', '15704', '12735', '4739', '6677', '36351', '3737', '49505', '46562', '55410', '23930', '37153', '29691', '12849', '45595', '42926', '803', '9824', '42772', '262287', '50340', '41998', '14537', '8280', '45011', '60294', '12353', '5645', '23944', '9541', '46375', '9891', '6147', '25106', '55720', '23969', '46844', '3243', '13213', '11338', '27796', '27715', '197155', '24904', '12322', '5410', '51765', '137409', '4670', '20845', '35228', '21334', '34569', '43317', '58477', '16276', '29854', '8412', '24768', '4804', '47536', '43289', '58065', '3238', '32489', '54133', '21928', '5378', '21502', '397373', '42863', '133480', '45669', '200899', '32329', '34803', '51430', '12390', '198570', '138384', '38266', '11878', '197328', '10507', '13170', '15435', '51852', '11831', '33083', '14593', '25560', '15456', '56309', '263945', '196819', '57814', '28573', '16135', '51207', '31615', '24158', '395954', '37705', '55286', '19165', '50266', '132199', '206067', '36850', '7203', '10139', '396190', '30633', '34296', '17552', '17858', '9644', '9605', '15457', '4685', '17853', '212238', '396362', '19148', '29485', '54858', '394380', '135478', '47800', '45382', '15491', '36445', '42580', '34702', '50613', '393886', '197706', '61272', '30900', '17090', '134094', '52270', '15003', '201924', '42082', '36077', '394752', '200698', '200651', '396986', '42994', '265708', '205053', '57127', '264649', '200709', '208673', '43945', '139879', '133481', '39651'}
cloudflare_rov_asns = {'3356', '1299', '174', '2914', '6939', '3257', '6453', '6461', '3491', '1273', '9002', '5511', '4637', '12956', '7922', '7018', '701', '6830', '3320', '286', '4826', '33891', '3303', '22773', '28329', '1221', '5405', '5617', '1239', '8708', '20965', '52873', '1764', '852', '10796', '263444', '13030', '9443', '30781', '3462', '28186', '29535', '35280', '5089', '3292', '28263', '2119', '47147', '17451', '52863', '6079', '45177', '15576', '8767', '11351', '15895', '207841', '16086', '28126', '25369', '719', '1136', '12271', '44530', '14282', '18106', '8100', '6866', '55850', '52999', '3399', '2860', '8560', '29695', '29518', '33915', '262659', '12337', '42831', '50058', '35432', '8426', '55805', '56655', '12611', '553', '5539', '25291', '2852', '2611', '51088', '13335', '9136', '2027', '33182', '3265', '51559', '8283', '13101', '150369', '4764', '7642', '21738', '8075', '58820', '7195', '24309', '35612', '16509', '264130', '1213', '52210', '61785', '18209', '41164', '51519', '2906', '212271', '37611', '1403', '204274', '29413', '31472', '397143', '60876', '49409', '27400', '394256', '39839', '14907', '199811', '14525', '44034', '12876', '47524', '197540', '35008', '6167', '21040', '31423', '30736', '46805', '33986', '41000', '205668', '197301', '204151', '20259', '39384', '263812', '54681', '393891', '60422', '265656', '399866', '201199', '215467', '51999', '56958', '211562', '213268', '19468', '17147', '207149', '397388', '142582', '202427', '200242'}

# 假设 df 是你的数据：columns = ['VPR', 'IPR', 'Status']
# Status 的取值: 'ROV', 'Non-ROV', 'Unknown'
data = []
y_0, y_1, x_less, y_less = 0, 0, 0, 0
x_less_v2, y_less_v2 = 0, 0
with open(f'/mountdisk3/prs_20250801.json', 'r') as rf:
    rf_data = json.load(rf)
    for asn, val in rf_data.items():
        if len(val) > 1:
            if asn in cloudflare_rov_asns: status = 'ROV'
            elif asn in cloudflare_nonrov_asns: status = 'Non-ROV'
            else: status = 'Unknown'
            vpr = val['valid'][0] / val['valid'][1]
            ipr = val['invalid'][0] / val['invalid'][1]
            # if ipr > 0.9 and val['invalid'][1] >= 5:
            #     print(f'{asn}: {val}, {status}')
            # if ipr == 1 and vpr < 1 and val['invalid'][1] >= 5:
            #     y_1 += 1
            # elif ipr == 0 and vpr < 1 and val['invalid'][1] >= 5: y_0 += 1
            # if ipr < vpr and val['invalid'][1] >= 5: y_less += 1
            # elif vpr < ipr and val['invalid'][1] >= 5: x_less += 1
            # if ipr < vpr: y_less_v2 += 1
            # elif ipr > vpr: x_less_v2 += 1
            data.append([vpr, ipr, status, (val['valid'][1] >= 10) & (val['invalid'][1] >= 10)])
            
# print(f'y_1: {y_1}, y_0: {y_0}, y_less: {y_less}, x_less: {x_less}')
# print(f'x_less_v2: {x_less_v2}, y_less_v2: {y_less_v2}')
    
df = pd.DataFrame(data, columns=['VPR', 'IPR', 'Status', 'Invalid_Denominator'])

total_points = len(df)
sufficient_points = df[df['Invalid_Denominator']]
marginal_points = df[~df['Invalid_Denominator']]
upper_left_points = df[(df['VPR'] < 0.5) & (df['IPR'] > 0.5)]
above_diagonal_points = df[df['IPR'] > df['VPR']]
print(f'total plotted points: {total_points}')
print(
    'sufficient observations '
    '(VUPR denominator >= 10 and IPR denominator >= 10): '
    f'{len(sufficient_points)} / {total_points}'
)
print(
    'marginal observations '
    '(VUPR denominator < 10 or IPR denominator < 10): '
    f'{len(marginal_points)} / {total_points}'
)
print(
    'upper-left points (VUPR < 0.5 and IPR > 0.5): '
    f'{len(upper_left_points)} / {total_points} '
    f'[{upper_left_points["Invalid_Denominator"].sum()} sufficient, '
    f'{(~upper_left_points["Invalid_Denominator"]).sum()} marginal]'
)
print(
    'points above diagonal (IPR > VUPR): '
    f'{len(above_diagonal_points)} / {total_points} '
    f'[{above_diagonal_points["Invalid_Denominator"].sum()} sufficient, '
    f'{(~above_diagonal_points["Invalid_Denominator"]).sum()} marginal]'
)

import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman'] + mpl.rcParams['font.serif']

# =====================================================================
# 视觉设置与调色板
# =====================================================================
#palette = {'ROV': '#2ca02c', 'Non-ROV': '#d62728', 'Unknown': '#b0b0b0'}
palette = {'ROV': '#2ca02c', 'Non-ROV': '#2ca02c', 'Unknown': '#2ca02c'}

# 这一次，我们终于可以随心所欲地混用标记了！
# Unknown 使用最干净的细十字 '+', (如果你喜欢叉号也可以换成 'x')
#markers = {'ROV': 'o', 'Non-ROV': 'D', 'Unknown': '+'} 
markers = {'ROV': 'o', 'Non-ROV': 'o', 'Unknown': 'o'} 

# 显式大小映射：True(分母大)对应大号 250，False(分母小)对应小号 20
size_mapping = {True: 100, False: 10}

# 1. 建立画板 (边缘的核密度图依然让 Seaborn 帮我们自动画)
g = sns.JointGrid(data=df, x="VPR", y="IPR", hue="Status", 
                  palette=palette, height=7, ratio=4, space=0.1)

# =====================================================================
# 2. 绘制散点图 (绕过 Seaborn，直接使用底层 Matplotlib)
# =====================================================================
# 我们刻意控制画图顺序：先画 Unknown，再画 Non-ROV，最后画 ROV
# 这样灰色的十字永远在最下层，绝对不会挡住关键的红绿数据点！
for status in['Unknown', 'Non-ROV', 'ROV']:
    subset = df[df['Status'] == status]
    if subset.empty: continue
        
    sizes = subset['Invalid_Denominator'].map(size_mapping)
    
    # 针对纯线条图形（如十字 '+'），只需要设置 color
    if markers[status] == '+':
        g.ax_joint.scatter(
            subset['VPR'], subset['IPR'],
            s=sizes,
            color=palette[status],  # 染色
            marker=markers[status],
            linewidths=1.2,
            alpha=0.6               # 十字不需要太抢眼，透明度调低一点
        )
    # 针对原本是实心的图形（o 和 D），原生支持直接画成空心
    else:
        g.ax_joint.scatter(
            subset['VPR'], subset['IPR'],
            s=sizes,
            facecolors='none',          # <=== 直接指定内部透明（掏空）
            edgecolors=palette[status], # <=== 边缘上色
            marker=markers[status],
            linewidths=1.5,
            alpha=0.8
        )

# =====================================================================
# 3. 绘制边缘分布及参考线
# =====================================================================
g.plot_marginals(sns.kdeplot, fill=True, common_norm=False, alpha=0.4, linewidth=2)

g.ax_joint.plot([0, 1.05],[0, 1.05], 'k--', linewidth=0.5, zorder=0)
g.ax_joint.axhline(y=0, color='black', linestyle=':', linewidth=2, zorder=0)

g.ax_joint.set_xlim(-0.05, 1.05)
g.ax_joint.set_ylim(-0.05, 1.05)
g.ax_joint.tick_params(axis='both', which='major', labelsize=18)
g.ax_joint.set_xlabel('Valid and Unknown Propagation Ratio (VUPR)', fontsize=20)
g.ax_joint.set_ylabel('Invalid Propagation Ratio (IPR)', fontsize=20)

# =====================================================================
# 4. 手工打造最干净的图例 (摆脱 Seaborn 的乱码图例)
# =====================================================================
# 状态图例
status_handles = [
    Line2D([0], [0], marker='o', color='w', markeredgecolor=palette['ROV'], markerfacecolor='none', markersize=9, markeredgewidth=1.5, label='ROV'),
    Line2D([0], [0], marker='D', color='w', markeredgecolor=palette['Non-ROV'], markerfacecolor='none', markersize=8, markeredgewidth=1.5, label='Non-ROV'),
    Line2D([0], [0], marker='+', color='w', markeredgecolor=palette['Unknown'], markersize=10, markeredgewidth=1.5, label='Unknown')
]
# legend1 = g.ax_joint.legend(handles=status_handles, 
#                             loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
# g.ax_joint.add_artist(legend1)

# # 大小图例
size_handles = [
    Line2D([0], [0], marker='o', color='w', markeredgecolor='gray', markerfacecolor='none', markersize=5, markeredgewidth=1.5, label='marginal observations'),
    Line2D([0], [0], marker='o', color='w', markeredgecolor='gray', markerfacecolor='none', markersize=13, markeredgewidth=1.5, label='sufficient observations')
]
# legend2 = g.ax_joint.legend(handles=size_handles, 
#                             loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)

from matplotlib.patches import Patch
empty_handle = Patch(color='none', label="") 
# all_handles = [
#     status_handles[0], size_handles[1], # 第一列 (索引0, 1)
#     status_handles[1], size_handles[0], # 第二列 (索引2, 3)
#     status_handles[2], empty_handle     # 第三列 (索引4, 5)
# ]
# legend = g.ax_joint.legend(
#     handles=all_handles,
#     loc='upper left',           # 改为左对齐锚点
#     bbox_to_anchor=(0, -0.125), # 调整水平偏移量（0.1为从左侧10%处开始）
#     ncol=3,                     # 每行显示3个
#     frameon=False,
#     columnspacing=1.0,          # 调节列间距
#     labelspacing=1.00,
#     handletextpad=0.5,           # 调节图标与文字间距
#     prop={'family': 'serif', 'size': 18}
# )


# legend = g.ax_joint.legend(
#     handles=all_handles,
#     loc='lower left',             # 锚点设为图例的左下角
#     bbox_to_anchor=(0.0, 1.3),   # (x, y) 坐标：0.0 与左轴对齐，1.15 位于图表上方
#     ncol=3,                       # 保持 3 列，会自动折行为两行
#     frameon=False,
#     columnspacing=1.5,            # 稍微拉开列间距避免拥挤
#     handletextpad=0.5,
#     prop={'family': 'serif', 'size': 14}  # <=== 在这里统一放大字体
# )
# 1. 状态图例 (独立的第一行)
leg_status = g.ax_joint.legend(
    handles=[status_handles[0], status_handles[1], status_handles[2]], 
    loc='upper left',            # <=== 改为基于左上角锚定
    bbox_to_anchor=(-0.1, -0.12), # <=== X轴设为 0.0，对齐画板左边缘
    ncol=3, frameon=False, fontsize=18, columnspacing=2.0
)
g.ax_joint.add_artist(leg_status)

# 2. 观察量图例 (独立的第二行)
leg_size = g.ax_joint.legend(
    handles=[size_handles[1], size_handles[0]], 
    loc='upper left',            # <=== 改为基于左上角锚定
    bbox_to_anchor=(-0.1, -0.22), # <=== X轴保持完全一致的 0.0
    ncol=2, frameon=False, fontsize=18, columnspacing=3.0
)
g.ax_joint.add_artist(leg_size)

# 3. 必须给底部留出足够的边距，防止被切掉
g.fig.subplots_adjust(bottom=0.25)

# 4. 保存时将两个独立的图例都加入 bbox_extra_artists
plt.savefig('tmp.png', dpi=300, bbox_inches='tight', bbox_extra_artists=(leg_status, leg_size))
plt.savefig('vpr_ipr.pdf', dpi=300, bbox_inches='tight', bbox_extra_artists=(leg_status, leg_size))
plt.show()
