import requests
from bs4 import BeautifulSoup

main_url = 'https://timesofindia.indiatimes.com/rss.cms'

html = requests.get(main_url)

if html.status_code == 200:
	
	soup = BeautifulSoup(html.content,'html.parser')

	all_p = soup.find('div',{'id':'main-copy'}).find_all('p')[1:]

	all_topics = []
	for p in all_p:
		tr_li = p.find('table').find_all('tr')
		topics = []
		for tr in tr_li:
			td_text = tr.find('td').a.text
			td_li = tr.find('td').a.get('href')
			topics.append({'text':td_text,'li':td_li})
		all_topics.append(topics)

	for topics in all_topics:
		for t in topics:
			print(t['text'])
		print('\n\n')
else:
	print('Unable to connect')