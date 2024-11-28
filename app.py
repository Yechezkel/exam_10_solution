from flask import Flask
from blue_prints.phone_tracker_bp import phone_tracker_bp
app = Flask(__name__)

app.register_blueprint(phone_tracker_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run( host="0.0.0.0",   port=5000 ,debug=True)


