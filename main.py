import requests
from bs4 import BeautifulSoup


def rss_list(html):
	"""return the list of all pages containing rss feed"""
	soup = BeautifulSoup(html.content,'html.parser')

	all_p = soup.find('div',{'id':'main-copy'}).find_all('p')[1:] # skip first text paragraph 

	all_topics = []
	for p in all_p:
		tr_li = p.find('table').find_all('tr')  # for each table in each paragraph select its rows
		topics = []
		i=1 								    # ith element of tr
		for tr in tr_li: 					    # for each row in set of rows 
			td_text = tr.find('td').a.td_text  	# content name
			td_li = tr.find('td').a.get('href') # link
			topics.append({'#':i,'text':td_text,'li':td_li}) # append to the list
			i += 1 								# incriment element number
		all_topics.append(topics)				# append to topics list

	return all_topics							# return the list

def rss_page(element):
	""" Return each news elements"""
	url = element['li'] 		# gather the link of the given element
	
	xml = requests.get(url) 	# scraping the link

	if xml.status_code == 200:
		xml_soup = BeautifulSoup(xml.content,'xml')
		items = xml_soup.find_all('item')

		# using list comprehension to extract news title, description etc
		item_list = [{'title':item.find('title').text,'desc':item.find('description').text,'li':item.find('link').text,'dt':item.find('pubDate').text} for item in items]
		return item_list # return the list
	else:
		print('Unable to connect') 
		return []        # if connection error then return an empty list

def show_news(news):
	"""Display the news"""
	for n in news:
		print('{}\n\n{}\n\nlink : {}\n\ndate : {}\n\n\n'.format(n['title'],n['desc'],n['li'],n['dt'])) # print news

main_url = 'https://timesofindia.indiatimes.com/rss.cms'

html = requests.get(main_url)

if html.status_code == 200:
	topic_list = rss_list(html)

	# menu for different section
	print('choose one section...\n1: Main feed\n2: Cities\n3: World\n4: Blogs \n5: Option\n6: Sunday TOI\n7: Others\n')
	while True:  # loop to handle incorrect input
		choice = int(input('Enter choice : '))
		if choice in range(1,7):
			break
		else:
			print('Invalid choice enter again.....')

	print('\n')
	sub_topic = topic_list[choice-1] # choose the section
	for sub_element in sub_topic: 
		print('{} {}'.format(sub_element['#'],sub_element['text'])) # display all the subtopics

	while True: # loop to handle incorrect input
		choice = int(input('Choose an option : '))
		if choice in range(1,len(sub_topic) + 1):
			break
		else:
			print('Invalid choice enter again.....')
	news = rss_page(sub_topic[choice-1]) # select appropriate link 
	show_news(news) # call show_news method to display the news
else:
	print('Unable to connect') # handle connection problems
