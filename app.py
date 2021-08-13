from flask import Flask, render_template, request, jsonify
import aiml
import os
from googletrans import Translator
#import speech
import find
import sys
######

import speech_recognition as sr 
import pyttsx3 

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to 
# speech 
def SpeakText(command): 
	
	# Initialize the engine 
	engine = pyttsx3.init() 
	engine.say(command) 
	engine.runAndWait() 
	
	
# Loop infinitely for user to 
# speak 

def hear():
        while(1):	 
                print('BOT : stage1')
                # Exception handling to handle 
                # exceptions at the runtime 
                try: 
                        
                        # use the microphone as source for input. 
                        with sr.Microphone() as source2: 
                                print('BOT : listerning')
                                # wait for a second to let the recognizer 
                                # adjust the energy threshold based on 
                                # the surrounding noise level 
                                r.adjust_for_ambient_noise(source2, duration=0.2) 
                                
                                #listens for the user's input 
                                audio2 = r.listen(source2) 
                                
                                # Using ggogle to recognize audio
                                print('BOT : Processing')
                                MyText = r.recognize_google(audio2) 
                                MyText = MyText.lower()
                                if MyText in ['voice deactivate','deactivate voice','activate text','use text']:                                  
                                  return 'voice deactivate'
                                print(MyText)
                                bot_response = kernel.respond(MyText)
                                if voiceFlag == 0:
                                  SpeakText(bot_response)
                                  

                                #return MyText 
                                #SpeakText(MyText) 
                                
                except sr.RequestError as e: 
                        print("Could not request results; {0}".format(e)) 
                        
                except sr.UnknownValueError: 
                        print("unknown error occured") 

######
kernel = aiml.Kernel()
penerjemah = Translator()
def load_kern(forcereload):
	if os.path.isfile("bot_brain.brn") and not forcereload:
		kernel.bootstrap(brainFile="bot_brain.brn")
	else:
		kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
		kernel.saveBrain("bot_brain.brn")

import mysql.connector
try:
	mydb=mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='minor_project',
		)
except mysql.connector.errors.ProgrammingError as e:
	print(e)
except mysql.connector.errors.InterfaceError as e:
	print(e)
mycursor=mydb.cursor()


app = Flask(__name__)
@app.route("/")
def hello():
	load_kern(False)
	return render_template('chat.html')

@app.route("/ask", methods=['POST','GET'])
def ask():
	mycursor.execute('select lang from language where sno=1;')
	v=mycursor.fetchall()
	lang=str()
	'''mycursor.execute('select type from language where sno=1;')
	w=mycursor.fetchall()
	typ=int()'''
	for i in v:
                lang=i
                lang=lang[0]
                '''for j in w:
                        typ=j
                        voiceFlag=typ[0]'''
	voiceFlag=1
	if voiceFlag == 0:
		message=hear()
	else:
		message = str(penerjemah.translate(request.form['chatmessage'], dest='en').text)
		message=find.cor(message)#spellcorrection
		print(message)
	if message == "save":
		kernel.saveBrain("bot_brain.brn")
		return jsonify({"status":"ok", "answer":"Brain Saved"})
	elif message == "reload":
		load_kern(True)
		return jsonify({"status":"ok", "answer":"Brain Reloaded"})
	elif message == "quit":
                return jsonify({"status":"ok", "answer":"exit Thank You"})
	elif message in ['voice activate','activate voice','activate speech','use voice','use speech']:
                x=int(0)
                n=1
                sql="update language set type = %s where sno = %s; "
                val=(x,n)
                mycursor.execute(sql,val)
                mydb.commit()
                return jsonify({"status":"ok", "answer":"voice activated"})
	elif message in ['voice deactivate','deactivate voice','activate text','use text']:
		n=1
		x=int(1)
		sql="update language set type = %s where sno = %s; "
		val=(x,n)
		mycursor.execute(sql,val)
		mydb.commit()
		return jsonify({"status":"ok", "answer":"voice deactivated"})
	elif message in ['english','tamil','hindi','telugu','french','kannada']:
                z={
                        'tamil':'ta',
                        'english':'en',
                        'hindi':'hi',
                        'telugu':'te',
                        'french':'fr',
                        'kannada':'kn'
                }
                x=z[message]
                n=1
                sql="update language set lang = %s where sno = %s; "
                val=(x,n)
                mycursor.execute(sql,val)
                mydb.commit()
                return jsonify({"status":"ok", "answer":"translated to {0}".format(message)})
	# kernel now ready for use
	else:
		bot_response = kernel.respond(message)
		bot_response = penerjemah.translate(bot_response, dest=lang).text
		if voiceFlag == 0:
			SpeakText(bot_response)
		return jsonify({'status':'OK','answer':bot_response})
        
if __name__ == "__main__":
    app.run(debug=True)
