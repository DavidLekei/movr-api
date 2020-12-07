# movr-api

HTTP API server for [movr][https://github.com/DavidLekei/movr]

(DISCLAIMER: This project is still a work in progress. In it's current state, it serves as a high fidelity prototype.)

## About

movr-api accepts and processes requests for Movie/TV Show information based on: 
	
	- Service (Netflix/Amazon Prime/etc)
	- Genre

movr-api will return JSON data containing:

	- Title
	- IMDb Rating
	- Description
	- Year of release
	- URL to the movie's poster


## Technology used

movr was developed in Android Studio using Flutter for cross platform on Android/iOS.

movr-api is written in Pythong using the Flask framework, running on Amazon's ElasticBeanstalk.

All movie data was scraped from the web using scrapers I wrote in Python. 

Amazon's RDS was used for a MySQL server to store movie/tv show data.

Amazon's S3 was used to store posters.

## Files

### Server/

#### application.py

The main file that get's executed to run the server.

#### movr_tests.py

Used to easily test the endpoints defined in application.py

### Server/Util/

#### Cinematerial.py

A web-scraper class used to retrieve High Definition posters from Cinematerial.com

#### DatabaseBuilder2.py

A web-scraper script used to build the movr database. It uses the Cinematerial and MyMDB classes to retrieve data from Cinematerial.com and IMDb.com. It then uses DatabaseController.py to store the data in the movr database and ImageUtils.py to save the Poster files.

#### DatabaseController.py

A class used to control access to the movr database. Basically a wrapper around SQL commands with some additional input validation.

#### FilmInfo.py

A simple data class used to pass information about a Film (Title/Rating/Year/Description/Poster URL)

#### ImageUtils.py

Provides utility methods for handling Images. This was used to save the Posters to disk.

#### PosterBuilder.py

Deprecated - All functionality of this file ended up being refactored into seperate files.

#### Constants.py

Defines global constants, which are information about services/genres (Such as Netflix Genre codes)

## Author

David Lekei

## License

