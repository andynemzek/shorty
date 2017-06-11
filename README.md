# Shorty 

A simple python flask app for shortening URLs.

## Running the App

Docker is required to run this application. If you do not have it, you can get it here:

- https://www.docker.com/docker-mac
- https://www.docker.com/docker-windows

To build and run the app, simply clone this repo and run the following command:

`docker-compose up`

Once the application is running, open a browser and proceed to:

`http://localhost:5000`

## Testing the App

Run Shorty's tests with the following command:

`docker-compose run app /app-venv/bin/python /src/test.py`