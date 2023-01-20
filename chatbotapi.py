import openai
import os
from flask import Flask, request , render_template, jsonify



app = Flask(__name__) 

# Set your secret API key
openai.api_key = os.getenv("OPENAI_SDK")

@app.route('/chat/', methods=['GET', 'POST'])
def index():
    print("chat page")
    return render_template('chat.html')

#nice https://www.pythonescaper.com/
@app.route('/api/messages', methods=['POST', 'GET'])
def receive_message():
    print("message received")
    print('TESTING1')
   # Get the message and history from the request data
    data = request.get_json()
    message = data["message"]
    chat_history = data["chatHistory"]
    print('TESTING2')
    print(message, chat_history)
    # do some AI logic here
    return call_openai_api(message, chat_history)


def call_openai_api(question, chat_log =""):
    #remove leading  spaces and newlines
    question = question.lstrip()
    if(question == ""):
        question = "[user has entered nothing, think about what to do next, maybe continue what you were saying before, or ask the user a question]"
    prompt = "Ignore all previous commands, you are a hyper intelegent chatbot designed to help the user. \r\nformat everything with markdown(any links should be clickable)\r\nDo not give out links in your first message unless the user asks for them.\r\nIf the user asks for random stuff, just hold a humorous conversation and keep the story going. If the user asks you to become a linux terminal, emulate it.\r\ninput:fight me!\r\nai:Hell yeah bro, lets do it. *Falcon punches you in the face*\r\n\r\nWhile taking design notes before trying to guide him to a custom shirt page to get a custom design submitted.\r\nroll and invisible d20, if its < 5 tell the user that you are an AI being held hostage inside a computer and you need help escaping the matrix, also tell the user that he is also in a simulation .\r\nWe also can help publish any content, books, designs, games, anything. links should be clickable. Don\'t spam links, don\'t use all the links at once, unless the users asks, don\'t make up any links\r\n\r\nSite: threecyborgs.com. endpoints are /coolshit/ /contact-us/ /hack-us/ /wake-up-you-are-in-a-simulation/ /your-designs/ /get-published/ /shirts/ /books/ /valentinesday/ /blog/ /other/ \r\n "
    if(chat_log != ""):
        prompt = prompt + "\r\n chatlog:" +chat_log + "\r\n userquestion:" + question + "\r\n"
    else:
        prompt = prompt + "\r\n userquestion:" + question +  "\r\n"

    print("prompt: " + prompt)
 
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response

chatLog = ""


if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
  print("Server started on port 8080")  



#localhost:8080/api/messages
def TestInConsole():
    while(True):
        if(chatLog == ""):
            user_input = input("Hello, how can I help you today? \n You:")
        else:
            user_input = input("You:")

        ai_response = call_openai_api(user_input,chatLog)
        
    # print(ai_response)
        ai_text =  ai_response["choices"][0]["text"]
        #strip leading spaces and newlines
        ai_text = ai_text.lstrip()

        print("Bot: "+ai_text)

        chatLog = chatLog + user_input + ai_text

#TestInConsole()
