from flask import Flask, request, jsonify, json
from flask_api import status
from datetime import datetime

import random
import logging
import threading

from util.DatabaseController import DatabaseController
import util.constants as constants

application = Flask(__name__)
db_access = DatabaseController('res/mysql_data.cfg')

@application.route('/')
def hello():
	return 'MOVR Home Page with Flask imports, flask_api, datetime, random and logging'

@application.route("/test", methods=['GET'])
def test():
	return 'MOVR Running on Amazon Elastic Beanstalk connected to an Amazon RDS MySQL Database', status.HTTP_200_OK

@application.route("/getTop100", methods=['GET'])
def getTop100():
	db_access.print_db_info()
	films = dict()
	base_film_id = 10100000
	for i in range(0, 10):
		film_id = base_film_id + i
		films[i] = get_film_info('imdb_top_100', film_id)

	return jsonify(films), status.HTTP_200_OK

def thread_get_movies(thread_id, service):
	pass


@application.route("/getMovies_t", methods=['GET'])
def get_movies_t():
	#Process services first
	services = request.args.get('services')
	if(services == None):
		return "No Services Provided", status.HTTP_400_BAD_REQUEST
	services = as_list(services)
	for service in services:
		try:
			thread.start_new_thread(thread_get_movies, ('{}-thread'.format(service), service, 0))
			return 'Threading Not Implemented Yet'
		except:
			print('Thread Exception')



@application.route("/getMovies", methods=['GET'])
def get_movies():
	service = request.args.get('service')
	num_films = request.args.get('numFilms')
	genres = request.args.get('genres')

	genres = get_genres_as_list(genres)
	logging.info('Request from [TODO] with parameters: \n\tService: %s\n\tnum_films: %s\n\tgenres: %s', service, num_films, genres)

	db_access.print_db_info()

	#films = []
	films = dict()

	for i in range(0, 20):
		random_film_id = get_random_film_id(service, genres[0])
		#print('Randomly Generated Film ID: {}'.format(random_film_id))
		print(i)
		#films.append(get_film_info(service, random_film_id))
		films[i] = get_film_info(service, random_film_id)

	#print('Film List: ', films)
	return jsonify(films), status.HTTP_200_OK


def get_random_film_id(service, genre):
	service_code = constants.services[service]
	genre_code = constants.genre_codes[genre]

	max_film_count = get_number_of_films(service, genre)
	print('Max Film Count For Service [{}] = '.format(service), max_film_count)

	film_code = random.randint(0, max_film_count)

	film_id = service_code + genre_code + film_code

	return film_id

def as_list(obj):
	return obj.split(",")

def get_genres_as_list(genres):
	return genres.split(",")

def get_film_info(service, film_id):
	return db_access.get_film_info(service, film_id)

def get_number_of_films(service, genre):
	return constants.service_genre_sizes['{}_{}_size'.format(service, genre)]

if __name__ == "__main__":
	application.config['JSON_SORT_KEYS'] = False
	application.debug = True
	application.run()