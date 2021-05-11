# Get real youtube videoId from encrypted id in youtube 8m dataset
import requests

def get(localId):
	url = "http://data.yt8m.org/2/j/i/" + localId[:2] + "/" + localId + ".js"
	page = requests.get(url)
	videoId = None
	
	if page.ok:
		videoId = page.content.decode("utf-8").split('"')[3]
	
	return videoId

if __name__ == "__main__":
	id = "nXSc"
	print(get(id))

	