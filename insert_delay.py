import sqlite3, requests
from bs4 import BeautifulSoup
import pandas as pd

dbname = 'saikyo_line_delay_history.db'
conn = sqlite3.connect(dbname)

req = requests.get('https://traininfo.jreast.co.jp/train_info/line.aspx?gid=1&lineid=saikyoline')
req.encoding = req.apparent_encoding
html = '埼京線（関東エリア）の運行情報・運休情報：JR東日本.html'

df = []
data = []

bsObj = BeautifulSoup(open(html), 'html.parser')

#HTMLのテーブルの行数を取得
div = bsObj.find_all('div', { 'class': 'basicTable02 tdCenter delayTable mb50 accMore_cont'})[0]
delay_table = len(div.find_all('tr')) - 1
print(delay_table)

for i in range(delay_table):
    delay_before = bsObj.find_all('div', { 'class': 'basicTable02 tdCenter delayTable mb50 accMore_cont'})[0].find_all('tr')[i]

    for l in range(6):
        data = []
        for j in delay_before.find_all('td'):
            if j.find('a') != None:
                if '分別ウィンドウで開きます' in j.find('a').get_text():
                    # print(j.find('a').get_text().replace('分別ウィンドウで開きます', ''))
                    data.append(j.find('a').get_text().replace('分別ウィンドウで開きます', ''))
                if '分以上別ウィンドウで開きます' in j.find('a').get_text():
                    # print(j.find('a').get_text().replace('分以上別ウィンドウで開きます', ''))
                    data.append(j.find('a').get_text().replace('分以上別ウィンドウで開きます', ''))
            else:
                if '月' in j.get_text():
                    # print('2024/' + j.get_text().replace('月', '/').replace('日', ''))
                    data.append('2024/' + j.get_text().replace('月', '/').replace('日', ''))
                else:
                    # print(j.get_text().replace('-', 'null'))
                    data.append(j.get_text().replace('-', 'null'))
    df.append(data)
df.pop(0)

df_ins = pd.DataFrame(df, columns=['date', 'first_seven', 'seven_ten', 'ten_sixteen', 'sixteen_twentyone', 'twentyone_last'])

df_ins.to_sql('delay_time', conn, if_exists='append', index=False)

df_sel = pd.read_sql('SELECT * FROM delay_time', conn)
print(df_sel)