import time

prev_t = time.time()
import sys
import json
import re
import numpy as np
import pycld2 as cld2
import transformers
from transformers import DistilBertTokenizer, TFDistilBertModel
import tensorflow as tf
import json
import numpy as np

tf.get_logger().setLevel('ERROR')
transformers.logging.set_verbosity_error()


from utils import getVideoInfo

print("Completed imports, time:{} \n".format(time.time() - prev_t))
prev_t = time.time()

	
escapes = ''.join([chr(char) for char in range(1, 32)])
escape_space = ''.join([' ' for _ in range(1, 32)])
translator = str.maketrans(escapes, escape_space)

model_file = "./model/distilBERT"
tokenizer_file = "./model/distilTokenizer"
idx2vertidx_file = "./idx2verticalidx.json"
vertidx2vert_file = "./verticalidx2vertical.json"
ytModel_path = "./ytModel"

tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_file)
model = TFDistilBertModel.from_pretrained(model_file)
ytModel = tf.keras.models.load_model(ytModel_path)

with open(idx2vertidx_file, 'r') as f:
	idx2verticalidx = json.load(f)
with open(vertidx2vert_file, 'r') as f:
	vertidx2vert = json.load(f)

print("Completed loading dependencies, time:{}".format(time.time() - prev_t))

while True:
	try:
		url = input("Enter video url:")
		prev_t = time.time()
		info = getVideoInfo(url, byurl=True)

		if info == None:
			print("info None")
			continue

		print("Completed scraping, time:{} \n".format(time.time() - prev_t))
		prev_t = time.time()


		# Remove escape characters
		title = info["title"].translate(translator)
		desc = info["description"].translate(translator)
		keywords = [x.translate(translator) for x in info["keywords"]]

		# Remove links
		title = re.sub(r'https?://\S+', '', title)
		desc = re.sub(r'https?://\S+', '', desc)
		keywords = [re.sub(r'https?://\S+', '', x) for x in keywords]

		# Compress spaces
		title = re.sub(r' +', ' ', title)
		desc = re.sub(r' +', ' ', desc)
		keywords = [re.sub(r' +', ' ', x) for x in keywords]

		# Reduce to English
		title = re.sub(r'[^\u0041-\u005a\u0061-\u007a\u0030-\u0039.!&\'",.? ]', '', title)
		desc = re.sub(r'[^\u0041-\u005a\u0061-\u007a\u0030-\u0039.!&\'",.? ]', '', desc)
		keywords = [re.sub(r'[^\u0041-\u005a\u0061-\u007a\u0030-\u0039.!&\'",.? ]', '', x) for x in keywords]

		keywords = " ".join(keywords)

		title_lang_vec = cld2.detect(title)[-1]
		desc_lang_vec = cld2.detect(desc)[-1]
		keywords_lang_vec = cld2.detect(keywords)[-1]

		print("detected language for \ntitle:{} \ndescription:{} \nkeywords:{}".format(title_lang_vec, desc_lang_vec, keywords_lang_vec))
		print("preprocessed TITLE:{} \n".format(title))
		print("preprocessed DESCRIPTION:{} \n".format(desc))
		print("preprocessed KEYWORDS:{} \n".format(keywords))

		vid_info_proc = {}
		vid_info_proc["words"] = ". ".join([keywords, title])
		# vid_info_proc["words"] = ". ".join([title, keywords, desc])


		for k in ["likeCount", "dislikeCount", "viewCount", "length"]:
			vid_info_proc[k] = 0.1*np.math.log10(info[k] + 1)

		vector = []

		print("Completed preprocessing, time:{} \n".format(time.time() - prev_t))
		prev_t = time.time()

		ip = tokenizer(vid_info_proc["words"], return_tensors='tf', truncation=True)
		op = model(ip)
		x = op.last_hidden_state
		x = tf.squeeze(x)
		x = x[0]
		vector.append(x)

		for k in ["length", "viewCount", "likeCount", "dislikeCount"]:
			vector.append(np.array([vid_info_proc[k]]))

		vector = np.hstack(vector)
		vector = np.expand_dims(vector, axis=0)

		predicted_vertical = np.argmax(np.squeeze(ytModel.predict(vector)))
		predicted_vertical = vertidx2vert[str(predicted_vertical)]
		print("Predicted class:{}".format(predicted_vertical))

		print("Completed time:{} \n".format(time.time() - prev_t))
		prev_t = time.time()
	
	except:
		continue