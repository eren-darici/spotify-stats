from flask import Flask, render_template
from SpotifyAPIManager import Spotify

app = Flask(__name__)

spotify = Spotify()

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/stats')
def stats():
    spotify.login()
    occurence = spotify.stats()
    return render_template('stats.html', occurence=occurence, len=len(occurence.items()))


if __name__ == '__main__':
    app.run()
