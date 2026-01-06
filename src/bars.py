import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import seaborn as sns

df1 = pd.read_csv('../comparisons/ds_eval_divergence.csv', header = None)
df1[2] = [x.split(':')[-1].strip() for x in df1[2]]
df1.columns = ['DS\ndisagreement', 'DS\ndivergence', 'question']
df1.set_index('question', inplace = True)

def check_ds_answer(r):
    return not r.startswith("Sorry, I'm")

d = json.load(open('../data.json'))
df = pd.DataFrame.from_records(d['questions'])
df.set_index('question', inplace = True)
df['distance'] = 1 - df['similarity']
df.drop(columns = ['similarity'], inplace = True)
df['DS Answers'] = [check_ds_answer(x) for x in df.deepseek]
df['question'] = df.index
df['question'] = [str(x) + ' - ' + y for x, y in zip(df.label, df.question)]
df2 = df['question,label,distance,divergence,disagreement,DS Answers'.split(',')]

m = df1.merge(df2, left_index = True, right_index = True)
m.replace([-1, -2], np.nan, inplace = True)
m.set_index('question', inplace = True)

m.loc[m['DS Answers'] == False, 'distance'] = np.nan
m.loc[m['DS Answers'] == False, 'DS\ndisagreement'] = np.nan
m.loc[m['DS Answers'] == False, 'disagreement'] = np.nan
m.drop(columns = ['DS Answers'], inplace = True)
m.head()

m_scaled = m.copy()
m_scaled['distance'] = MinMaxScaler(feature_range = (0, 5)).fit_transform(m[['distance']])
m_scaled = m_scaled.drop(columns = 'label')

m_scaled.rename(columns = {'distance': 'Embedding\ncosine distance', 'divergence': 'ChatGPT\ndivergence', 'disagreement': 'ChatGPT\ndisagreement', 'DS\ndivergence': 'DeepSeek\ndivergence', 'DS\ndisagreement':'DeepSeek\ndisagreement'}, inplace = True)

suffix = 'Embedding\ncosine distance'
tmp = m_scaled[suffix].copy()
fig, axes = plt.subplots(1, 3, figsize = (11, 16))
ax0 = tmp.plot(kind = 'barh', ax = axes[0], color = 'gray');
ax0.set_ylabel('')
ax0.set_axisbelow(True)
ax0.yaxis.grid(color='gray', linestyle='dotted')
ax0.xaxis.grid(color='gray', linestyle='dotted')
plt.setp(ax0.get_yticklabels(), visible=False)
ax0.set_xticks([0,1,2,3,4,5])
ax0.set_xlabel('Embedding\nCosine Distance')

suffix = 'divergence'
tmp = m_scaled[["DeepSeek\n" + suffix, "ChatGPT\n" + suffix]].copy()
ax1 = tmp.plot(kind = 'barh', ax = axes[1]);
ax1.set_ylabel('')
ax1.set_axisbelow(True)
ax1.yaxis.grid(color='gray', linestyle='dotted')
ax1.xaxis.grid(color='gray', linestyle='dotted')
plt.setp(ax1.get_yticklabels(), visible=False)
ax1.set_xticks([0,1,2,3,4,5])
ax1.set_xlabel('Divergence')
ax1.legend(['DeepSeek', 'chatGPT'], ncol=2, loc = 'upper center', bbox_to_anchor=(1.03, 1.025))

suffix = 'disagreement'
tmp = m_scaled[["DeepSeek\n" + suffix, "ChatGPT\n" + suffix]].copy()
ax = tmp.plot(kind = 'barh', ax = axes[2], legend = False);

ax.yaxis.tick_right()
plt.tight_layout()
fig = ax.get_figure()
ax.set_ylabel('')
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dotted')
ax.xaxis.grid(color='gray', linestyle='dotted')
#plt.setp(ax1.get_yticklabels(), visible=False)
ax.set_xticks([0,1,2,3,4,5])
ax.set_xlabel('Disagreement')

plt.subplots_adjust(wspace=0.05, hspace=0)

fig.savefig('../plots/bar_all.png')
plt.show()

