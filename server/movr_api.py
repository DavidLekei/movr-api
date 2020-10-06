from flask import Flask, request, jsonify, json
from flask_api import status
from datetime import datetime

import logging
import random

from util.DatabaseController import DatabaseController
import util.constants as constants

movr_api = Flask(__name__)
db_access = DatabaseController('res/mysql_data.cfg')

"""
Routes

"""

@movr_api.route("/getMovies", methods=['GET'])
def get_movies():
	service = request.args.get('service')
	num_films = request.args.get('numFilms')
	genres = request.args.get('genres')

	genres = get_genres_as_list(genres)
	logging.info('Request from [TODO] with parameters: \n\tService: %s\n\tnum_films: %s\n\tgenres: %s', service, num_films, genres)

	db_access.print_db_info()

	films = []

	for i in range(0, 20):
		random_film_id = get_random_film_id(service, genres[0])
		print('Randomly Generated Film ID: {}'.format(random_film_id))
		films.append(get_film_info(service, random_film_id))

	print('Film List: ', films)


def get_random_film_id(service, genre):
	service_code = constants.services[service]
	genre_code = constants.genre_codes[genre]

	max_film_count = get_number_of_films(service, genre)
	print('Max Film Count For Service [{}] = '.format(service), max_film_count)

	film_code = random.randint(0, max_film_count)

	film_id = service_code + genre_code + film_code

	return film_id

def get_genres_as_list(genres):
	return genres.split(",")

def get_film_info(service, film_id):
	return db_access.get_film_info(service, film_id)

def get_number_of_films(service, genre):
	return constants.service_genre_sizes['{}_{}_size'.format(service, genre)]


if __name__ == "__main__":
	logging.basicConfig(filename='logs/movr_api_log.log', level=logging.DEBUG)
	movr_api.run();