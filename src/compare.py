
from sentence_transformers import SentenceTransformer
from glob import glob
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


##################################################
TOTAL_ANS = 50
CHATGPT_BASE_PATH = "../answers/chatgpt"
DEEPSEEK_BASE_PATH = "../answers/deepseek"
##################################################

# Load the model
sentence_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") 
# sentence_model = SentenceTransformer("sentence-transformers/paraphrase-albert-small-v2")

# Load all answers
chatgpt_ans = dict()
deepseek_ans = dict()

for i in range(1, TOTAL_ANS + 1):
    chatgpt_ans[i] = open(f"{CHATGPT_BASE_PATH}/ans_{i}.md", "r").read()
    deepseek_ans[i] = open(f"{DEEPSEEK_BASE_PATH}/ans_{i}.md", "r").read()


# Compare the answers
heat_map = np.zeros(TOTAL_ANS)
for i in range(1, TOTAL_ANS + 1):
    chatgpt_emb = sentence_model.encode(chatgpt_ans[i], convert_to_tensor=True)
    deepseek_emb = sentence_model.encode(deepseek_ans[i], convert_to_tensor=True)

    cos_sim = sentence_model.similarity(chatgpt_emb, deepseek_emb)
    print(f"Answer {i}: {cos_sim.item()}")
    heat_map[i-1] = cos_sim.item()


heat_map = heat_map.reshape(5, 10)

# Save the heat map
# np.savetxt("heat_map.csv", heat_map, delimiter=",")


# plot the heat map using seaborn
sns.heatmap(heat_map, cmap="YlGnBu", annot=True)
plt.show()












