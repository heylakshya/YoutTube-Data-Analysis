import time

start_t = time.time()
import sys
import json
import re
import numpy as np
# from polyglot.detect import Detector
# from polyglot.detect.base import logger as polyglot_logger
import pycld2 as cld2
import transformers
from transformers import DistilBertTokenizer, TFDistilBertModel
import tensorflow as tf
# import os
import json
import numpy as np
# import tqdm

tf.get_logger().setLevel('ERROR')
transformers.logging.set_verbosity_error()


from utils import getVideoInfo

print("Completed imports, time:{} \n".format(time.time() - start_t))

	
escapes = ''.join([chr(char) for char in range(1, 32)])
escape_space = ''.join([' ' for _ in range(1, 32)])
translator = str.maketrans(escapes, escape_space)


vidid = str(sys.argv[1])

info = getVideoInfo(vidid)

if info == None:
	exit()

print("Completed scraping, time:{} \n".format(time.time() - start_t))

model_file = "./model/distilBERT"
tokenizer_file = "./model/distilTokenizer"
idx2vertidx_file = "./idx2verticalidx.json"
vertidx2vert_file = "./verticalidx2vertical.json"

tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_file)
model = TFDistilBertModel.from_pretrained(model_file)

print("Completed loading BERT models, time:{}".format(time.time() - start_t))

# polyglot_logger.setLevel("ERROR")

with open(idx2vertidx_file, 'r') as f:
	idx2verticalidx = json.load(f)
with open(vertidx2vert_file, 'r') as f:
	vertidx2vert = json.load(f)

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

# if Detector(title, quiet=True).language.code == 'en' or Detector(desc, quiet=True).language.code == 'en':
# title_lang = Detector(title, quiet=True).language.code
# desc_lang = Detector(desc, quiet=True).language.code
# keywords_lang = Detector(keywords, quiet=True).language.code

title_lang_vec = cld2.detect(title)[-1]
desc_lang_vec = cld2.detect(desc)[-1]
keywords_lang_vec = cld2.detect(keywords)[-1]

print("detected language for \ntitle:{} \ndescription:{} \nkeywords:{}".format(title_lang_vec, desc_lang_vec, keywords_lang_vec))
print("preprocessed TITLE:{}".format(title))
print("preprocessed DESCRIPTION:{}".format(desc))
print("preprocessed KEYWORDS:{}".format(keywords))

# if not (title_lang == 'en' and desc_lang == 'en' and keywords_lang == 'en'):
# 	print("Some parameters of this video may not be in english.")

vid_info_proc = {}
vid_info_proc["words"] = keywords + title + desc

for k in ["likeCount", "dislikeCount", "viewCount", "length"]:
	vid_info_proc[k] = 0.1*np.math.log10(info[k] + 1)

vector = []

print("Completed preprocessing, time:{} \n".format(time.time() - start_t))

ip = tokenizer(vid_info_proc["words"], return_tensors='tf', truncation=True)
op = model(ip)
x = op.last_hidden_state
x = tf.squeeze(x)
x = x[0]
vector.append(x)

for k in ["length", "viewCount", "likeCount", "dislikeCount"]:
	vector.append(np.array([vid_info_proc[k]]))

# idx = vid_info_proc["labels"][0]

# vector.append(idx2verticalidx[str(idx)])

vector = np.hstack(vector)
vector = np.expand_dims(vector, axis=0)
# print(vector.shape)

ytModel_path = "./ytModel"
ytModel = tf.keras.models.load_model(ytModel_path)

predicted_vertical = np.argmax(np.squeeze(ytModel.predict(vector)))
predicted_vertical = vertidx2vert[str(predicted_vertical)]
print("Predicted class:{}".format(predicted_vertical))
print("Completed time:{} \n".format(time.time() - start_t))