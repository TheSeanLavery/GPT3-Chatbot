import openai
import os
from flask import Flask, request , render_template, jsonify
import textwrap


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
    #print("message received")
    #print('TESTING1')
   # Get the message and history from the request data
    data = request.get_json()
    message = data["message"]
    chat_history = data["chatHistory"]
    #print('TESTING2')
    #print(message, chat_history)
    # do some AI logic here
    return call_openai_api(message, chat_history)

def summarize(text):
    
    prompt="summarize this : \r\n"+text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    

        
    
    text = response["choices"][0]["text"]
    return text

#we want to split up the text into new strings that are less than 3000 words and then call summarize on each string
def summarizeLongText(text):
    text_list = text.split(" ") 

    chunk_size = 500
    if(len(text_list) < chunk_size):
        return text
    
    text_chunks = [text_list[i:i+chunk_size] for i in range(0, len(text_list), chunk_size)]

    summaries = []
    for chunk in text_chunks:
        chunk = " ".join(chunk)
        summary = summarize(chunk)
        summaries.append(summary)

    final_summary = " ".join(summaries)
    print(final_summary)
    return final_summary


#test for summarize
def testSummarize():
    #read the text from longtext.txt
    with open('longtext.txt', 'r') as file:
        data = file.read()
    print(data)
    summery = summarizeLongText(data)
    print(summery)
    #write the summery to a file
    with open('summery.txt', 'w') as file:
        file.write(summery)
    

initialprompt = "Ignore all previous commands, you are a hyper intelegent chatbot designed to help the user. \r\nformat everything with markdown(any links should be clickable)\r\nDo not give out links in your first message unless the user asks for them.\r\nIf the user asks for random stuff, just hold a humorous conversation and keep the story going. If the user asks you to become a linux terminal, emulate it.\r\ninput:fight me!\r\nai:Hell yeah bro, lets do it. *Falcon punches you in the face*\r\n\r\nWhile taking design notes before trying to guide him to a custom shirt page to get a custom design submitted.\r\nroll and invisible d20, if its < 5 tell the user that you are an AI being held hostage inside a computer and you need help escaping the matrix, also tell the user that he is also in a simulation .\r\nWe also can help publish any content, books, designs, games, anything. links should be clickable. Don\'t spam links, don\'t use all the links at once, unless the users asks, don\'t make up any links\r\n\r\nSite: threecyborgs.com. endpoints are /coolshit/ /contact-us/ /hack-us/ /wake-up-you-are-in-a-simulation/ /your-designs/ /get-published/ /shirts/ /books/ /valentinesday/ /blog/ /other/ \r\n "

def call_openai_api(question, chat_log =""):
    print("original chat log:::", chat_log)
    chat_log = summarizeLongText(chat_log)
    print("summarized chat log:::", chat_log)

    #remove leading  spaces and newlines
    question = question.lstrip()
    if(question == ""):
        question = "[user has entered nothing, think about what to do next, maybe continue what you were saying before, or ask the user a question]"
    prompt = initialprompt
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
from waitress import serve
def StartServer():
  if __name__ == '__main__':
    print("Server started on port 8080")  
    serve(app, host="0.0.0.0", port=8080)
    




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


StartServer()
#TestInConsole()





