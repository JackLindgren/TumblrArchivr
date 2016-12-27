import json
import requests
import os

def getKey():
	f   = open("apikey", "r")
	key = f.read()
	key = key.rstrip()
	f.close()
	return key

def getTotalPosts(url):
	response = requests.get(postURL)
	responseJSON = json.loads(response.text)
	totalPosts = responseJSON["response"]["total_posts"]
	return int(totalPosts)

def processPhoto(url, offset):
	if not os.path.exists("Photos"):
		os.makedirs("Photos")
	response = requests.get(url)
	responseJSON = json.loads(response.text)
	postCount = offset
	for post in responseJSON["response"]["posts"]:
		os.makedirs("Photos/{0}".format(postCount))
		date = post["date"]
		tags = post["tags"]
		caption = post["caption"]
		f = open("Photos/{0}/info.txt".format(postCount), "a")
		f.write(date.encode("utf-8"))
		f.write("\n")
		f.write(caption.encode("utf-8"))
		f.write("\n")
		for tag in tags:
                        f.write(tag.encode("utf-8"))
                        f.write(",")
		f.close()
		for photo in post["photos"]:
			img_url = photo["original_size"]["url"]
			img_url = img_url.replace("https", "http")
			img_data = requests.get(img_url).content
			fileName = img_url.split('/')[-1]
			with open('Photos/{0}/{1}.png'.format(postCount, fileName), 'wb') as handler:
				handler.write(img_data)
		postCount += 1


def processText(url):
	f = open("textPosts.txt", "a")
	response = requests.get(url)
	responseJSON = json.loads(response.text)
	for post in responseJSON["response"]["posts"]:
		date  = post["date"]
		tags  = post["tags"]
		title = post["title"]
		body  = post["body"]
		f.write(date.encode("utf-8"))
		f.write("\n")
		f.write("Title: ")
		try: 
			f.write(title.encode("utf-8"))
		except AttributeError:
			pass
		f.write("\n")
		f.write("Post: ")
		f.write(body.encode("utf-8"))
		f.write("\n")
		f.write("Tags: ")
		for tag in tags:
			f.write(tag.encode("utf-8"))
			f.write(",")
		f.write("\n")
		f.write("--------------\n\n")
	f.close()
		
def processQuote(url):
	f = open("quotes.txt", "a")
	response = requests.get(url)
	responseJSON = json.loads(response.text)
	for post in responseJSON["response"]["posts"]:
		date   = post["date"]
		tags   = post["tags"]
		text   = post["text"]
		source = post["source"]
		f.write(date.encode("utf-8"))
		f.write("\n")
		f.write("Quote: ")
		f.write(text.encode("utf-8"))
		f.write("\n")
		f.write("Source: ")
		f.write(source.encode("utf-8"))
		f.write("\n")
		f.write("Tags: ")
		for tag in tags:
			f.write(tag.encode("utf-8"))
			f.write(",")
		f.write("\n")
		f.write("--------------\n\n")
	f.close()		

def getAllPosts(baseURL, total, postType):
	offset = 0
	while offset < total:
		url = baseURL + "&offset=" + str(offset)
		if postType == "text":
			processText(url)
		if postType == "photo":
			processPhoto(url, offset)
		if postType == "quote":
			processQuote(url)
		offset += 20

blogName = raw_input("enter blog name: ")
postType = raw_input("enter the post type (text, photo, quote): ")
APIKey = getKey()
print APIKey

postURL = "https://api.tumblr.com/v2/blog/{0}.tumblr.com/posts/{1}?api_key={2}".format(blogName, postType, APIKey)

totalPosts = getTotalPosts(postURL)
print totalPosts

getAllPosts(postURL, totalPosts, postType)

#offset = 0
#while offset < totalPosts:
	#get the posts
