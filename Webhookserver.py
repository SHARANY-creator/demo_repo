from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

STATUSPAGE_API_KEY = 'efedb6ec0a17468982ac3ac07b7ff431'
PAGE_ID = 'gssrvqwbzz91'
COMPONENT_ID = 'vhrm0ww1rkwn'

@app.route('/opsgenie-webhook', methods=['POST'])
def opsgenie_webhook():
    data = request.json
    print("Received payload:", data)

    message = data.get('message', 'Opsgenie Alert')
    description = data.get('description', 'Alert from Opsgenie to StatusPage')

    payload = {
        "incident": {
            "name": message,
            "status": "investigating",
            "impact_override": "major",
            "components": {
                COMPONENT_ID: "major_outage"
            },
            "body": description
        }
    }

    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://api.statuspage.io/v1/pages/{PAGE_ID}/incidents.json",
        json=payload,
        headers=headers
    )

    return jsonify({"status": response.status_code, "response": response.text})

if __name__ == '__main__':
    app.run(port=5000)
