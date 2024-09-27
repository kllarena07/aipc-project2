from flask import Flask, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import base64
from embeddings import get_embeddings
from dotenv import load_dotenv
from os import getenv
from search import vector_search
from pinecone_init import create_pinecone

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

PINECONE_API_KEY = getenv('PINECONE_API_KEY')
dimensions = 512
index_name = "video-embeddings"
pc = create_pinecone(api_key=PINECONE_API_KEY, dimensions=dimensions)

@app.route('/post', methods=['POST'])
def receive_string():
    received_data = request.get_json()
    url = received_data.get('url')
    video_id = url.replace('https://www.youtube.com/watch?v=', '')

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    chunks = []

    for x in transcript:
        sentence = x['text']
        chunks.append(sentence)

    print(chunks)

    embeddings = get_embeddings(chunks, dimensions)

    upsert_data = []
    for i, (text, embedding) in enumerate(zip(chunks, embeddings)):
        upsert_data.append((
            f"id_{i}",
            embedding.tolist(),
            {"text": text}
        ))

    index = pc.Index(index_name)
    index.upsert(
        vectors=upsert_data,
        namespace=video_id
    )

    query = "What is OpenVINO?"
    search_results = vector_search(pc=pc, index_name=index_name, namespace=video_id, dimensions=dimensions, query=query)
    print("search results:", search_results)

    for result in search_results:
        print(f'{result['score']} : {result['metadata']['text']}')
        print('----------')

    print("Sending response back to client.")
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
