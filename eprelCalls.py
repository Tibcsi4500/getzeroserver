import urllib.request
import json
import requests
from cairosvg import svg2png
import io
import util

# Returns the json of an appliance from the eprel website
# Params:
# type - the type of the appliance e.g.: washingmachines2019
# modelid - the model identifier of the appliance
def lookup():
    data = util.getBody()
    print(str(data))
    try:
        typetext = data['type']
        modelid = data['modelid']
        url = "https://eprel.ec.europa.eu/api/products/" + typetext + "?_page=1&_limit=5&modelIdentifier=" + modelid
        result = json.loads(requests.get(url, headers={"x-api-key":"3PR31D3F4ULTU1K3Y2020", "X-Requested-With":"XMLHttpRequest"}).text)
        if(result['size'] > 0):
            return json.dumps(result['hits'][0])
        return "Model ID not found"
    except Exception as e:
        return "Something went wrong:" + str(e)

# Returns the label image of an appliance in bytearray form
# Params: 
# eprelid - the eprel registration number of the appliance
def getimage():
    data = util.getBody()

    try:
        eprelid = data['eprelid']
        url = 'https://eprel.ec.europa.eu/label/Label_' + str(eprelid) + '.svg'
        svg = requests.get(url).text
        imgstream = open("temp_img.png", "rb")
        svg2png(bytestring = svg, write_to = "temp_img.png")
        b = bytearray(imgstream.read())
        return bytearray(b)
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"