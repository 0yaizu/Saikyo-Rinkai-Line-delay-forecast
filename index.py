import sqlite3

search_settings = {
	"search_time": "first_seven",
	"rain": True
}

def get_delay_percentage():
	dbname = 'saikyo_line_delay_history.db'
	conn = sqlite3.connect(dbname)
	delay_time = 0
	all_count = 0
	for row in conn.execute(f"""SELECT COUNT({search_settings["search_time"]}) FROM delay_time WHERE {search_settings["search_time"]};"""):
		delay_time = int(row[0])
		print('遅延発生回数: ' + str(delay_time))
	for row in conn.execute(f"""SELECT COUNT(*) FROM delay_time;"""):
		all_count = int(row[0])
		print('日数: ' + str(all_count))
	print('遅延発生率: ' + str(round(delay_time / all_count * 100, 4)) + '%')
	conn.close()

get_delay_percentage()