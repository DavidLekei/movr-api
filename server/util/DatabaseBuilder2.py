import constants
import sys
import requests
import shutil
from os import listdir

from DatabaseController import DatabaseController
from Cinematerial import Cinematerial
from MyMDb import MyMDb
from ImageUtils import ImageUtils
import constants as constants

class DatabaseBuilder2:

	def __init__(self):
		self.db = DatabaseController('../res/mysql_data.cfg')
		self.cin = Cinematerial()

	def run(self):
		netflix_code = constants.services['netflix']
		
		for genre in constants.genre_codes:
			code = constants.genre_codes[genre]
			filename = 'netflix_{}.txt'.format(genre)
			self.build('movie_lists/{}'.format(filename), netflix_code + code)

	def get_poster(self, film_name, imdb_id):
		self.cin.get_poster(film_name, imdb_id);

	def build_top_100(self):
		imdb = MyMDb()
		film_count = 10100000
		for f in listdir('C:/Users/David/Desktop/imdb_top_100/'):
			film_id = film_count
			imdb_id = f.split('.')[0]
			info = imdb.get_film_info_ii(imdb_id)
			self.db.insert_film('imdb_top_100', film_id, info)
			film_count = film_count + 1


	def build(self, input_file, start_film_id):
		imdb = MyMDb()
		films = {}
		film_count = 0
		try:
			movie_list = open(input_file, 'r', encoding='utf-8')
		except:
			print('ERROR: Could not open file: ', input_file)
			sys.exit()

		with movie_list:
			print('Reading From: ', input_file)
			for movie in movie_list:
				if movie in films:
					print('Skipping {} - Already in Database'.format(movie))
				else:
					films[movie] = True
					film_id = start_film_id + film_count
					info = imdb.get_film_info(movie)
					print(film_id)
					film_count = film_count + 1
					self.insert_film(film_id, info)
					self.get_poster(movie, info.imdb_id)

	def insert_film(self, film_id, film_info):
		try:
			self.db.insert_film('netflix', film_id, film_info)
		except:
			print('ERROR: Failed to insert: ', film_info.name)



if __name__ == '__main__':
	db = DatabaseBuilder2()
	db.build_top_100()
	# db.run()
	# db.build('suzie', 'action')

