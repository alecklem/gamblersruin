from flask import Flask
from nba_api.stats.endpoints import playercareerstats


app = Flask(__name__)

# API route
@app.route("/example")
def example():
    # API call

    return

if __name__ == "__main__":
    app.run(debug=True)