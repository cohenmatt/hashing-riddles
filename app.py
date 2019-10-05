"""
A riddle challenge with a twist: hashes.

Author:     Matt Cohen
Date:       06/10/2019
Version:    1.0
"""
from flask import Flask, request, send_from_directory
import hashlib

app = Flask(__name__)

# Ideally this would be in a separate file, but it was quicker to just do this
index_html = """
<!DOCTYPE html>
<html>
  <head>
    <style>
      p, h1, h2 {
        text-align: center;
        font-family: sans-serif;
      }
    </style>
  </head>
  <body>
    <h1>
      Riddles with Hashing #️⃣
    </h1>
    <br>
    <h2>
      How it works
    </h2>
    <p>
      There are 5 riddles to solve.
      <br>
      Every guess gets passed into a hash function.
      <br>
      If the hash output from your guess matches the hash of the answer,
      <br>
      you've guessed right!
      <br>
      <br>
      <strong>(Answers are in lowercase, and can include spaces)</strong>
    </p>
    <br>
    <p>
        <a class="link" href="http://cohenmatt.pythonanywhere.com/riddle1">
            Go to first riddle
            </a>
    </p>
    <br>
  </body>
</html>
"""

# The final page once all riddles have been completed
end_html = """
<!DOCTYPE html>
<html>
  <head>
    <style>
      p, h1, h2 {
        text-align: center;
        font-family: sans-serif;
      }
      .message {
        font-size: 10px;
      }
    </style>
  </head>
  <body>
    <h1>
      CONGRATS! You beat the game!
    </h1>
    <br>
    <br>
    <br>
    <br>
    <p class="message">
        so can i work for you guys pls??
    </p>
    <br>
    <p>
        <a class="link" href="http://cohenmatt.pythonanywhere.com/">
            Go to start
            </a>
    </p>
    <br>
  </body>
</html>
"""

# A riddle page template
riddle_html = """
<!DOCTYPE html>
<html>
  <head>
    <style>
        {css}
        {hash_css}
        {success_css}
    </style>
  </head>
  <body>
    <h1>
        Riddle {riddle_no}
    </h1>
    <p class="riddle">
        {riddle}
    </p>
    <br>
    <p>
        Answer hash 👇
    </p>
    <h2>
        {answer_hash}
    </h2>
    <h2 class="guess_hash">
        {guess_hash}
    </h2>
    <p>
        Guess hash ☝️
    </p>
    <div class="form" id="guess">
        <form action="/{current_riddle}">
            <input type="text" name="guess">
            <input type="submit" value="Guess">
        </form>
    </div>
    <br>
    <div class="success">
        <h2>
            {success_message}
        </h2>
        <a href="http://cohenmatt.pythonanywhere.com/{next_riddle}">
            Go to next riddle
        </a>
    </div>
  </body>
</html>
"""

# Styling for riddle pages
css = """
p, h1, h2, a, div {
    text-align: center;
    font-family: sans-serif;
}

.riddle {
    font-style: italic;
}
"""

def sha1hash(text):
    """Takes a plain text input and returns a SHA-1 hash of it."""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def create_riddle_page(number, riddle, answer, success_message):
    """Formats the html required to make a riddle page."""
    answer_hash = sha1hash(answer)
    current_riddle = "riddle" + str(number)
    next_riddle = "riddle" + str(number + 1)

    guess = request.args.get('guess')
    if not guess:
        # For the first time a user lands on a page
        guess = ""
    guess_hash = sha1hash(guess)

    if answer_hash == guess_hash:
        # Make hash green
        hash_css = ".guess_hash {color: green;}"
        # Unhide link to next riddle
        success_css = ".success {visibility: visible;}"

    else:
        # Make hash red
        hash_css = ".guess_hash {color: red;}"
        # Hide link to next riddle
        success_css = ".success {visibility: hidden;}"

    return riddle_html.format(
        riddle=riddle,
        css=css, # Global variable
        hash_css=hash_css,
        success_css=success_css,
        riddle_no=number,
        answer_hash=answer_hash,
        guess_hash=guess_hash,
        success_message=success_message,
        current_riddle=current_riddle,
        next_riddle=next_riddle)

@app.route('/')
def index():
    return index_html

@app.route('/riddle1')
def riddle1():
    NUMBER = 1
    RIDDLE = "What's brown and sticky?"
    ANSWER = "a stick"
    SUCCESS_MESSAGE = "Nice one!! 👏"

    return create_riddle_page(NUMBER, RIDDLE, ANSWER, SUCCESS_MESSAGE)

@app.route('/riddle2')
def riddle2():
    NUMBER = 2
    RIDDLE = "Where can you find roads without cars, forests without trees, cities without houses?"
    ANSWER = "a map"
    SUCCESS_MESSAGE = "Sick hash, bro 🤘🏼"

    return create_riddle_page(NUMBER, RIDDLE, ANSWER, SUCCESS_MESSAGE)

@app.route('/riddle3')
def riddle3():
    NUMBER = 3
    RIDDLE = "The more you take, the more you leave behind. What am I?"
    ANSWER = "footsteps"
    SUCCESS_MESSAGE = "It SHA-1derful world 🌏"

    return create_riddle_page(NUMBER, RIDDLE, ANSWER, SUCCESS_MESSAGE)

@app.route('/riddle4')
def riddle4():
    NUMBER = 4
    RIDDLE = "Feed me and I live. Give me drink and I die. What am I?"
    ANSWER = "a fire"
    SUCCESS_MESSAGE = "5e6b4b0d32 <-- that's SHA-1 for 'you've got an impressively large brain' 🧠"

    return create_riddle_page(NUMBER, RIDDLE, ANSWER, SUCCESS_MESSAGE)

@app.route('/riddle5')
def riddle5():
    NUMBER = 5
    RIDDLE = "What have I got in my pocket?"
    ANSWER = "a ring"
    SUCCESS_MESSAGE = "Very good, Master Baggins 💍"

    return create_riddle_page(NUMBER, RIDDLE, ANSWER, SUCCESS_MESSAGE)

@app.route('/riddle6')
def end():
    return end_html
