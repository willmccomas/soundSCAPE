# soundSCAPE

soundSCAPE is a Flask-based web application for rating and reviewing albums using data from the Spotify Web API.

The project started as a simple album review website and has grown into a personal music-ranking application with persistent reviews, customizable ratings, album artwork, search, sorting, and album-themed backgrounds.

## Features

* Search for albums using the Spotify Web API
* Dynamic album information and artwork
* Rate albums using whole and half-star ratings
* Write and edit album reviews
* Delete reviews
* View individual album review pages
* View all rated albums in a grid
* Sort rated albums by:

  * Release date — newest first
  * Release date — oldest first
  * Highest rated
  * Lowest rated
  * Newest reviewed
  * Oldest reviewed
  * Album name A–Z
  * Album name Z–A
* Generate dynamic album-themed page backgrounds
* Responsive layout for smaller screens
* Persistent review data using SQLite

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

## Project Structure

The project uses Flask routes and Jinja2 templates to dynamically generate pages. Album information is retrieved through Spotify's API, while reviews and album data are stored in a local SQLite database.

## Future Improvements

* Deploy SoundScape as a live website
* PostgreSQL or another production database
* User accounts and authentication
* Support for multiple users and user-specific reviews
* Public user profiles
* Album and artist statistics
* More advanced music-ranking features
* Song ratings and rankings
* Social features such as comments and following
* Additional sorting and filtering options

## Development

SoundScape is an ongoing personal project focused on learning web development, APIs, databases, and full-stack application development with Python and Flask.
