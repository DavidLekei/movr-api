#movr_tests.py
import requests
import json
import pprint

def test_endpoints():
	printer = pprint.PrettyPrinter(indent=2)
	print('Testing /getTop100...')
	#response = requests.get('http://localhost:5000/getTop100')
	#response = requests.get('https://movr-292517.uc.r.appspot.com/getMovies?service=netflix&numFilms=20&genres=action,drama,scifi')
	response = requests.get('http://movr-api-env.eba-6imq5dvi.us-east-2.elasticbeanstalk.com/getTop100')
	response = json.loads(response.text)
	printer.pprint(response)
	
def run_tests():
	test_endpoints()

if __name__ == '__main__':
	run_tests()