import preprocess
import os
import json

json_folder = "./jsondata100/"
out_json_folder = "./preprocessed_jsondata/"

for jsonpath in os.listdir(json_folder):
	jsondict = preprocess.preprocess(json_folder + jsonpath)
	with open(out_json_folder+"preproc_"+jsonpath, 'w') as f:
		json.dump(jsondict, f, ensure_ascii=False)