import requests
from bs4 import BeautifulSoup

def get(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	with open("html-sample.html", "w") as f:
		f.write(str(soup))

if __name__ == "__main__":
	url = "https://www.youtube.com/watch?v=Y1n8F4uClUU"
	get(url)
