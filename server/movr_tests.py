#movr_tests.py
import requests
import json
import pprint

def test_endpoints():
	printer = pprint.PrettyPrinter(indent=2)
	print('Testing /get_movies...')
	response = requests.get('http://localhost:5000/getMovies?service=netflix&numFilms=20&genres=action,drama,scifi')
	response = json.loads(response.text)
	printer.pprint(response)
	
def run_tests():
	test_endpoints()

if __name__ == '__main__':
	run_tests()