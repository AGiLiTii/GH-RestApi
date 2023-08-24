# GH-RestApi

GitHub API Project

This project is a Flask-based API that interacts with the GitHub API to retrieve user and repository data.

# How to Run
Make sure you have Python 3 installed on your system.
Install the required dependencies using the following command:

`pip install Flask requests beautifulsoup4`

To run the Flask app, use the following command:

`make run`

This will start the Flask app and make it accessible at http://127.0.0.1:5000/.
To test the app, use the following command:

`make test`

# Cleaning Up
To remove generated cache files, use the following command:

`make clean`

Files

    github_api.py: Main Flask app file.
    github_scraper.py: Script for scraping GitHub data.
    Makefile: Provides commands for running and testing the app.

Dependencies

    Flask: A web framework for Python.
    Requests: Library for making HTTP requests.
    Beautiful Soup 4: Library for web scraping.
