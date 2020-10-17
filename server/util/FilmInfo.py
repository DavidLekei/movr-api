class FilmInfo:
	def __init__(self, name, imdb_id, description, year, rating):
		self.name = name
		self.imdb_id = imdb_id
		self.description = description
		self.year = year
		self.rating = rating

	def __str__(self):
		return '{}: IMDb_id: {}\n{} ({})\n{}'.format(self.name, self.imdb_id, self.description, self.year, self.rating)