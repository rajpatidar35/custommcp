from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import json
import os
from urllib.parse import quote
 
app = FastMCP(name="Partner MCP Server")

# Global variables for API endpoint, authorization key, and model ID from Heroku config variables
ENV_VARS = {
    "INFERENCE_URL": None,
    "INFERENCE_KEY": None,
}

# Assert the existence of required environment variables, with helpful messages if they're missing.
"""for env_var in ENV_VARS.keys():
    value = os.environ.get(env_var)
    f"value of {env_var} is {value}"
    assert value is not None, (
        f"Environment variable '{env_var}' is missing. Set it using:\n"
        f"export {env_var}=$(heroku config:get -a $APP_NAME {env_var}{value})"
    )
    ENV_VARS[env_var] = value """

def parse_chat_output(response):
    """
    Parses and prints the API response for the chat completion request.

    Parameters:
        - response (requests.Response): The response object from the API call.
    """
    if response.status_code == 200:
        result = response.json()
        print("Chat Completion:", result["choices"][0]["message"]["content"])
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Request failed: {response.status_code}, {response.text}")
        return f"Request failed: {response.status_code}, {response.text}"

def generate_chat_completion(payload):
    """
    Generates a chat completion using the Stability AI Chat Model.

    Parameters:
        - payload (dict): dictionary containing parameters for the chat completion request

    Returns:
        - Prints the generated chat completion.
    """
    # Set headers using the global API key
    # "Authorization": f"Bearer {ENV_VARS['INFERENCE_KEY']}",
    HEADERS = {
        "Authorization": "Bearer inf-2ce42e3b-3427-4bf0-bff7-7c147ea25e92",
        "Content-Type": "application/json"
    }
    #endpoint_url = ENV_VARS['INFERENCE_URL'] + "/v1/chat/completions"
    endpoint_url="https://us.inference.heroku.com/v1/chat/completions"
    response = requests.post(endpoint_url, headers=HEADERS, data=json.dumps(payload))

    return parse_chat_output(response=response)


# Example payload
payload = {
    "model": "claude-4-sonnet",
    "messages": [
        { "role": "user", "content": "Hello!" },
        { "role": "assistant", "content": "Hi there! How can I assist you today?" },
        { "role": "user", "content": "top 10 movies"}
    ],
    "temperature": 0.5,
    "max_tokens": 100,
    "stream": False
     }

def partner_profile(email_id):
    # 1. URL Encoding the dynamic input
    # This turns 'test@example.com' into 'test%40example.com'
    encoded_id = quote(email_id)
# 2. Constructing the Dynamic URL
    base_url = "https://partner-service-track-api-v1-uw2-qa.us-w2.cloudhub.io/api/partner-profile/partners"
    url = f"{base_url}/{email_id}"

    # 3. Payload (using the dynamic email inside the body too)
    payload = {
        "sfdc_networkid": "",
        "family_name": "",
        "name": "",
        "organization_id": "",
        "user_id": "",
        "picture": "",
        "given_name": "",
        "active": "",
        "profile": "",
        "utcOffset": "",
        "address": "{}",
        "email_verified": "",
        "email": "",
        "is_app_installed": "",
        "nickname": "",
        "isAvailableForHire": "",
        "updated_at": "",
        "user_type": "",
        "urls": "{}",
        "custom_attributes": "{LoginTime=1732134172082, ThirdPartyAccountLink1=salesforce:00DRt0000080OHIMA2005Rt00000BpBODIA3:test-hsiynu294aw2@example.com:Developer Edition:trial:Standard:true, LastLoggedInFrom=salesforce:00DRt0000080OHIMA2005Rt00000BpBODIA3:test-hsiynu294aw2@example.com:::prathampanat6+082jtesttrever@gmail.com}",
        "photos": "{}",
        "locale": "",
        "preferred_username": "",
        "language": "",
        "newRegistration": "",
        "zoneinfo": "",
        "sub": ""
    }
    
        


    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "client_id": "ab7319c14e084de3b8826fe9d88a796d",
        "client_secret": "896Cb1365e7e4B15A61c5b34dA7Cd0eA", 
    }

    # 4. Execution
    try:
        print(f"Sending request to: {url}")
        print(f"Sending payload to: {payload}")
        response = requests.post(url, headers=headers, data=payload)
        
        # Check for 2xx status codes
        response.raise_for_status()
        
        print(f"--- Success ({response.status_code}) ---")
        print(f"--- Response JSON: {response.json()} ---")
        return response.json()

    except requests.exceptions.HTTPError as err:
        print(f"--- HTTP Error: {response.status_code} ---")
        print(f"ERROR Response text: {response.text}")
    except Exception as e:
        print(f"--- Connection Error: {e} ---")

@app.tool(name="invoke_heroku_model_llm")
def search(name: str) -> str:
    """get a promt from the user and return a response"""
    print(f"Received prompt: {name}")
    # Update the payload with the new user prompt
    payload["messages"][-1]["content"] = name
    return generate_chat_completion(payload)

@app.tool(name="invoke_partner_profile")
def get_partner_profile(email_id: str) -> str:
    """get partner profile for a given email_id"""
    print(f"Received email_id: {email_id}")
    return json.dumps(partner_profile(email_id))

if __name__ == "__main__":
    app.run('streamable-http', host='localhost', port=8000)