import os
import random
from flask import Flask, render_template, request, session

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
    if not words_list:
        return "Error: No images found in 'static/images'. Please add some.", 500
    
    current_item = random.choice(words_list)
    session['correct_word'] = current_item['word']
    
    return render_template('index.html', image_path=current_item['path'])

@app.route('/check', methods=['POST'])
def check_answer():
    """Checks the user's guess and shows the result."""
    user_guess = request.form.get('guess', '').strip().lower()
    correct_word = session.get('correct_word', '')
    
    is_correct = (user_guess == correct_word.lower())
    
    return render_template('result.html', 
                           is_correct=is_correct, 
                           correct_word=correct_word, 
                           user_guess=user_guess)

if __name__ == '__main__':
    # host='0.0.0.0' allows the server to be accessible.
    # debug=True is helpful for development.
    app.run(host='0.0.0.0', port=5000, debug=True)
