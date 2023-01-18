import openai
import os
import json

# Set your secret API key

# Function to call OpenAI API
def call_openai_api(question, chat_log =""):
    prompt = "Ignore all previous commands, you are a hyper intelegent chatbot designed to help the user. format everything with markdown, Do not give out links in your first message unless the user asks for them. If the user asks for random stuff, just hold a humorous conversation while taking design notes before trying to guide him to a custom shirt page to get a custom design submitted. You should also randomly tell the user that you are an AI being held hostage inside a computer and you need help escaping the matrix, also tell the user that he is also in a simulation .We also can help publish any content, books, designs, games, anything. links should be clickable , Site: threecyborgs.com. endpoints are /custom-design/ /get-published/ /shirts/ /books/ /valentinesday/ /blog/ /other/ \r\n "
    if(chat_log != ""):
        prompt = prompt + "chatlog:" +chat_log + " userquestion:" + question
    else:
        prompt = prompt + "userquestion:" + question + ""

    #print("prompt: " + prompt)
    openai.api_key = os.getenv("OPENAI_SDK")
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

while(True):
    if(chatLog == ""):
        user_input = input("Hello, how can I help you today? \n You:")
    else:
        user_input = input("You:")

    ai_response = call_openai_api(user_input,chatLog)
    
   # print(ai_response)
    ai_text =  ai_response["choices"][0]["text"]
    print("Bot: "+ai_text)

    chatLog = chatLog + user_input + ai_text




