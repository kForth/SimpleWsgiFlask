from flask import Flask

# This is a pretty bad website, you should make a better one.

app = Flask(__name__)  # this is the Flask object you need for line 8 of your wsgi file.

@app.route('/')
def index():
	return 'It works!'