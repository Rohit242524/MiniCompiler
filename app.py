from flask import Flask
from routes.main import routes

app = Flask(__name__)
routes(app)

if __name__ == '__main__':
    app.run(debug=True)