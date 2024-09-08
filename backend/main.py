from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/post', methods=['POST'])
def receive_string():
    received_data = request.get_json()
    url = received_data.get('url')
    print(url)
    return 'Received string.'

if __name__ == '__main__':
    app.run()
