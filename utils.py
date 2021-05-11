import requests
import re
from bs4 import BeautifulSoup
import json
import os



def getYtid(localId):
	url = "http://data.yt8m.org/2/j/i/" + localId[:2] + "/" + localId + ".js"
	page = requests.get(url)
	videoId = None
	
	if page.ok:
		videoId = page.content.decode("utf-8").split('"')[3]
	
	return videoId

def getVideoInfo(id):
	url = "https://www.youtube.com/watch?v=" + id
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	soup.find_all("script", recursive=False)

	str_head1 = "var ytInitialData = "
	str_head2 = "var ytInitialPlayerResponse = "
	
	for tag in soup.find_all("script"):
		if tag.string != None and str_head1 in tag.string:
			json_string = tag.string[tag.string.find(str_head1)+len(str_head1):-1]
			json_data = json.loads(json_string)
			break
	
	video_info = {}

	try:
		video_info["likeCount"] = json_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
		video_info["dislikeCount"] = json_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]

		likes = re.sub("\D", "", video_info["likeCount"])
		if likes == '': likes = '0'
		video_info["likeCount"] = int(likes)

		dislikes = re.sub("\D", "", video_info["dislikeCount"])
		if dislikes == '': dislikes = '0'
		video_info["dislikeCount"] = int(dislikes)

		for tag in soup.find_all("script"):
			if tag.string != None and str_head2 in tag.string:
				json_string = tag.string[tag.string.find(str_head2)+len(str_head2):-1]
				json_data = json.loads(json_string)
				with open("json-sample.json", "w") as f:
					f.write(json_string)
				break
		
		video_info["videoId"] = json_data["videoDetails"]["videoId"]
		video_info["title"] = json_data["videoDetails"]["title"]
		video_info["description"] = json_data["videoDetails"]["shortDescription"]
		video_info["length"] = int(json_data["videoDetails"]["lengthSeconds"])
		video_info["keywords"] = []
		video_info["viewCount"] = int(json_data["videoDetails"]["viewCount"])

		if "keywords" in json_data["videoDetails"].keys():
			video_info["keywords"] = json_data["videoDetails"]["keywords"]
	
	except Exception as e:
		print(url)
		print(e)
		video_info = {}

	return video_info

def getTfRecords(folder):
	files = os.listdir(folder)
	record_files = []

	for f in files:
		if f.split('.')[-1] == "tfrecord":
			record_files.append(folder + f)
	
	return record_files

if __name__ == "__main__":
	folder = "./rawdata/"
	print(getTfRecords(folder))