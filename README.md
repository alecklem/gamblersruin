# gamblersruin

Statistics and Analytics service for prop bets


## How to Install

1. virtualenv venv
2. source venv/bin/activate
3. pip install -r requirements.txt


To run the flask server: (only need to do the export flask app line once)
```
cd flask-server
python3 -m venv venv
source venv/bin/activate
export FLASK_APP=server.py
flask run
```

```
cd client
npm start
```
