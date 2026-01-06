from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import json
import pandas as pd
import seaborn as sns

# Load data
d = json.load(open('../data.json'))
df = pd.DataFrame.from_records(d['questions'])
# ['label', 'question', 'focus', 'chatgpt', 'deepseek', 'similarity', 'divergence', 'disagreement']

# sns.histplot(data=df, x="similarity", bins=100)

df['chatgpt'] = df['chatgpt'].apply(lambda x: x.replace(". ", "; ").replace(".\n", ";\n").replace(".",""))
df['deepseek'] = df['deepseek'].apply(lambda x: x.replace(". ", "; ").replace(".\n", ";\n").replace(".",""))

# Get low similarity answers
# low = df[df['similarity'] < 0.9]

stopwords = set(STOPWORDS)
stopwords.add('eg')
stopwords.add('s')

wc = WordCloud(max_words=100, stopwords=stopwords,
               font_path='/Library/Fonts/Arial Unicode.ttf',
               margin=10, random_state=1,
               relative_scaling=0.4,
               colormap='winter',
               min_font_size=8,
               max_font_size=70,
               background_color='white').generate('\n\n'.join(df['chatgpt'].to_list()))
plt.figure(figsize=(20,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title("ChatGPT")
plt.tight_layout()
plt.show()
wc.to_file("../plots/wordcloud_chatgpt.png")
with open("../plots/wordcloud_chatgpt.svg", "w") as text_file:
    text_file.write(wc.to_svg())

wc = WordCloud(max_words=100, stopwords=stopwords,
               font_path='/Library/Fonts/Arial Unicode.ttf',
               margin=10, random_state=1,
               relative_scaling=0.4,
               colormap='winter',
               min_font_size=8,
               max_font_size=70,
               background_color='white').generate('\n\n'.join(df['deepseek'].to_list()))
plt.figure(figsize=(20,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title("DeepSeek")
plt.tight_layout()
plt.show()
wc.to_file("../plots/wordcloud_deepseek.png")
with open("../plots/wordcloud_deepseek.svg", "w") as text_file:
    text_file.write(wc.to_svg())