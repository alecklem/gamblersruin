from flask import Flask

app = Flask(__name__)

# API route
@app.route("/example")
def example():
    # API call
    return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True)