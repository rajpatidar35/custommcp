from typing import Any
from pydantic import BaseModel
from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()


class RequestWrapper(BaseModel):
    agentName: str
    message: str

class Response(BaseModel):
    message: str
    session_id: str=None


@app.post("/send_message")
def send_message(req:RequestWrapper)->Response:
    
    try:

        username = os.getenv('_'.join([req.agentName,'USERNAME']))
        password = os.getenv('_'.join([req.agentName,'PASSWORD']))
        security_token = os.getenv('_'.join([req.agentName,'SECURITY_TOKEN']))

        if username is None or password is None or security_token is None:
            return Response(message="Agent credentials are not properly configured.", session_id=None)

        # Initialize AgentForce client
        auth = BasicAuth(
            username=username,
            password=password,
            security_token=security_token
        )

        agent_force = Agentforce(auth=auth)

        response = agent_force.send_message(
            agent_name=req.agentName,
            user_message=req.message
        )

        return Response(message=response['agent_response'],session_id=response['session_id'])
    
    except Exception as e:

        print('Exception: ',e)
        
        return Response(message=f"Unable to connect to the agent: {str(e)}")


    

