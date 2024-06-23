import sqlite3, requests, datetime
from bs4 import BeautifulSoup

req = requests.get('https://traininfo.jreast.co.jp/train_info/line.aspx?gid=1&lineid=saikyoline')
req.encoding = req.apparent_encoding
now = datetime.datetime.now()

bsObj = BeautifulSoup(req.text, 'html.parser')

delay_latest = bsObj.find_all('div', { 'class': 'basicTable02 tdCenter delayTable mb50'})[0].find_all('tr')[1]
delay_list = []

if now.hour <= 5 and now.minute <= 0:
	delay_list.append(datetime.datetime(now.year, now.month, now.day - 1).strftime('%Y-%m-%d'))
else:
	delay_list.append(now.date().strftime('%Y-%m-%d'))

for i in delay_latest.find_all('td'):
	if i.find('a') != None:
		delay_list.append(int(i.find('a').get_text().replace('分別ウィンドウで開きます', '')))
	else:
		delay_list.append('""')
print(delay_list)

dbname = 'saikyo_line_delay_history.db'
conn = sqlite3.connect(dbname)
conn.execute(f"""CREATE TABLE IF NOT EXISTS delay_time (date Date, first_seven INT, seven_ten INT, ten_sixteen INT, sixteen_twentyone INT, twentytwo_last INT)""")

print(f"""INSERT INTO delay_time VALUES ("{delay_list[0]} 00:00:00", {delay_list[1]}, {delay_list[2]}, {delay_list[3]}, {delay_list[4]}, {delay_list[5]});""")
conn.execute(f"""INSERT INTO delay_time VALUES ("{delay_list[0]} 00:00:00", {delay_list[1]}, {delay_list[2]}, {delay_list[3]}, {delay_list[4]}, {delay_list[5]});""")

conn.close()