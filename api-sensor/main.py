from flask import Flask
from routes.sensor import sensor


app = Flask(__name__)
app.register_blueprint(sensor)


@app.route('/')
def index():
    return 'ok'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
