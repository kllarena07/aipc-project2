from flask import Flask, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import base64

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

@app.route('/upload', methods=['POST'])
def receive_image():
    received_data = request.get_json()
    data_url = received_data.get('dataURL')

    # Extract the base64 image data from the data URL
    image_data = data_url.split(',')[1]

    # Decode the base64 image data
    image_bytes = base64.b64decode(image_data)

    # Save the image to disk
    with open('image.jpg', 'wb') as f:
        f.write(image_bytes)

    return 'Image saved.'

if __name__ == '__main__':
    app.run()
