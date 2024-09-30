from flask import Flask, request
from flask_sock import Sock
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from embeddings import get_embeddings
from dotenv import load_dotenv
from os import getenv
from search import vector_search
from pinecone_init import create_pinecone
import json
from llm import generate_text
from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer
from openvino.runtime import Core
load_dotenv()

app = Flask(__name__)
sock = Sock(app)
cors = CORS(app)

PINECONE_API_KEY = getenv('PINECONE_API_KEY')
dimensions = 512
index_name = "video-embeddings"
pc = create_pinecone(api_key=PINECONE_API_KEY, index_name=index_name, dimensions=dimensions)

core = Core()
core.set_property({"CACHE_DIR": "./model_cache"})

model_id = "Gunulhona/openvino-llama-3.1-8B_int8"
model = OVModelForCausalLM.from_pretrained(
    model_id,
    device="CPU",
    ov_config={"CACHE_DIR": "./model_cache"}
)

tokenizer = AutoTokenizer.from_pretrained(model_id)

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


    print("Finished indexing vectors.")
    return 'Finished indexing vectors.'

@sock.route('/ws')
def websocket(ws):
    while True:
        data = ws.receive()
        if data:
            print(data)
            parsed_data = json.loads(data)
            url= parsed_data['url']
            video_id = url.replace('https://www.youtube.com/watch?v=', '')
            message = parsed_data['message']

            print(f"Received URL: {url}")
            print(f"Received Message: {message}")

            search_results = vector_search(pc=pc, index_name=index_name, namespace=video_id, dimensions=dimensions, query=message)

            relevant_context = ''

            if len(search_results) > 0:
                    for result in search_results:
                        print(f'{result['score']} : {result['metadata']['text']}')
                        print('----------')

                        if result['score'] > 0.5:
                            relevant_context += f'{result["metadata"]["text"]} \n'
            else:
                print("No search results found.")

            if relevant_context == '':
                llm_answer = generate_text(model=model, tokenizer=tokenizer, context="No context available.", input_text=message)
                print(llm_answer)
                ws.send(f"{llm_answer}")
            else:
                llm_answer = generate_text(model=model, tokenizer=tokenizer, context=relevant_context, input_text=message)
                print(llm_answer)
                ws.send(f"{llm_answer}")

if __name__ == '__main__':
    app.run(debug=True)
