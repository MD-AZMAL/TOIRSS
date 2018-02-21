import requests
from bs4 import BeautifulSoup


def rss_list(html):
	"""return the list of all pages containing rss feed"""
	soup = BeautifulSoup(html.content,'html.parser')

	all_p = soup.find('div',{'id':'main-copy'}).find_all('p')[1:]

	all_topics = []
	for p in all_p:
		tr_li = p.find('table').find_all('tr')
		topics = []
		i=1
		for tr in tr_li:
			td_text = tr.find('td').a.text
			td_li = tr.find('td').a.get('href')
			topics.append({'#':i,'text':td_text,'li':td_li})
			i += 1
		all_topics.append(topics)

	return all_topics

def rss_page(element):
	""" Return each news elements"""
	url = element['li']
	
	xml = requests.get(url)

	if xml.status_code == 200:
		xml_soup = BeautifulSoup(xml.content,'xml')

		items = xml_soup.find_all('item')
		item_list = []
		for item in items:
			title = item.find('title').text
			desc = item.find('description').text
			li = item.find('link').text
			dt = item.find('pubDate').text
			item_list.append({'title':title,'desc':desc,'li':li,'dt':dt})
		return item_list
	else:
		print('Unable to connect')
		return []

def show_news(news):
	"""Display the news"""
	for n in news:
		print('{}\n\n{}\n\nlink : {}\n\ndate : {}\n\n\n'.format(n['title'],n['desc'],n['li'],n['dt']))

main_url = 'https://timesofindia.indiatimes.com/rss.cms'

html = requests.get(main_url)

if html.status_code == 200:
	topic_list = rss_list(html)

	print('choose one section...\n1: Main feed\n2: Cities\n3: World\n4: Blogs \n5: Option\n6: Sunday TOI\n7: Others\n')
	while True:
		choice = int(input('Enter choice : '))
		if choice in range(1,7):
			break
		else:
			print('Invalid choice enter again.....')

	print('\n')
	sub_topic = topic_list[choice-1]
	for sub_element in sub_topic:
		print('{} {}'.format(sub_element['#'],sub_element['text']))

	while True:
		choice = int(input('Choose an option : '))
		if choice in range(1,len(sub_topic) + 1):
			break
		else:
			print('Invalid choice enter again.....')
	news = rss_page(sub_topic[choice-1])
	show_news(news)
else:
	print('Unable to connect')
