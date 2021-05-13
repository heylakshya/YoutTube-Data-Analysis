import tensorflow as tf
import utils
import time
import json
raw_folder = "./rawdata/"
files = utils.getTfRecords(raw_folder)
json_folder = "./jsondata100/"


big_start_t = time.time()

count = 0
success_count = 0

data_list = {}
for j, file in enumerate(files):
	raw_dataset = tf.data.TFRecordDataset(file)

	for i, raw_data in enumerate(raw_dataset):
		count = count + 1
		if count<=4500:
			continue
		start_t = time.time()
		tf_example = tf.train.Example.ParseFromString(raw_data.numpy())
		data = {}
		id = tf_example.features.feature["id"].bytes_list.value[0].decode(encoding = "UTF-8")
		videoId = utils.getYtid(id)

		if videoId != None:
			# Video still exists on youtube
			data = utils.getVideoInfo(videoId)

			if bool(data):
				success_count = success_count + 1
				# Data is available
				data["labels"] = list(tf_example.features.feature["labels"].int64_list.value)
				data_list[data["videoId"]] = data


		print("Scraped file# {}/{} record# {} in {:.3f} sec".format(j+1, len(files), i+1, time.time() - start_t))

		if success_count%100 == 0:
			print("Dumping json ", str(success_count-99) + "_" + str(success_count))
			fname = str(count-99) + "_" + str(count) + '.json'
			with open(json_folder + fname, 'w') as fp:
				json.dump(data_list, fp)
			data_list = {}

	# print("Scraped {} videos with {} successes in file# {}".format(count, success_count, j))