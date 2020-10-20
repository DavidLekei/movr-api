import requests
from bs4 import BeautifulSoup
from FilmInfo import FilmInfo

class MyMDb:

	base_url = 'https://www.imdb.com{}'
	base_title_url = 'https://www.imdb.com/title/{}'
	base_search_url = 'https://www.imdb.com/find?q={}'

	def __init__(self):
		pass

	def get_film_info_ii(self, imdb_id):
		page = self.get_imdb_page(imdb_id)
		film_name = self.get_name(page)
		description = self.get_description(page)
		year = self.get_year(page)
		rating = self.get_rating(page)
		info = FilmInfo(film_name, imdb_id, description, year, rating)
		return info

	def get_film_info(self, film_name):
		imdb_id = self.get_id(film_name)
		page = self.get_imdb_page(imdb_id)
		description = self.get_description(page)
		year = self.get_year(page)
		rating = self.get_rating(page)
		info = FilmInfo(film_name, imdb_id, description, year, rating)
		return info

	def get_name(self, page):
		title_wrapper = page.find('div', class_='title_wrapper')
		h1 = title_wrapper.find('h1')
		title = h1.text.split('(')[0]
		return title

	def get_id(self, film_name):
		try:
			res = requests.get(self.base_search_url.format(film_name));
			search_result = BeautifulSoup(res.text, 'html.parser')
			table = search_result.find('table')
			link = table.find('a')['href']
			title_id = link.split('/')[2]
			return title_id
		except:
			self.print_error()
			raise Exception

	def get_imdb_page(self, imdb_id):
		try:
			search_url = self.base_title_url.format(imdb_id)
			print('Searching for: ', search_url)
			res = requests.get(search_url);
			return BeautifulSoup(res.text, 'html.parser')
		except:
			self.print_error()
			raise Exception

	def get_year(self, page):
		try:
			div = page.find('div', class_='title_wrapper')
			a = div.find('a')
			a = str(a)
			a = a.split('>')
			year = a[1].split('<')[0]
			return year
		except:
			self.print_error()
			raise Exception

	def get_rating(self, page):
		try:
			span = page.find('span', attrs={'itemprop':'ratingValue'})
			span = str(span)
			span = span.split('>')
			rating = span[1].split('<')
			return rating[0]			
		except:
			self.print_error()
			raise Exception

	def get_description(self, page):
		try:
			div = page.find('div', class_='summary_text')
			div = str(div)
			desc = div.split("\n")
			return desc[1].strip()
		except:
			self.print_error()
			raise Exception

	def print_error(self):
		print('ERROR: Could not connect to IMDb')

if __name__ == '__main__':
	mymdb = MyMDb()
	info = mymdb.get_film_info('Venom')