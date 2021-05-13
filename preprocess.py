import json
import re
import numpy as np
from polyglot.detect import Detector
from polyglot.detect.base import logger as polyglot_logger
polyglot_logger.setLevel("ERROR")

escapes = ''.join([chr(char) for char in range(1, 32)])
escape_space = ''.join([' ' for _ in range(1, 32)])
translator = str.maketrans(escapes, escape_space)

def preprocess(jsonpath):
	''' returns preprocessed dict of a json file'''
	with open(jsonpath, 'rb') as f:
		file = json.load(f)

	inlen = len(file)
	invalid_keys = []

	for vidid in file:
		# Remove escape characters
		title = file[vidid]["title"].translate(translator)
		desc = file[vidid]["description"].translate(translator)
		keywords = [x.translate(translator) for x in file[vidid]["keywords"]]

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
		title_lang = Detector(title, quiet=True).language.code
		desc_lang = Detector(desc, quiet=True).language.code
		keywords_lang = Detector(keywords, quiet=True).language.code
		# if title_lang == 'en':
		# 	file[vidid]["title"] = title
		# else:
		# 	file[vidid]["title"] = ""
		# if desc_lang == 'en':
		# 	file[vidid]["description"] = desc
		# else:
		# 	file[vidid]["description"] = ""
		# if keywords_lang == 'en':
		# 	file[vidid]["keywords"] = keywords
		# else:
		# 	file[vidid]["keywords"] = ""

		if title_lang == 'en' and desc_lang == 'en' and keywords_lang == 'en':
			file[vidid]["title"] = ""
			file[vidid]["description"] = ""
			file[vidid]["keywords"] = keywords + title + desc
			for k in ["likeCount", "dislikeCount", "viewCount", "length"]:
				file[vidid][k] = 0.1*np.math.log10(file[vidid][k] + 1)
		else:
			invalid_keys.append(vidid)
	
	for k in invalid_keys:
		file.pop(k)

	outlen = len(file)
	print("success {}/{}".format(outlen, inlen))

	return file

if __name__ == "__main__":
	jsonpath = "./jsondata100/1001_1100.json"
	preprocess(jsonpath)
	# for x in file:
	# 	print(file[x]["description"])