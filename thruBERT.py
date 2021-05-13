from transformers import DistilBertTokenizer, TFDistilBertModel
import tensorflow as tf
import os
import json
import numpy as np
import tqdm

model_file = "./model/distilBERT"
tokenizer_file = "./model/distilTokenizer"
idx2vertidx_file = "./idx2verticalidx.json"

tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_file)
model = TFDistilBertModel.from_pretrained(model_file)

json_folder = "./preprocessed_jsondata/"
json_files = os.listdir(json_folder)
json_files = [json_folder+x for x in json_files]

with open(idx2vertidx_file, 'r') as f:
	idx2verticalidx = json.load(f)

data = []
# [0,768) title
# [768-1536) desc
# [1536-2304) keywords
# 2304 length
# 2305 viewcount
# 2306 likecount
# 2307 dislikecount
# [2308, 2309) multihot class vertical index

for i, file in enumerate(json_files):
	print("converting {}/{} file:{}".format(i, len(json_files), file))
	with open(file, 'rb') as f:
		json_dict = json.load(f)
	
	for videoId in tqdm.tqdm(json_dict):
		vector = []

		if json_dict[videoId]["keywords"] == '':
			continue
		
		ip = tokenizer(json_dict[videoId]["keywords"], return_tensors='tf', truncation=True)
		op = model(ip)
		x = op.last_hidden_state
		x = tf.squeeze(x)
		x = x[0]
		vector.append(x)

		for k in ["length", "viewCount", "likeCount", "dislikeCount"]:
			vector.append(np.array([json_dict[videoId][k]]))
		
		# multi_hot = np.zeros(25)

		idx = json_dict[videoId]["labels"][0]
			# multi_hot[idx2verticalidx[str(idx)]] = 1.0
		
		vector.append(idx2verticalidx[str(idx)])
		
		vector = np.hstack(vector)
		# print(vector.shape)
		data.append(vector)

data = np.vstack(data)

print("Saving data as npy file")
with open("data2.npy", 'wb') as f:
	np.save(f, data)

			

