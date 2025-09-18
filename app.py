import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# A secret key is needed to manage user sessions securely
app.secret_key = 'your_very_secret_key_here' 

IMAGE_FOLDER = os.path.join('static', 'images')

def load_words():
    """Loads words and image paths from the static/images folder."""
    words = []
    if os.path.exists(IMAGE_FOLDER):
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                word = os.path.splitext(filename)[0]
                words.append({'word': word, 'path': os.path.join('images', filename)})
    return words

words_list = load_words()

@app.route('/')
def game():
    """Displays the main game page with a new random image."""
    # Initialize score if it doesn't exist in the session
    if 'score' not in session:
        session['score'] = 0
    
    if not words_list:
        return "Error: No images found in 'static/images'. Please add some.", 500
    
    current_item = random.choice(words_list)
    session['correct_word'] = current_item['word']
    
    # Pass the current score to the template
    return render_template('index.html', 
                           image_path=current_item['path'], 
                           score=session.get('score', 0))

@app.route('/check', methods=['POST'])
def check_answer():
    """Checks the user's guess and shows the result."""
    user_guess = request.form.get('guess', '').strip().lower()
    correct_word = session.get('correct_word', '')
    
    is_correct = (user_guess == correct_word.lower())
    
    # If correct, add 10 points to the score
    if is_correct:
        session['score'] = session.get('score', 0) + 10
    
    # Pass the updated score to the result template
    return render_template('result.html', 
                           is_correct=is_correct, 
                           correct_word=correct_word, 
                           user_guess=user_guess,
                           score=session.get('score', 0))

@app.route('/reset')
def reset():
    """Resets the score and starts a new game."""
    session['score'] = 0
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
