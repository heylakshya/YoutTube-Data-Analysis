import os

def get(folder):
	files = os.listdir(folder)
	record_files = []

	for f in files:
		if f.split('.')[-1] != "tfrecord":
			record_files.append(f)
	
	return record_files

if __name__ == "__main__":
	folder = "../rawdata"
	print(get(folder))
