from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import json
import os
import mcp
 
app = FastMCP(name="Agentforce MCP Server")

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



@app.tool(name="invoke_heroku_model")
def search(name: str) -> str:
    """get a promt from the user and return a response"""
    print(f"Received prompt: {name}")
    # Update the payload with the new user prompt
    payload["messages"][-1]["content"] = name
    return generate_chat_completion(payload)



if __name__ == "__main__":
    app.run('streamable-http', host='localhost', port=8000)