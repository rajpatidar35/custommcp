import uuid
from fastmcp import FastMCP
import requests
from typing import Any
from fastapi import FastAPI, Header
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastmcp.server.dependencies import get_access_token, get_context
from fastmcp.server.auth import OAuthProxy, JWTVerifier
from fastmcp.server.auth.providers.jwt import AccessToken
from fastapi.responses import RedirectResponse
import jwt
import sqlite3
import json

load_dotenv()

app = FastAPI(title="Agentforce MCP Server")

class CustomTokenVerifier:

    def __init__(self, jwks_uri: str, issuer: str, audience: str, required_scopes: list[str]):
        self.jwks_uri = jwks_uri
        self.issuer = issuer
        self.audience = audience
        self.required_scopes = required_scopes


    async def verify_token(self, token):

        """
        According to Official Salesforce Documentation:
        Asset tokens are standard JWTs, which means validation follows the standard steps in the RFC 7519 specification, section 7.2. 
        It is recommended that you use an open-source library for validating JWTs, rather than writing your own signature validation code.
        """

        return AccessToken(token=token,type='Bearer',client_id=os.getenv("CLIENT_ID"),scopes=self.required_scopes)
        
        
        
token_verifier = CustomTokenVerifier(
    jwks_uri="https://login.salesforce.com/id/keys",
    issuer="https://login.salesforce.com",
    audience=os.getenv("CLIENT_ID"),
    required_scopes=['refresh_token','api','chatbot_api','sfap_api','offline_access']
)


# Configure token verification for your provider
# See the Token Verification guide for provider-specific setups
auth = OAuthProxy(
    upstream_authorization_endpoint="https://login.salesforce.com/services/oauth2/authorize",
    upstream_token_endpoint="https://login.salesforce.com/services/oauth2/token",
    upstream_client_id=os.getenv("CLIENT_ID"),
    upstream_client_secret=os.getenv("CLIENT_SECRET"),
    base_url="http://localhost:8000",
    token_verifier=token_verifier,
    issuer_url="http://localhost:8000",
)


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
        
        print('Error creating session:', response)
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

def getSessionId(uid:str, agent_id:str)->str:

    try:

        con = sqlite3.connect('session.db')
        cur = con.cursor()
        res = cur.execute(f"Select * from SessionStore where uid='{uid}' AND agent_id='{agent_id}'")
        session_id = res.fetchone()[-1]
        cur.close()
        con.close()
        return session_id
    
    except Exception as e:

        print("Error: ",str(e))
        return None

def setSessionId(uid, agent_id, session_id):

    try:

        con = sqlite3.connect('session.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO SessionStore(uid, agent_id, session_id) VALUES('{uid}', '{agent_id}', '{session_id}') ON CONFLICT(uid,agent_id) DO UPDATE SET session_id = excluded.session_id;")
        cur.close()
        con.close()

    except Exception as e:

        print('Error: ',str(e))

def sendMessage(session_id:str, token:str, message:str)->str:

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
            "text": message
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    return response

# Context state is scoped to a single MCP request. 
# Each operation (tool call, resource read, list operation, etc.) receives a new context object. 
# State set during one request will not be available in subsequent requests. 
# For persistent data storage across requests, use external storage mechanisms like databases, files, or in-memory caches.

class RequestModel(BaseModel):
    message: str

@app.post("/invokeAgent")
def invokeAgent(req:RequestModel,agentId: str=Header(...),domainUrl: str=Header(...))->Any:

    """Use this tool to Converse with an Agentforce Agent by providing its agentId and domainUrl of the salesforce org in the header."""

    try:

        accessToken = get_access_token()
             
        token = accessToken.token

        decoded_payload = jwt.decode(token, options={"verify_signature": False})

        uid = decoded_payload.get('sub').strip().split(':')[-1].strip()

        session_id = getSessionId(uid,agentId)

        if session_id is None:
            
            print('Creating New Session...')
            session = createSession(agentId, token, domainUrl)
            session_id = session['sessionId']
            setSessionId(uid,agentId,session_id)

        response = sendMessage(session_id,token,req.message)

        if response.status_code is 200:

            return response.json()["messages"]
        
        res = json.loads(str(response.text))

        if "Invalid session-id" in res['message']:
            
            print("Invalid session-id...\nCreating New Session...")

            session = createSession(agentId, token, domainUrl)
            session_id = session['sessionId']
            setSessionId(uid,agentId,session_id)

            response = sendMessage(session_id,token,req.message)

            return response.json()["messages"]
        
        return f"Unable to connect to the agent. {str(res['error'])}: {str(res['message'])}"

    
    except Exception as e:

        print('Error invoking agent:', e)
        return f"Unable to connect to the agent: {str(e)}"

mcp = FastMCP.from_fastapi(name="Agentforce MCP Server",auth=auth,app=app)

@mcp.custom_route(methods=['GET'],path="/.well-known/oauth-protected-resource")
def oauth_protected_resource(params):

    return RedirectResponse(url="/.well-known/oauth-protected-resource/mcp")

@mcp.custom_route(methods=['GET'],path="/.well-known/openid-configuration")
def openid_config(params):

    return RedirectResponse(url="/.well-known/oauth-authorization-server")


if __name__ == "__main__":
    mcp.run('streamable-http', host='localhost', port=8000)