from flask import Flask, request
from twilio import twiml
import bs4, requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def sms():
  # Get the text in the message sent
    message_body = request.form['Body']
    
    # Create a Twilio response object to be able to send a reply back (as per         # Twilio docs)
    resp = twiml.Response()
    
    # Send the message body to the getReply message, where 
    # we will query the String and formulate a response
    replyText = get_tail_number(message_body)

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

  message = 'Owner: ' + owner[0].getText() + '\nManufacturer: ' + mfr[0].getText() + '\nModel: ' + model[0].getText()

  return message

if __name__ == '__main__':
  app.run()