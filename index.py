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
	for row in conn.execute(f'SELECT COUNT(*) FROM first_seven WHERE {search_settings[search_time]} > 0;'):
		delay_time = int(row[0])
	for row in conn.execute(f'SELECT COUNT(*) FROM {search_settings[search_time]};'):
		all_count = row[0]
	print('遅延発生率: ' + str(delay_time / all_count * 100) + '%')
	conn.close()

get_delay_percentage()