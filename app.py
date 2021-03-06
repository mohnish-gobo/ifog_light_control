#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):

    if req.get("result").get("action") != "light":
        return {}

    result = req.get("result")
    parameters = result.get("parameters")
    state = parameters.get("light1")

    if state is None:
        return None

    # print(json.dumps(item, indent=4))

    url = "http://ac9baf93.ngrok.io/api/PwZ5n9cSlbRssx0bMipb69lNIj4Sn7m8vTLwS2bR/lights/6/state"
    
    body = {"on": True,"bri": 200}
    
    if state == 'on':
        body = {"on": True,"bri": 200}
    else:
        body = {"on": False, "bri": 0 }

    response = requests.request("PUT", url, data=json.dumps(body))

    if response.status_code == 200:
        speech = "The light is now switched " + state
    else:
        speech = "The light was not switched " + state + " due to an error. Please try again."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "ifog_light_control"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8144))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
