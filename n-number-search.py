import bs4, requests

url = 'http://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?nNumberTxt='
nnumber = ''

nnumber = input('Please enter tail number: ')

res = requests.get(url+nnumber)

try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

data = bs4.BeautifulSoup(res.text, "html.parser")

mfr = data.select('#content_lbMfrName')
model = data.select('#content_Label7')
owner = data.select('#content_lbOwnerName')

print('Owner: ' + owner[0].getText())
print('Manufacturer: ' + mfr[0].getText())
print('Model: ' + model[0].getText())