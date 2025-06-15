'''
Author: Lucas Stackhouse

Goal: - Front-end development of the sentiment generating app
      - Display results
'''

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    message = (
        "Welcome to the Sentiment Analysis App!<br><br>"
        "This is where we will display our results from the game sentiment generator project.<br><br>"
        "<strong>Kenji Ramcharansingh</strong><br>"
        "GitHub: <code>KenjiR1</code><br><br>"
        "<strong>Lucas Stackhouse</strong><br>"
        "GitHub: <code>lust6199</code><br><br>"
        "<strong>Nicholas Swisher</strong><br>"
        "GitHub: <code>swish0621</code><br><br>"
        "<strong>Nicole Sawtelle</strong><br>"
        "GitHub: <code>Nsawtelle</code>"
    )
    return message

if __name__ == "__main__":
    app.run()