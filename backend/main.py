from flask import Flask, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
cors = CORS(app)

@app.route('/post', methods=['POST'])
def receive_string():
    received_data = request.get_json()
    url = received_data.get('url')
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    output=''
    for x in transcript:
        sentence = x['text']
        output += f' {sentence}\n'

    print(output)

    return 'Received string.'

if __name__ == '__main__':
    app.run()
