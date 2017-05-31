from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import bs4, requests
import wikipedia

app = Flask(__name__)

@app.route('/', methods=['POST'])
def sms():
  # Get the text in the message sent
    message_body = request.form['Body']
    
    #parse message body

    if message_body.upper[0] == 'N':
      replyText = get_tail_number(message_body)

    elif message_body.upper[:3] == 'WIKI':
      replyText = get_wiki(message_body)

    # Send the message body to the getReply message, where 
    # # we will query the String and formulate a response

  # Create a Twilio response object to be able to send a reply back (as per         # Twilio docs)
    resp = MessagingResponse()
	# Text back our response!
    resp.message(replyText)
    return str(resp)

def get_tail_number(nnumber):

  url = 'http://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?nNumberTxt='  #FAA registry website
  #nnumber = ''  #variable to hold n-number

  #nnumber = input('Please enter tail number: ') #get input

  res = requests.get(url+nnumber)

  try:
    res.raise_for_status()
  except Exception as exc:
    message = 'There was a problem.'
    return message
    
  data = bs4.BeautifulSoup(res.text, "html.parser")

  mfr = data.select('#content_lbMfrName')
  model = data.select('#content_Label7')
  owner = data.select('#content_lbOwnerName')

  message = '\nOwner: ' + owner[0].getText() + '\nManufacturer: ' + mfr[0].getText() + '\nModel: ' + model[0].getText()

  return message

def get_wiki(query):

  search_text = query[5:]

  try:
    search_result = wikipedia.summary(search_text)
  except wikipedia.exceptions.DisambiguationError as e:
    return e.options

  message = wikipedia.summary(search_text)

  if len(message) > 1600:
    a = len(message)
    for parsed in a(1600):
      return parsed
  
  else:
    return message

if __name__ == '__main__':
  app.run()