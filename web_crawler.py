import time
from bs4 import BeautifulSoup
import requests
import urllib

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True

def find_first_link(url):
    # get the HTML from "url", use the requests library
	response = requests.get(url)
	html = response.text
    # feed the HTML into Beautiful Soup
	soup = BeautifulSoup(html, 'html.parser')
    # find the first link in the article
	f_link = None
	div_data = soup.find(id="mw-content-text").find(class_="mw-parser-output")
	#f_link = soup.find(id='mw-content-text').p.a.get('href')
    # return the first link as a string, or return None if there is no link
    # Find all the direct children of content_div that are paragraphs
	for element in div_data.find_all("p", recursive=False):
		if element.find("a", recursive=False):
			f_link = element.find("a", recursive=False).get('href')
			break

	if not f_link: #checking if there is no links in the webpage
		return

    # Build a full url from the relative article_link url
	first_link = urllib.parse.urljoin('https://en.wikipedia.org/', f_link)

	return first_link

		
article_chain = [start_url]

while continue_crawl(article_chain, target_url): 
	print(article_chain[-1])
    # download html of last article in article_chain
    # find the first link in that html
	first_link = find_first_link(article_chain[-1])
    # add the first link to article_chain
	article_chain.append(first_link)
    # delay for about two seconds
	time.sleep(2)