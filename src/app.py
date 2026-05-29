"""Flask web application for generating motivational memes."""

import random
import os
import requests
from flask import Flask, render_template, abort, request

from QuoteEngine import Ingestor
from MemeEngine import MemeEngine

app = Flask(__name__)

os.makedirs('./static', exist_ok=True)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Failed to fetch image: {e}", 400

    tmp_path = f'./tmp/{random.randint(0, 1_000_000_000)}.jpg'
    os.makedirs('./tmp', exist_ok=True)
    with open(tmp_path, 'wb') as f:
        f.write(response.content)

    try:
        path = meme.make_meme(tmp_path, body, author)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
