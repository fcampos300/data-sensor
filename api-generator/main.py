from flask import Flask
from routes.generate import generate


app = Flask(__name__)
app.register_blueprint(generate)


@app.route('/')
def index():
    return 'ok'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
