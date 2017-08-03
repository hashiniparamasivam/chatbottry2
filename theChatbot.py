
# coding: utf-8

# In[3]:

#import packages
from __future__ import print_function
import os
import pandas as p
import dateutil
import itertools
import sys 
import imp
import threading
import subprocess
import uuid
import json
import flask
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request,send_from_directory,redirect
from flask import request
from flask import make_response
from werkzeug import secure_filename
import speech_recognition as sr
from fuzzywuzzy import fuzz
from random import randint

from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError


# In[4]:

# Creating flask app
app = Flask(__name__)

# Folder for storing uploaded files
app.config['UPLOAD_FOLDER'] = 'C:\\Hashini\\chatbot\\jupytercodes\\uploads'

# In[5]:

@app.route('/')
def index():
	return render_template('index.html')


# In[6]:

@app.route('/record',methods=['POST'])
def record():
	return render_template('record2.html')


# In[ ]:
@app.route('/upload',methods=['POST'])
def upload():
	if request.method == 'POST':
		submitted_file = request.files['file']
		filename = "uploadedFile.csv"
		submitted_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		path = 'C:\\Hashini\\chatbot\\jupytercodes\\uploads\\'
		# Reading the file into a DataFrame
		df = p.DataFrame.from_csv(path+filename)
		df.reset_index(inplace=True)
		summary_df = df.head(10)
		columns_df = p.DataFrame(df.columns)
		columns_df.columns = ['Column']
		
		datatypes_df = p.DataFrame(df.dtypes)
		datatypes_df.reset_index(inplace=True,drop=True)
		columns_df = p.concat([columns_df,datatypes_df],axis=1)
		columns_df.columns = ['Column','Data Type']
		##print columns_df
		
		return render_template('index.html',tables=[summary_df.to_html(index=False),columns_df.to_html(	index=False)],titles=['Summary','Columns'],summary_flag=True)



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    print("You have webhooked")

    #res = processRequest(req)

    #res = json.dumps(res, indent=4)
    #print(res)
    
    res="here is the respone"
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    return json.dumps(req, indent=4)
	
    

def makeWebhookResult(data,req):
    query = data.get('query')
    #if query is None:
        #return {}

    result = query.get('results')
    #if result is None:
        #return {}

    channel = result.get('channel')
    #if channel is None:
        #return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    result = req.get("result")
    parameters = result.get("parameters")
    condition=parameters.get("Condition")
    
    winddetail = channel.get('wind')
    atmosphere = channel.get('atmosphere')
    sun = channel.get('astronomy')
    #if (location is None) or (item is None) or (units is None):
        #return {}

    cond = item.get('condition')


    # print(json.dumps(item, indent=4))
    if req.get("result").get("action") == "yahooWeatherForecast":
            speech = "The weather in " + location.get('city') + ": " + cond.get('text') + \
                     ", the temperature is " + cond.get('temp') + " " + units.get('temperature')
    if req.get("result").get("action") == "yahooWeatherCondition":
            if parameters.get("Condition") == "windspeed":
                     speech = "The windspeed is " + winddetail.get('speed') + " " + units.get('speed') +" in " + location.get('city')
            if condition == "direction":
                     speech = "The direction is " + winddetail.get('direction') + " " +" in " + location.get('city')
            if condition == "humidity":
                     speech = "The humidity is " + atmosphere.get('humidity')  +"% " + " in " + location.get('city')
            if condition == "pressure":
                     speech = "The pressure is " + atmosphere.get('pressure') +" in " + location.get('city')
            if condition == "sunrise":  
                     speech = "The Sunrise is at " + sun.get('sunrise') +" in " + location.get('city')
            if condition == "sunset":
                     speech = "The Sunset is at " + sun.get('sunset') +" in " + location.get('city')
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

    
# Speech recognition route - records the audio, converts it to text and displays the resultant text
@app.route('/output',methods=['POST'])
# Function to Record Audio
def output():
	if request.method == 'POST':
		voice_input = request.form['text'] 
		#print voice_input
		
		if voice_input == "":
			r = sr.Recognizer()
			with sr.Microphone() as source:
				r.adjust_for_ambient_noise(source, duration = 1)
				print("Say something!")
				audio = r.listen(source,timeout=4)
			
			# Speech recognition using Google Speech Recognition
			try:
				print("You said: " + r.recognize_google(audio,language='en-us'))
				voice_input = r.recognize_google(audio,language='en-us')
				#voice_input='category by city and state filter out web and facebook'
			except sr.UnknownValueError:
				voice_input = "Google Speech Recognition could not understand audio"
				#print voice_input
			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))
				voice_input = "Could not request results from Google Speech Recognition service"


                        # Path for Uploaded Files
        path = 'C:\\Hashini\\chatbot\\jupytercodes\\uploads\\'
        # Reading the file into a DataFrame
        Source = p.DataFrame.from_csv(path+'uploadedFile.csv')
        Source = Source.reset_index()          

        #analysis_num=input("What type of analysis do you wish to perform? Please enter only the number : \n 1.Component Innovation Analysis\n 2.Drivers of Sentiment\n 3.Triggers of Purchase\n 4.Innovation Analysis\n 5.Drivers of Purchase\n ")
                # print(analysis_num)
        if analysis_num==1:
            analysis_type="Component Innovation Analysis"     
        elif analysis_num==2: 
            analysis_type="Drivers of Sentiment"     
        elif analysis_num==3:     
            analysis_type="Triggers of Purchase"     
        elif analysis_num==4:     
            analysis_type="Innovation Analysis"     
        elif analysis_num==5:     
            analysis_type="Drivers of Purchase"     
                # print(analysis_type)


        #business_unit_num=input("At what level do you wish to perform analysis? Please enter only the number : \n 1.Product Group\n 2.Product Family\n 3.Platform\n 4.Commercial Segment\n 5.Product ID \n choice:\n ")
        print(business_unit_num)
        if business_unit_num==1:
            business_unit_type="ProductGroup"     
        elif business_unit_num==2: 
            business_unit_type="ProductFamily"     
        elif business_unit_num==3:     
            business_unit_type="Platform"     
        elif business_unit_num==4:     
            business_unit_type="COMMERCIAL_SEGMENT"     
        elif business_unit_num==5:     
            business_unit_type="ProductID"     
        print(business_unit_type)
	return render_template('record2.html',speech_input = voice_input,question="What type of analysis do you wish to perform? Please enter only the number : \n 1.Component Innovation Analysis\n 2.Drivers of Sentiment\n 3.Triggers of Purchase\n 4.Innovation Analysis\n 5.Drivers of Purchase\n ")
# In[ ]:

if __name__ == '__main__':
    app.run(
                debug=True
    )

