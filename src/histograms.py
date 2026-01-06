import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, RobustScaler
import seaborn as sns

df1 = pd.read_csv('../comparisons/ds_eval_divergence.csv', header = None)
df1[2] = [x.split(':')[-1].strip() for x in df1[2]]
df1.columns = ['DeepSeek\ndisagreement', 'DeepSeek\ndivergence', 'question']
df1.set_index('question', inplace = True)

d = json.load(open('../data.json'))

df = pd.DataFrame.from_records(d['questions'])
df.set_index('question', inplace = True)
df['distance'] = 1 - df['similarity']
df.drop(columns = ['similarity'], inplace = True)

df2 = df['distance divergence disagreement'.split(' ')]

m = df1.merge(df2, left_index = True, right_index = True, how = 'outer')
m.replace([-1, -2], pd.NA, inplace = True)

m2 = m.replace(pd.NA, 0)

fig, axes = plt.subplots(1, 3, figsize=(17, 5))

# ChatGPT divergence histogram
sns.histplot(m2['divergence'], discrete=True, edgecolor='white', shrink=.9, ax=axes[0], alpha=1)
axes[0].set_title('ChatGPT')
axes[0].set_xlabel("Divergence")
axes[0].set_yticks([0,2,4,6,8,10,12,14,16])
axes[0].set_xticks([0,1,2,3,4,5])
axes[0].set_xticklabels(['NA',1,2,3,4,5])
axes[0].set_xlim(-0.8,5.8)
axes[0].grid(axis='y')
axes[0].set_axisbelow(True)

# DS divergence histogram
sns.histplot(m2['DeepSeek\ndivergence'], discrete=True, edgecolor='white', shrink=.9, ax=axes[1], alpha=1)
axes[1].set_title('DeepSeek')
axes[1].set_xlabel("Divergence")
axes[1].set_yticks([0,2,4,6,8,10,12,14,16])
axes[1].set_xticks([0,1,2,3,4,5])
axes[1].set_xticklabels(['NA',1,2,3,4,5])
axes[1].grid(axis='y')
axes[1].set_axisbelow(True)
# Destacando as ocorrências de NA
patch = axes[1].patches[0]
target_bin = patch.get_x()
width = patch.get_width()
height = patch.get_height()
axes[1].bar(target_bin + width/2, height, width=width, color='none', edgecolor='black', hatch='//')

# Bivariate histogram
sns.histplot(m2, x="divergence", y="DeepSeek\ndivergence", discrete=True, edgecolor='white', shrink=.9, ax=axes[2], cbar=True)
axes[2].set_title('Bivariate Histogram')
axes[2].set_xlabel("ChatGPT")
axes[2].set_ylabel("DeepSeek")
axes[2].set_xticks([0,1,2,3,4,5])
axes[2].set_xticklabels(['NA',1,2,3,4,5])
axes[2].set_yticklabels(['NA',1,2,3,4,5])
axes[2].set_xlim(-0.8,5.8)
axes[2].set_yticks([0,1,2,3,4,5])
# Destacando as ocorrências de NA no Bivariate Histogram
quadmesh = axes[2].collections[0]
quad_paths = quadmesh.get_paths()
highlight_positions = [(2, 0), (4, 0), (5, 0)]
for path in quad_paths:
    vertices = path.vertices
    x_left = vertices[0][0]
    y_bottom = vertices[0][1]
    x_right = vertices[2][0]
    y_top = vertices[2][1]
    width = (x_right - x_left) * 0.9
    height = (y_top - y_bottom) * 0.9

    # Ajustando a posição central do quadrado com base no shrink
    x_center = x_left + (x_right - x_left) / 2
    y_center = y_bottom + (y_top - y_bottom) / 2
    x_left_adjusted = x_center - width / 2
    y_bottom_adjusted = y_center - height / 2

    for x_target, y_target in highlight_positions:
        if x_left <= x_target < x_right and y_bottom <= y_target < y_top:
            axes[2].bar(x_left_adjusted + width/2, height, width=width, bottom=y_bottom_adjusted, 
                        color='none', edgecolor='black', hatch='//')

fig.tight_layout()
# plt.savefig("../plots/hist_divergence_refuses.pdf", bbox_inches='tight', dpi=300)
plt.show()
