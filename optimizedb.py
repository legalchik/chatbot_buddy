import re, sqlite3, datetime, os, sys


def dboptimize(name):
	try:
		with sqlite3.connect(f"{name}.db") as conn:
			csr = conn.cursor()
			csr.execute(f"SELECT context, reply FROM data")
			data = csr.fetchall()

		questions = []
		answers = []
		for i in range(len(data)):
			questions.append(data[i][0])
			answers.append(data[i][1])


		with sqlite3.connect(f"{name} optimize.db") as conn:
			csr = conn.cursor()
			try:
				csr.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, context TEXT NOT NULL, reply TEXT NULL)")
				print('Создание')
			except:
				csr.execute("DELETE FROM data")
				print('Обновление')

			for i in range(len(questions)):
				if questions[i] != '' and answers[i] != '':
					csr.execute("INSERT INTO data (context, reply) VALUES (?, ?)", (clear_text(questions[i]), answers[i]))
			conn.commit()

		print(f"'{name}.db' to '{name} optimize.db'")
	except Exception as e:
		print('Error:', e)
		raise




def clear_text(text):        
    text = re.sub(r'[^\w-]+', ' ', text.lower().replace('ё', 'е'))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def main():
	while True:
		name = input('\nВведите название.db БД (ctrl+c чтобы выйти): ')

		v = False
		for file in os.listdir():
			if file == name+'.db':
				v = True

		if v:
			print('Подождите...')
			dboptimize(name)
		else:
			print('Такого БД нет :(')


if __name__ == '__main__':
	try:
		os.system('cls')
		main()
	except KeyboardInterrupt:
		print('\nExit.')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)