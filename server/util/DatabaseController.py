import mysql.connector
import configparser

class DatabaseController:

	def __init__(self, mysql_file):
		config = configparser.RawConfigParser()
		config.read(mysql_file)
		host = config.get('MYSQL', 'host').strip('"')
		user = config.get('MYSQL', 'user').strip('"')
		password = config.get('MYSQL', 'passwd').strip('"')
		database = config.get('MYSQL', 'database').strip('"')

#		print('DatabaseController.host = ', host)

		try:
			self.db = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
#			print("Sucessfully connected to database")
		except mysql.connector.Error as e:
			if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Incorrect username or password.")
			elif e.errno == errorcode.ER_BAD_DB_ERROR:
				print("Could not find database - ", database)
			else:
				print(e)

	def print_db_info(self):
		print('Database for MOVR')

	def get_all_films(self, service):
		cursor = self.db.cursor()
		sql = 'SELECT * FROM {}'.format(service)

		films = []
		try:
			cursor.execute(sql)
			films = cursor.fetchall()
		except:
			print('[x] DatabaseController.get_all_films() - An Error Occurred')
		finally:
			cursor.close()
			return films

	def insert_film(self, service, film_id, film_name):
		print('Inserting into {} table: {} - {}'.format(service, film_id, film_name))
		cursor = self.db.cursor()
		film_name = film_name.strip()

		sql = "INSERT INTO {} (film_id, film_name) VALUES (%s, %s)".format(service)

		data = (film_id, film_name)

		#TODO: Protect against duplicate entries
		try:
			cursor.execute(sql, data)
			self.db.commit()
		except:
			print('[x] DatabaseController.insert_film() - An Error Occurred')
		finally:
			cursor.close()

	def get_number_of_films(self, service):
		cursor = self.db.cursor()

		sql = "SELECT COUNT(*) FROM {}".format(service)
		
		cursor.execute(sql)
		return cursor.fetchone()[0]

	def get_film_info(self, service, film_id):
		cursor = self.db.cursor()

		sql = "SELECT * FROM {} WHERE film_id={}".format(service, film_id)

		print('Searching {} Table For {} id'.format(service, film_id))
		print('sql statement: {}'.format(sql))
		
		try:
			cursor.execute(sql)
			film_info = cursor.fetchone()
			self.db.commit()
		except mysql.connector.Error as err:
			print('[x] DatabaseController.get_film_info() - {}'.format(err))
		finally:
			cursor.close()
			return film_info

	def add_imdb_id(self, service, imdb_id, film_id):
		cursor = self.db.cursor()

		sql = 'UPDATE {} SET imdb_id=%s WHERE film_id=%s'.format(service)
		data = (imdb_id, film_id)
		
		try:
			cursor.execute(sql, data)
			self.db.commit()
		except Exception as e:
			print('[x] DatabaseController.add_imdb_id() - Failed')
			print(e)
		finally:
			cursor.close()

	def add_film_desc(self, service, imdb_desc, film_id):
		cursor = self.db.cursor()

		sql = 'UPDATE {} SET film_desc=%s WHERE film_id=%s'.format(service)
		data = (imdb_desc, film_id)

		try:
			cursor.execute(sql, data)
			self.db.commit()
		except Exception as e:
			print('[x] DatabaseController.add_film_desc() - Failed')
			print(e)
		finally:
			cursor.close()


class DbTests:
	def __init__(self):
		self.db = DatabaseController('../res/mysql_data.cfg')
		print('Starting DbTests...')

		count = self.db.get_number_of_films('netflix')
		print(count)

		wreck_it_ralph = self.db.get_film_info('netflix', 10300131)
		print(wreck_it_ralph)

		#10100146 | The Ridiculous 6                                   |    NULL
		self.db.add_imdb_id('netflix', 2479478, 10100146)
		ridic6 = self.db.get_film_info('netflix', 10100146)
		print(ridic6)

		self.db.add_film_desc('netflix', 'The Ridiculous 6', 10100146)
		ridic6 = self.db.get_film_info('netflix', 10100146)
		print(ridic6)

if __name__ == '__main__':
	tests = DbTests()