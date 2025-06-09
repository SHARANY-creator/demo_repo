from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration (replace with your actual values or use environment variables)
STATUSPAGE_API_KEY = os.environ.get('STATUSPAGE_API_KEY', 'efedb6ec0a17468982ac3ac07b7ff431')
PAGE_ID = os.environ.get('STATUSPAGE_PAGE_ID', 'gssrvqwbzz91')
COMPONENT_ID = os.environ.get('STATUSPAGE_COMPONENT_ID', 'vhrm0ww1rkwn')

STATUSPAGE_API_BASE = f"https://api.statuspage.io/v1/pages/gssrvqwbzz91"

# For demo: Store the last incident ID (for production, use persistent storage and map ProblemID to incident ID)
incident_map = {}

def update_component_status(status):
    url = f"{STATUSPAGE_API_BASE}/components/{COMPONENT_ID}"
    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "component": {
            "status": status
        }
    }
    response = requests.patch(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def create_incident(problem_id, title, details):
    url = f"{STATUSPAGE_API_BASE}/incidents"
    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "incident": {
            "name": f"Dynatrace Alert: {title}",
            "status": "investigating",
            "impact_override": "major",
            "components": {
                COMPONENT_ID: "major_outage"
            },
            "body": details
        }
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    incident_id = response.json()["id"]
    incident_map[problem_id] = incident_id
    return incident_id

def resolve_incident(problem_id):
    incident_id = incident_map.get(problem_id)
    if not incident_id:
        print(f"No incident found for ProblemID {problem_id}")
        return
    url = f"{STATUSPAGE_API_BASE}/incidents/{incident_id}"
    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "incident": {
            "status": "resolved",
            "body": "Dynatrace reports the issue is resolved and the service is operational again."
        }
    }
    response = requests.patch(url, json=data, headers=headers)
    response.raise_for_status()
    # Optionally remove from map
    del incident_map[problem_id]
    return response.json()

@app.route('/', methods=['POST'])
def dynatrace_webhook():
    payload = request.get_json()
    print("Received Dynatrace Problem Notification:")
    print(payload)

    state = payload.get('State')
    problem_id = payload.get('ProblemID')
    title = payload.get('ProblemTitle', 'No Title')
    details = payload.get('ProblemDetailsText', 'No Details')

    if state == 'OPEN':
        # 1. Update component status to major_outage
        update_component_status('major_outage')
        # 2. Create incident
        incident_id = create_incident(problem_id, title, details)
        print(f"Created incident {incident_id} for problem {problem_id}")
    elif state == 'RESOLVED':
        # 1. Update component status to operational
        update_component_status('operational')
        # 2. Resolve incident
        resolve_incident(problem_id)
        print(f"Resolved incident for problem {problem_id}")
    else:
        print(f"Unknown state: {state}")

    return jsonify({"status": "processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
