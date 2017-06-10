import logging
import random
import string

import flask
from flask import Flask
from flask_pymongo import PyMongo
import pymongo
import validators

import config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(config)
mongo = PyMongo(app)

@app.route("/", methods=["GET", "POST"])
def main():
    """
    This is the endpoint that displays the main page
    """
    logging.info("Main page accessed")

    input_url = False
    short_url = False
    error = False
    
    if flask.request.method == 'POST':
        input_url = flask.request.form['input-url']
        if len(input_url) > config.URL_LENGTH_LIMIT:
            logging.info("Input URL too long")
            error = "The URL specified is too long"
        elif not validators.url(input_url):
            logging.info("Invalid url: %s", input_url)
            error = "Please enter a valid URL"
        else:
            logging.info("Storing url: %s", input_url)
            short_url_code = store_url(input_url)
            short_url = create_short_url(short_url_code)
            logging.info("Short url created: %s", short_url)

    params = {
        "input_url": input_url,
        "short_url": short_url, 
        "error": error
    }
    template = flask.render_template('index.html', **params)

    return template

@app.route("/<string:short_url_code>")
def redirect_to_url(short_url_code):
    """
    This is the endpoint that will accept a shortened URL
    and redirect to the original URL.
    """
    logging.info("Looking up url code: %s", short_url_code)
    result = mongo.db.urls.find_one({"_id": short_url_code})
    if result is None:
        logging.info("Invalid url code")
        return "invalid short url code"

    logging.info("Redirecting to original url: %s", result['url'])
    return flask.redirect(result['url'])

def store_url(url):
    """
    Takes a URL and stores it to the DB.

    :param url:
        The URL to be shortened

    :returns:
        The short code for the URL which is also the _id
        of the saved DB record.
    """
    while True:
        try:
            short_url_code = create_random_code(
                config.CODE_LENGTH, config.CODE_ALLOWED_CHARS)
            mongo.db.urls.insert_one({
                "_id": short_url_code,
                "url": url
            })
            msg = "Created code {0} for url {1}"
            msg = msg.format(short_url_code, url)
            logging.info(msg)
            break
        except pymongo.errors.DuplicateKeyError as e:
            msg = "URL code {0} already in use, creating another"
            msg.format(short_url_code)
            logging.info(msg)
            continue
    return short_url_code

def create_random_code(length=6, allowed_chars=None):
    """
    :param length:
        The number of chars to include in the random code

    :param allowed_chars:
        The characters that are allowed in the random code

    :returns:
        The random code
    """
    if allowed_chars is None:
        allowed_chars = string.ascii_lowercase + string.digits
    url_code = ''.join(random.choice(allowed_chars) for i in range(length))
    return url_code

def create_short_url(short_url_code):
    """
    :param short_url_code:
        The code to use when creating the short url

    :returns:
        The fully qualified short URL
    """
    params = {"short_url_code": short_url_code, "_external": True}
    return flask.url_for('redirect_to_url', **params)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=config.DEBUG)