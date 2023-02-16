from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from replit import db
import random, string

app = Flask(__name__)
CORS(app)

@app.route('/')
def app_index():
    return render_template('index.html')

@app.route('/<key>')
def app_key(key):
    if (d := db.get(key)):
        d['views'] += 1
        db[key] = d
    return redirect(db.get(key, {}).get('url', '/'))

@app.route('/<key>.json')
def app_key_data(key):
    return jsonify(db.get(key, {}))

@app.route('/api/create', methods=['POST'])
def api_create():
    url = request.form['url']
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    c = 4
    key = ''.join([random.choice(chars) for _ in range(c)])
    while key in list(db.keys()):
        c += 1
        key = ''.join([random.choice(chars) for _ in range(c)])
    db[key] = {
        'url': url,
        'views': 0
    }
    return jsonify({'key': key, 'url': f'https://{request.host}/{key}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)