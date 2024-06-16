import sqlite3, requests
from bs4 import BeautifulSoup

req = requests.get('https://traininfo.jreast.co.jp/train_info/line.aspx?gid=1&lineid=saikyoline')
req.encoding = req.apparent_encoding

bsObj = BeautifulSoup(req.text, 'html.parser')

items = bsObj.find_all('div', { 'class': 'basicTable02 tdCenter delayTable mb50'})[0].find_all('tr')[1]

# print('---')
# for i in items.find_all('td'):
# 	print(i)
# 	print('---')


delay_befores = bsObj.find_all('div', { 'class': 'basicTable02 tdCenter delayTable mb50 accMore_cont'})[0].find_all('tr')[1]

print('---')
for i in delay_befores.find_all('td'):
	if i.find('a') != None:
		print(i.find('a').get_text().replace('分別ウィンドウで開きます', ''))
	else:
		print(i.get_text())
	print('---')