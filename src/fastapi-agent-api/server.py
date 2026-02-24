from typing import Any
from fastapi import FastAPI, Header
import requests
import uuid
import pydantic
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def createToken(clientId: str, clientSecret: str, domainUrl: str) -> Any:

    url = f"https://{domainUrl}/services/oauth2/token"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)

    if(response.status_code != 200):
        print('Create Token Error: ',response.json())
        raise Exception(f"Failed to create token: {response.text}")

    return response.json()


def createSession(agentId:str,token:str,domainUrl:str)->Any:

    url = f"https://api.salesforce.com/einstein/ai-agent/v1/agents/{agentId}/sessions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "externalSessionKey": str(uuid.uuid4()),  # Generates a random UUID
        "instanceConfig": {
            "endpoint": f"https://{domainUrl}"
        },
        "streamingCapabilities": {
            "chunkTypes": ["Text"]
        },
        "bypassUser": True
    }

    response = requests.post(url, json=payload, headers=headers)

    if(response.status_code != 200):
        print('Create Session Error: ',response.json())
        raise Exception(f"Failed to create session: {response.text}")

    return response.json()

def deleteSession(session_id:str,token:str)->Any:

    url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}"

    headers = {
        "x-session-end-reason": "UserRequest",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)

    return response.json()

class RequestModel(pydantic.BaseModel):
    agentId: str
    message: str

@app.post("/invokeAgent")
def invokeAgent(req:RequestModel)->Any:

    clientId: str=os.getenv(f"{req.agentId}_CLIENT_ID")
    clientSecret: str=os.getenv(f"{req.agentId}_CLIENT_SECRET")
    agentId: str= req.agentId
    domainUrl: str=os.getenv(f"{req.agentId}_DOMAIN_URL")

    try:

        token_response = createToken(clientId, clientSecret, domainUrl)
        
        token = token_response['access_token']

        session = createSession(agentId, token, domainUrl)

        session_id = session['sessionId']

        url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{session_id}/messages"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "message": {
                "sequenceId": 1, 
                "type": "Text",
                "text": req.message
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        deleteSession(session_id, token)

        return response.json()["messages"]
    
    except Exception as e:

        print('Error invoking agent:', e)
        return f"Unable to connect to the agent: {str(e)}"