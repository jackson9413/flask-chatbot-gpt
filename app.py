import os
from flask import Flask, render_template, request
import openai 
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

#print(openai.api_key)

# Create a new Flask app
app = Flask(__name__)


# Define the home page route
@app.route('/')
def index():
    return render_template('index.html')

# define chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # get the message from the user
    user_message = request.form['message']
    
    chat_history = []
    
    # use the OpenAI API to generate a response
    prompt = f"User: {user_message}\nChatbot: "
    
    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=prompt,
      temperature=0.5,
      max_tokens=100,
      top_p = 1.0,
      frequency_penalty=0.0,
      stop=["\nUser: ", "\nChatbot: "]      
    )
    
    # extract the response text from the OpenAI API result
    bot_response = response.choices[0].text.strip()
    
    # add the user imput and bot response to the chat history
    chat_history.append(f"User: {user_message}\nChatbot: {bot_response}")
    
    # render the Chatbot template with the chat history
    return render_template('chatbot.html', 
                           user_message=user_message, 
                           bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)