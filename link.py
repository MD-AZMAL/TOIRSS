import requests
from bs4 import BeautifulSoup


def rss_list(html):
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

main_url = 'https://timesofindia.indiatimes.com/rss.cms'

html = requests.get(main_url)

if html.status_code == 200:
	topic_list = rss_list(html)

	for sub_topic in topic_list:
		for sub_element in sub_topic:
			print('{} \t {}'.format(sub_element['#'],sub_element['text']))
		print('\n\n')

else:
	print('Unable to connect')