import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram

df1 = pd.read_csv('../comparisons/ds_eval_divergence.csv', header = None)
df1[2] = [x.split(':')[-1].strip() for x in df1[2]]
df1.columns = ['DeepSeek\ndisagreement', 'DeepSeek\ndivergence', 'question']
df1.set_index('question', inplace = True)
q1 = set(df1.index)

# If DeepSeek does now answer (starts with "Sorry, I'm"), then returns False
def check_ds_answer(r):
    return not r.startswith("Sorry, I'm")

d = json.load(open('../data.json'))

d['questions']
df = pd.DataFrame.from_records(d['questions'])
df.set_index('question', inplace = True)
df['distance'] = 1 - df['similarity']
df.drop(columns = ['similarity'], inplace = True)
df['DS Answers'] = [check_ds_answer(x) for x in df.deepseek]

df2 = df['distance,divergence,disagreement,DS Answers'.split(',')]

q2 = set(df2.index)

m = df1.merge(df2, left_index = True, right_index = True, how = 'outer')
m.replace([-1, -2], pd.NA, inplace = True)

# distance
# DS\ndisagreement
# GPT\ndisagreement
# Não mexemos em divergência pois é apenas baseada na pergunta
m.loc[m['DS Answers'] == False, 'distance'] = np.nan
m.loc[m['DS Answers'] == False, 'DeepSeek\ndisagreement'] = np.nan
m.loc[m['DS Answers'] == False, 'disagreement'] = np.nan

m.drop(columns = ['DS Answers'], inplace = True)

# m2 = m.replace(pd.NA, 0)

index_na = m.isna()
# x = StandardScaler().fit_transform(m.fillna(0))
x = MinMaxScaler().fit_transform(m.fillna(0))
m_scaled = pd.DataFrame(x, columns = m.columns, index = m.index)
m_scaled[index_na] = pd.NA

m_scaled.rename(columns = {'distance': 'Embedding\ncosine distance', 'divergence': 'ChatGPT\ndivergence', 'disagreement': 'ChatGPT\ndisagreement'}, inplace = True)

order_plot = ['Embedding\ncosine distance', 'DeepSeek\ndisagreement', 'ChatGPT\ndisagreement', 'DeepSeek\ndivergence',
       'ChatGPT\ndivergence', ]

Z = hierarchy.linkage(m_scaled.fillna(0), 'ward', metric = 'euclidean')
dn = hierarchy.dendrogram(Z, no_plot = True)

m_r = m_scaled.iloc[[int(x) for x in dn['ivl']], :]

# agrupamento hierárquico
data = m_r[order_plot].copy()
data_filled = data.apply(lambda x: x.fillna(x.mean()), axis=0)
linkage_y = linkage(data_filled, method='ward')
num_clusters = 4  
cluster_labels = fcluster(linkage_y, num_clusters, criterion='maxclust')

# colormap para os clusters
unique_clusters = np.unique(cluster_labels)
colors = sns.color_palette('tab10', len(unique_clusters))
cluster_colors = {uc: colors[i] for i, uc in enumerate(unique_clusters)}

row_colors = pd.Series(cluster_labels, index=data_filled.index).map(cluster_colors)

# máscara para nan
print(data)
mask = data.isna()

# colormap para o heatmap
# cmap = sns.color_palette("magma", as_cmap=True)
cmap = sns.color_palette("coolwarm", as_cmap=True)
# cmap = sns.color_palette("viridis_r", as_cmap=True)
cmap.set_bad(color='white')  # Define NaNs como branco


cm = sns.clustermap(
    data_filled,
    figsize=(10,16),
    col_cluster=False,  # disable dendrogram
    yticklabels=True,
    method='ward',
    cmap=cmap,
    mask=mask,
    tree_kws=dict(linewidths=1),
    dendrogram_ratio=0.3,
    #cbar_pos=(0, .2, .03, .4),
    #cbar_kws=dict(orientation='vertical', shrink=1, pad=0.1),
    cbar_kws=dict(orientation='vertical'),
    row_colors=row_colors  # adiciona a barra lateral de clusters
)

cm.figure.subplots_adjust(top=1.37,
                          right=0.3
)
# cm.ax_cbar.set_position((0.48, .038, .4, .01)) # Left, Bottom, Width, Height
cm.ax_cbar.set_position((0.94, .4, .02, .3))

# barra de cores
# cbar = cm.ax_heatmap.figure.colorbar(
#     cm.ax_heatmap.collections[0], 
#     ax=cm.ax_heatmap, 
#     orientation="horizontal",
#     fraction=0.05,  # tamanho da barra
#     pad=0.1  # distância entre a barra e o heatmap
# )

# ordena as cores de acordo com o dendrograma
ordered_leaves = cm.dendrogram_row.reordered_ind
ordered_row_colors = row_colors.iloc[ordered_leaves]

cm.data2d.index = ordered_row_colors.index
cm.row_colors = [ordered_row_colors]

# esconde a barra de cor (opcional)
#cm.cax.set_visible(False)
#plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

ax = cm.ax_heatmap
ax.set_xlabel("")
ax.set_ylabel("")

# plt.tight_layout()
plt.savefig('../plots/clustermap.pdf', dpi=300)

plt.show()
