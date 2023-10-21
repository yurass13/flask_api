from flask import Flask

from blueprints.basic_endpoints import blueprint as basic_endpoints


app = Flask(__name__)
app.register_blueprint(basic_endpoints)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8080', debug=True)
