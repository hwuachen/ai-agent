from flask import Flask, request, render_template
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
import config
import openai
from aihelplib import *

app = Flask(__name__)

openai.api_key = config.OPENAI_API_KEY


@app.route("/index")
def home():
  return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
  user_message = request.form["user_message"]

  # Call your chatbot function here to get a response
  bot_response = get_bot_response(user_message)

  return {
    "user_message": user_message,
    "bot_response": bot_response
  }

def get_bot_response(user_message):
    # Predefined messages
    predefined_messages = [
        "Hi, how can I assist you?",
        "What brings you here today?",
        "How can I help you?",
        "Is there anything specific you would like to know?"
    ]

    # Combine user message and predefined messages
    messages = predefined_messages + [user_message]

    # Generate a response from ChatGPT
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     messages=[
    #         {"role": "system", "content": message} for message in messages
    #     ],
    #     max_tokens=50,
    #     temperature=0.7,
    #     n=1,
    #     stop=None
    # )
    # # Extract and return the generated response
    # bot_response = response.choices[0].message.content.strip()
    
    bot_response = messages[1]

    return bot_response

@app.route('/static/<path:filename>')
def serve_static(filename):
   # create a search input template that send a search to the backend
  return app.send_static_file(filename)

@app.route('/')
def search_form():
  return render_template('search_form.html')

@app.route('/search')
def search():
  # Get the search query from the URL query string
  query = request.args.get('query')
  result = []
  if query:
    print(query)
    results = test_search_function(query) # does not work
    #results = gpt_search_function(query)     
    
    # output the result to console for debugging
    print(results)

    # Render the search results template, passing in the search query and results
    return render_template('search_results.html', query=query, results=results)

def test_search_function(query):
  items = ['apple', 'banana', 'mango', 'orange']
  return items

def gpt_search_function(query): 
  #search_term_vector = get_embedding(query, engine="text-embedding-ada-002")
  search_term_vector = get_avg_embedding(query)

  df = pd.read_csv('earnings-embeddings.csv')
  df['embedding'] = df['embedding'].apply(eval).apply(np.array)
  df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
  sorted_by_similarity = df.sort_values("similarities", ascending=False).head(3)
  results = sorted_by_similarity['text'].values.tolist()

if __name__ == '__main__':
  app.run(debug=True, port=5000)