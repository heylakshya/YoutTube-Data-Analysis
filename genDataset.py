import tensorflow as tf
import utils
import time

folder = "./rawdata/"
files = utils.getTfRecords(folder)

data_list = []

for j, file in enumerate(files):
	raw_dataset = tf.data.TFRecordDataset(file)
	for i, raw_data in enumerate(raw_dataset):
		start_t = time.time()
		tf_example = tf.train.Example.FromString(raw_data.numpy())
		data = {}
		id = tf_example.features.feature["id"].bytes_list.value[0].decode(encoding = "UTF-8")
		videoId = utils.getYtid(id)
		if videoId != None:
			# Video still exists on youtube
			data = utils.getVideoInfo(videoId)
			if bool(data):
				# Data is available
				data["labels"] = tf_example.features.feature["labels"].int64_list.value
				# print(data)
		print("evaluated file# {}/{} record# {} in {} sec".format(j+1, len(files), i+1, time.time() - start_t))