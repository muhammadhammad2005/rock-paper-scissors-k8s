from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
# Replace with a secure secret (do NOT commit secrets to git)
app.secret_key = "replace-this-with-a-secure-secret"

@app.route('/')
def index():
    # initialize scoreboard in session
    if 'wins' not in session:
        session['wins'] = 0
        session['losses'] = 0
        session['ties'] = 0
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    if not data or 'move' not in data:
        return jsonify({'error': 'missing move'}), 400

    user_move = data['move']
    options = ['rock', 'paper', 'scissors']
    if user_move not in options:
        return jsonify({'error': 'invalid move'}), 400

    comp_move = random.choice(options)
    result = _decide_winner(user_move, comp_move)

    # Update session scoreboard
    if result == 'win':
        session['wins'] = session.get('wins', 0) + 1
    elif result == 'lose':
        session['losses'] = session.get('losses', 0) + 1
    else:
        session['ties'] = session.get('ties', 0) + 1

    return jsonify({
        'user': user_move,
        'computer': comp_move,
        'result': result,
        'score': {
            'wins': session.get('wins', 0),
            'losses': session.get('losses', 0),
            'ties': session.get('ties', 0),
        }
    })

@app.route('/reset', methods=['POST'])
def reset_score():
    session.pop('wins', None)
    session.pop('losses', None)
    session.pop('ties', None)
    return jsonify({'ok': True})

def _decide_winner(user, comp):
    if user == comp:
        return 'tie'
    wins = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    if wins[user] == comp:
        return 'win'
    return 'lose'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

