# soundSCAPE

soundSCAPE is a Flask-based web application for rating, reviewing, and organizing albums. It uses the Spotify Web API to retrieve album information and artwork, while SQLite stores personal ratings, reviews, and a custom album queue.

The project started as a simple album review website and has grown into a personal music-ranking application with album search, whole and half-star ratings, reviews, sorting, filtering, album-themed backgrounds, Spotify and Apple Music links, and a personal listening queue.

## Features

* Search for albums using the Spotify Web API
* Display dynamic album information and artwork
* Support custom albums that are not available through Spotify
* Rate albums using whole and half-star ratings
* Write, edit, and delete album reviews
* View individual album review pages
* View all rated albums in a grid
* View a visual rating distribution
* Filter ratings by star rating
* Filter ratings by release year
* Sort rated albums by:

  * Release date — newest first
  * Release date — oldest first
  * Highest rated
  * Lowest rated
  * Newest reviewed
  * Oldest reviewed
  * Album name A–Z
  * Album name Z–A
* Generate dynamic album-themed page backgrounds based on album artwork
* Display recent ratings on the homepage
* Maintain a personal album queue
* Add and remove albums from the queue
* Pick a random album from the queue
* Automatically determine and save Apple Music album links
* Prefer explicit Apple Music versions when available
* Provide direct links to albums on Spotify and Apple Music
* Responsive layout for smaller screens

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript
* Jinja2
* Spotify Web API
* Spotipy
* Pillow
* Requests
* python-dotenv

## Project Structure

The application is built with Flask and uses Jinja2 templates to dynamically generate its pages.

Album information and artwork are retrieved through the Spotify Web API using Spotipy. Apple Music links are found through Apple's iTunes Search API.

Reviews, ratings, album information, queue data, colors, and saved Apple Music links are stored in a local SQLite database.

### Main Files

* `app.py` — Flask application, routes, and page logic
* `database.py` — SQLite database setup and database functions
* `spotify_api.py` — Spotify and Apple Music API functionality
* `image_colors.py` — Extracts dominant colors from album artwork
* `style.css` — Main stylesheet and responsive layout
* `templates/` — Jinja2 HTML templates for the application's pages

## Future Improvements

* Deploy soundSCAPE as a live website
* Move to PostgreSQL or another production database
* Add user accounts and authentication
* Support multiple users and user-specific reviews
* Create public user profiles
* Add album and artist statistics
* Add more advanced music-ranking features
* Add song ratings and rankings
* Add social features such as comments and following
* Add additional sorting and filtering options

## Development

soundSCAPE is an ongoing personal project focused on learning web development, APIs, databases, and full-stack application development with Python and Flask.

The project has evolved from a basic album review site into a more complete personal music-ranking application while continuing to serve as a hands-on way to learn new programming concepts and build practical features.