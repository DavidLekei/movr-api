import requests
import shutil
from bs4 import BeautifulSoup
from imdb import IMDb

from DatabaseController import DatabaseController

class PosterBuilder:
	def __init__(self):
		print('New PosterBuilder')

	def build(self, service):

		db = DatabaseController('../res/mysql_data.cfg')
		films = db.get_all_films(service)

		for film in films:
			film_id = film[0]
			film_name = film[1]
			if(film[2] != None and film[3] == None):
				#imdb_id = self.get_image_from_imdb(film_name)
				#db.add_imdb_id(service, imdb_id, film_id)
				#imdb_id = film[2]
				imdb_id = self.get_imdb_id(film_name)
				if(imdb_id != None):
					imdb_id = self.pad_imdb_id(imdb_id)
					db.add_imdb_id(service, imdb_id, film_id)
					film_desc = self.get_film_desc(imdb_id)
					if(film_desc != None):
						db.add_film_desc(service, film_desc, film_id)

	def pad_imdb_id(self, imdb_id):
		imdb_id = str(imdb_id)
		return imdb_id.zfill(8)

	def get_image_from_imdb(self, film_name):
		
		imdb_id = self.get_imdb_id(film_name)
		if(imdb_id == None):
			return None

		print('IMDb ID: ', imdb_id)
		imdb_url = 'https://www.imdb.com/title/tt{}/'.format(imdb_id)
		print('IMDb URL: ', imdb_url)

		r = requests.get(imdb_url)
		html = BeautifulSoup(r.text, 'html.parser')
		div = html.find_all(class_='poster', limit=1)
		image_src = self.extract_src_url(div)

		if(image_src != None):
			self.write_image_to_file(image_src, '../res/posters/netflix/action/{}.jpg'.format(imdb_id))

		return imdb_id

	def get_imdb_id(self, film_name):
		imdb = IMDb()
		try:
			results = imdb.search_movie(film_name)
		except Exception as e:
			print('[x] get_imdb_id() - imdb.search_movie() failed')
		if(results == None):
			print('[x] No IMDB Results Found')
			return None
		if not results:
			print('[x] No IMDB Results Found')
			return None
		#For now, we'll assume the first result is always the correct result, since we're searching a specific Netflix-generated name
		return results[0].getID()

	def extract_src_url(self, div):
		src = None
		try:
			div = str(div)
			elements = div.split("=")
			src = elements[4].split(" ")[0]
			src = src.strip('\"')
		except:
			print('[x] extract_src_url() failed.')

		return src

	def write_image_to_file(self, image_url, file_path):
		try:
			response = requests.get(image_url, stream=True)
		except Exception as e:
			print('[x] Failed to get image url: {}'.format(image_url))
			return

		if(response.status_code != 200):
			print('[x] Could Not Connect to IMDb')
			return

		response.raw.decode_content = True

		file = open(file_path, "wb+")
		print('Saving {}'.format(file_path))
		shutil.copyfileobj(response.raw, file)
		#file.write(response.content)
		file.close()

	def get_film_desc(self, imdb_id):
		print('Getting Description For: {}'.format(imdb_id))
		imdb_url = 'https://www.imdb.com/title/tt{}/'.format(imdb_id)
		try:
			response = requests.get(imdb_url)
		except Exception as e:
			print('[x] Failed to retrieve IMDb Description for {}'.format(imdb_id))
			return None

		html = BeautifulSoup(response.text, 'html.parser')
		div = html.find_all(class_='summary_text', limit=1)
		desc = self.extract_desc(div)
		return desc

	def extract_desc(self, div):
		try:
			desc = str(div)
			desc = desc.split("\n")
			return desc[1].strip()
		except Exception as e:
			print('[x] Failed To Extract Description')
			return None





if __name__ == '__main__':
	pb = PosterBuilder()
	pb.build('netflix')
