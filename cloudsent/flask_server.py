import json
import couchdb
from flask import Flask, jsonify, render_template
from textblob import TextBlob

# flask  settings
app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/v1/sentiment/<message>')
def sentiment(message):
    # couchdb settings
    server = couchdb.client.Server('http://localhost:5984/')
    db = server['twitter_users']
    list = db.view('_design/default/_view/'+message)
    response = []
    for r in list:
        text = r.key
        text = TextBlob(text)
        response.append({'polarity' : str(text.polarity) , 'subjectivity' : str(text.subjectivity), 'date' : r.value})    
    return json.dumps(response)

@app.route('/api/v1/graph/<message>')
def graph(message):
    # couchdb settings
    server = couchdb.client.Server('http://localhost:5984/')
    db = server['twitter_users']
    list = db.view('_design/default/_view/'+message)
    response = []
    for r in list:
        print(r.value);
        text = r.key
        text = TextBlob(text)
        response.append({'location' : r.value})    
    return json.dumps(response)

 
if __name__ == "__main__":
    app.run(debug=True)
