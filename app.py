from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "abc123"   # required for sessions

# Words for the game
WORDS = ["python", "flask", "docker", "kubernetes", "cloud", "devops", "engineer", "computer"]

def get_scrambled_word():
    word = random.choice(WORDS)
    scrambled = "".join(random.sample(word, len(word)))
    return word, scrambled

@app.route('/')
def index():
    # If new session or reset
    if 'original_word' not in session:
        original, scrambled = get_scrambled_word()
        session['original_word'] = original
        session['scrambled_word'] = scrambled

    return render_template(
        'index.html',
        scrambled_word=session['scrambled_word']
    )

@app.route('/check', methods=['POST'])
def check():
    user_answer = request.form.get('answer').strip().lower()
    original = session['original_word']

    if user_answer == original:
        message = f"🎉 Correct! The word was **{original}**."
        session.pop('original_word', None)
        session.pop('scrambled_word', None)
        return render_template('result.html', message=message)
    else:
        message = "❌ Wrong guess! Try again."
        return render_template('index.html',
                               scrambled_word=session['scrambled_word'],
                               message=message)

@app.route('/reset')
def reset():
    session.pop('original_word', None)
    session.pop('scrambled_word', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
