from datetime import datetime

from flask import Flask, jsonify, session
from flask_cors import CORS
from config import Config
from models import db
from routes import api



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)




with app.app_context():
    db.create_all()

# Add root URL route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

app.register_blueprint(api, url_prefix='/api')

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)

