import constants
import sys
import requests
import shutil
import traceback

from bs4 import BeautifulSoup

from DatabaseController import DatabaseController
from ImageUtils import ImageUtils

class Cinematerial:

	def __init__(self):
		self.base_url = 'https://www.cinematerial.com'

	def search(self, film_name):
		search_url = 'https://www.cinematerial.com/search?q={}'
		search_term = film_name.replace(' ', '+')
		print('Searching: ', search_url.format(search_term));

		try:
			res = requests.get(search_url.format(search_term))
		except Exception as e:
			print('ERROR: Unable to connect to Cinematerial.')
			print(e)
			raise Exception

		html = BeautifulSoup(res.text, 'html.parser')
		table = html.find('table')
		if(table == None):
			print('Film Not Found')
			raise Exception

		row = table.find('tr')
		src = row.find('a')['href']
		src = str(src)
		return self.base_url + src


	def get_image_url(self, movie_url):
		try:
			res = requests.get(movie_url)
		except Exception as e:
			print('ERROR: Could Not Find Movie Page: ', movie_url)
			raise Exception

		html = BeautifulSoup(res.text, 'html.parser')
		div = html.find('div', attrs={'class':'poster'})
		src = div.find('a')['href']
		src = str(src)
		return self.base_url + src


	def get_image_src(self, image_url):
		try:
			res = requests.get(image_url)
		except Exception as e:
			print('ERROR: Could Not Connect To image_url: ', image_url)
			raise Exception

		html = BeautifulSoup(res.text, 'html.parser')
		img = html.find('img', attrs={'id':'poster'})['src']
		return img

	def get_poster(self, film_name, imdb_id):
		imageUtils = ImageUtils()
		image_path = '../res/hd_posters/{}.jpg'

		try:
			movie_url = self.search(film_name)
			image_url = self.get_image_url(movie_url)
			image_src = self.get_image_src(image_url)
			imageUtils.write_image_to_file(image_src, image_path.format(imdb_id))
		except Exception as e:
			print('ERROR: Failed to find poster for: ', film_name)
			print(e)
			traceback.print_exc()


	def get_posters(self, file):
		imageUtils = ImageUtils()
		image_path = '../res/hd_posters/{}.jpg'
		try:
			movie_list = open(file, 'r', encoding='utf-8')
		except:
			print('Could Not Open File: ', file)
			sys.exit()
		with movie_list:
			print('Reading From File: ', file)
			count = 0
			for movie in movie_list:
				#Assume that the movie only exists once
				try:
					movie_url = self.search(movie)
					image_url = self.get_image_url(movie_url)
					image_src = self.get_image_src(image_url)
					imageUtils.write_image_to_file(image_src, image_path.format(count))
					count = count + 1
				except:
					pass


if __name__ == '__main__':
	#Run Tests
	c = Cinematerial()
	c.get_poster('Jurassic World: Fallen Kingdom', 'tt123456')
	#c.get_poster('Venom', 'tt1270797')
	#c.get_posters('../../movie_lists/netflix_action.txt')
	
