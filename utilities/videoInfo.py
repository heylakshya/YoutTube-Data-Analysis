# get info for one video as a dictionary

import re
import requests
from bs4 import BeautifulSoup
import json

def get(id):
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
			# with open("json-sample.json", "w") as f:
			# 	f.write(json_string)
			break
	
	video_info = {}
	video_info["likeCount"] = json_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
	video_info["dislikeCount"] = json_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]

	video_info["likeCount"] = int(re.sub("\D", "", video_info["likeCount"]))
	video_info["dislikeCount"] = int(re.sub("\D", "", video_info["dislikeCount"]))

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

	return video_info

if __name__ == "__main__":
	id = "Y1n8F4uClUU"
	id = input("Enter VideoId:")
	info = get(id)
	print(info)
