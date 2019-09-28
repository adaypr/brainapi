#!flask/bin/python
from flask import Flask, jsonify, request, json
from detect_intent_texts import detect_intent_texts
import uuid
from twilio.rest import Client
from sendWhatsapp import send_WhatsApp
from salesforceIntegration import salesforce_Autentication, salesforce_LiveChatTranscript
from pymessenger.bot import Bot
import random

app = Flask(__name__)

# --------- Facebook Messenger ------
#Facebook Auth
ACCESS_TOKEN = 'EAAGcI6VZAygcBAOkMZAYafcgEbyqqvs9EuZB4kAfq2P6E90PcJ8ZAageO1TgfEEmSiZCPQA3ELWQILyUwXblGmcJwUT8KDm5IskHQmrpXa4Bv1srTsZBo3jUNLcRE7HNHtYCqv0gdCOtTftIb4FkmYIEGgCpoQsgsftKZAnzTylvxwi4YKKtz7jvDiw2sLWIkgZD'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)
@app.route("/facebookMessenger", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        #Before allowing people to message your bot, Facebook has implemented a verify token that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot    
        data = {}
        data['channel'] = "facebookMessenger"    
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to                    
                    data['from'] = message['sender']['id']
                    data['to'] = message['recipient']['id']
                    if message['message'].get('text'):
                        data['text'] = message['message'].get('text')
                        run_process(data)                                               
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#uses PyMessenger to send response to user
def send_facebookmessage(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


# --------- Twillio Whatsapp ---------
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)
    
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():    
    
    data = {}
    data['channel'] = "twillio"
    data['from'] = request.form['From']
    data['to'] = request.form['To']
    data['text'] = request.form['Body']    
    run_process(data)  
    return "ok", 201

def run_process(data):
    if (data['channel'] == "facebookMessenger"):

        #send to dialogflow
        output_dialogflow = detect_intent_texts("chatbotapiintegration-hvlbfm", data['from'], [data['text']], "en-US")
        #send to facebook messenger the response
        send_facebookmessage(data['from'], output_dialogflow['fulfillment_text'])
        channelColor = "green"
            
    elif (data['channel'] == "twillio"):
        #send to dialogflow
        output_dialogflow = detect_intent_texts("chatbotapiintegration-hvlbfm", data['from'], [data['text']], "en-US")
        
        #if end process, send the media file
        media_url = ''
        if (output_dialogflow['action'] == 'room.reservation.yes'): 
            media_url = 'http://fireworks.my/v4/wp-content/uploads/2017/08/Untitled6.jpg'
        #send to Whatsapp the response
        send_WhatsApp(data['from'], data['to'], output_dialogflow['fulfillment_text'],media_url)
        channelColor = "red"
        
    #Envia Pregunta y Respuesta a Salesforce
    text1 = '<p style="color:' + channelColor + ';" align="left">' + 'Lead(' + data['from'] + '): ' + data['text'] + '</p>'
    text2 = '<p style="color:blue;" align="right">' + 'Chatbot: ' + output_dialogflow['fulfillment_text'] + '</p>'
    authtoken = salesforce_Autentication()
    result = salesforce_LiveChatTranscript(text1 + text2, data['from'].replace('whatsapp:+34',''), authtoken)
    print('Resultado: ' + result)
    
    print(json.dumps(data))
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
