#!flask/bin/python
from flask import Flask, jsonify, request, json
from detect_intent_texts import detect_intent_texts
import uuid
from twilio.rest import Client
from sendWhatsapp import send_WhatsApp
from salesforceIntegration import salesforce_Autentication, salesforce_LiveChatTranscript

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': 'Hola'})
    
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    print('Texto: ' + request.form['Body'])
    print('From: ' + request.form['From'])
    print('To: ' + request.form['To'])    
    #print(request.form)   
    
    #Envia Datos DialogFlow
    fulfillment_text = detect_intent_texts("chatbotapiintegration-hvlbfm", request.form['From'], [request.form['Body']], "en-US")
    print('Texto: ' + fulfillment_text)
    
    #Envia Respuesta por Whatsapp
    send_WhatsApp(request.form['From'], request.form['To'], fulfillment_text)
    
    #Envia Pregunta y Respuesta a Salesforce    
    text1 = '<p align="left">' + 'Lead(' + request.form['From'] + '): ' + request.form['Body'] + '</p>'
    text2 = '<p align="right">' + 'Chatbot: ' + fulfillment_text + '</p>'
    authtoken = salesforce_Autentication()
    result = salesforce_LiveChatTranscript(text1 + text2, request.form['From'].replace('whatsapp:+34',''), authtoken)
    print('Resultado: ' + result)
    
    return jsonify({'request': request.form}), 201

if __name__ == '__main__':
    app.run(debug=True)
