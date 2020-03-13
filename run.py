import db
import os
import sys

from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for

# setup our constants
BABY_NICKNAME = os.environ.get('BABY_NICKNAME', False)
BORN_PHRASE = os.environ.get('BORN_PHRASE', False)
DATABASE_URL = os.environ.get('DATABASE_URL', False)
NUMBER = os.environ.get('NUMBER', False)
SID = os.environ.get('SID', False)
TOKEN = os.environ.get('TOKEN', False)
URL = os.environ.get('URL', False)

# ensure the required constants are defined
if (False in (BABY_NICKNAME, BORN_PHRASE, DATABASE_URL, NUMBER, SID, TOKEN, URL)):
  print("One or more environment variables are not set. Please navigate to you Heroku app's Settings page and add your Config Vars.")
  sys.exit()

# define out optional constants
TWILIO_VOICE = os.environ.get('TWILIO_VOICE', 'female')
PORT = os.environ.get('PORT', 8080)

# init the flask app and database
app = Flask(__name__)
db.init()


@app.route('/')
def index():
  return 'invalid request'


# handle the case where someone calls instead of texts
@app.route('/api/call', methods=['GET'])
def call():
  resp = VoiceResponse()
  resp.say("Thank you for calling the {} Labor Notifier. Unfortunately, we only support text messaging. Please text "\
    "this number with the word REGISTER to sign up for a notification when {} is born!".format(BABY_NICKNAME, BABY_NICKNAME))
  return str(resp)

# entry point for SMS
@app.route('/api/sms', methods=['GET', 'POST'])
def register():
  resp = MessagingResponse()
  number = request.values.get('From')
  if not db.number_exists(number):
    resp.redirect(url=url_for('welcome'))
    return str(resp)
  else:
    resp.redirect(url=url_for('handle_text'))
    return str(resp)


@app.route('/api/welcome', methods=['GET', 'POST'])
def welcome():
  resp = MessagingResponse()
  number = request.values.get('From')
  db.store_number(number)
  resp.message("Welcome to the {} Labor Notifier! You will receive a notification once the baby is born. If you would"\
    " like to remove yourself from the notification list, please text REMOVE at any time.".format(BABY_NICKNAME))
  return str(resp)


@app.route('/api/handle_text', methods=['GET', 'POST'])
def handle_text():
  resp = MessagingResponse()
  body = request.values['Body']

  born = db.get_born_message()
  if born:
    resp.message(born[0])
    return str(resp)
  elif request.values['Body'].startswith(BORN_PHRASE):
    resp.redirect(url=url_for('notify'))
    return str(resp)
  elif "remove" in body.lower():
    number = request.values.get('From')
    db.remove_number(number)
    resp.message("You have been removed from the {} Notifier.".format(BABY_NICKNAME))
    return str(resp)
  else:
    resp.message("{} is not born yet. You'll be notified when that changes.".format(BABY_NICKNAME))
    return str(resp)


@app.route('/notify', methods=['GET', 'POST'])
def notify():
  client = Client(SID, TOKEN)
  message = request.values['Body'].replace(BORN_PHRASE, '', 1)

  # store the message as an autoreply for follow-ups
  db.store_born_message(message)

  # notify each number
  numbers = db.get_all_numbers()
  for number in numbers:
    params = {'from_': NUMBER, 'to': number, 'body': message}
    client.messages.create(**params)

  # notify the number that triggered the BORN_PHRASE
  resp = MessagingResponse()
  resp.message('Finished notifying all {} numbers'.format(len(numbers)))
  return str(resp)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT)
