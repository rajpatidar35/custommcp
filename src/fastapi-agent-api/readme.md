# Cross-Org Agentforce Communication Server

**Custom FastAPI Server for Salesforce Agent-to-Agent Communication**

This project provides a **Custom FastAPI Server** to enable **secure, cross-org communication between Salesforce Agentforce Agents**.
It facilitates **Agent-to-Agent message exchange** via Salesforce’s **Agent API**, allowing real-time AI-driven collaboration between multiple business domains.

---


## Prerequisites

Before setting up the server, ensure the following:

* ✅ A **Salesforce Org** with **Agentforce enabled**.
* ✅ An **Active Agentforce Agent** configured in the org.
* ✅ **Python 3.9+**.
* ✅ **Salesforce Connected App** (for OAuth credentials).
* ✅ Environment variables configured for each Agent.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-org>/agentforce-crossorg-server.git
cd agentforce-crossorg-server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Each Agent participating in the communication must have its own set of credentials configured via environment variables.

| Variable                  | Description                                   | Example                          |
| ------------------------- | --------------------------------------------- | -------------------------------- |
| `{agentId}_CLIENT_ID`     | Consumer Key from Salesforce Connected App    | `AGENT_A_CLIENT_ID`              |
| `{agentId}_CLIENT_SECRET` | Consumer Secret from Salesforce Connected App | `AGENT_A_CLIENT_SECRET`          |
| `{agentId}_DOMAIN_URL`    | Salesforce Org Domain URL                     | `https://orgA.my.salesforce.com` |

These can be configured in your shell or `.env` file:

```bash
AGENT_A_CLIENT_ID="xxxxxxxxxxxxx"
AGENT_A_CLIENT_SECRET="xxxxxxxxxxxxx"
AGENT_A_DOMAIN_URL="https://orgA.my.salesforce.com"
```

---

### Server Inputs

When invoking the server, send a JSON body containing:

| Field     | Type  | Description                                      |
| --------- | ----- | ------------------------------------------------ |
| `agentId` | `str` | Identifier of the calling Agent.                 |
| `message` | `str` | Message or query to forward to the target Agent. |

**Example Request:**

```json
{
  "agentId": "Agent_A",
  "message": "Fetch lead data from Org B"
}
```

---

## Salesforce Setup Guide

Follow these steps to configure Salesforce for communication:

1. **Create a Connected App**

   * Navigate to **Setup → App Manager → New Connected App**.
   * Enable **OAuth Settings** and provide callback URL (e.g., `https://localhost/callback`).
   * Select **OAuth Scopes**:

    - `Manage user data via APIs (api)`
    - `Full access (full)`
    - `Perform requests at any time (refresh_token, offline_access)`
    - `Access chatbot services (chatbot_api)`
    - `Access the Salesforce API Platform (sfap_api)`

2. **Copy Keys**

   * Note the **Consumer Key** and **Consumer Secret**; use them in the environment variables.

3. **Add the AI Agent**

   * Add the **Agentforce Agent** you wish to invoke to this Connected App.

---

## Apex Integration

You’ll need to integrate the FastAPI server with Salesforce via Apex.

### Steps:

1. **Create Invocable Apex Method**
   Define an invocable method to send HTTP requests to the FastAPI server.

```java

public with sharing class CallFastAPIServer {

    // Input structure for Invocable Method
    public class Request {
        @InvocableVariable(required=true)
        public String agentId;

        @InvocableVariable(required=true)
        public String message;
    }

    // Output structure (optional)
    public class Response {
        @InvocableVariable
        public String status;

        @InvocableVariable
        public String responseBody;
    }

    @InvocableMethod(label='Call FastAPI Server' description='Sends a POST request to a FastAPI server with agentId and message')
    public static List<Response> callFastAPI(List<Request> requests) {
        List<Response> responses = new List<Response>();

        for (Request req : requests) {
            Response res = new Response();

            try {
                Http http = new Http();
                HttpRequest httpReq = new HttpRequest();

                // 👇 Replace this with your FastAPI endpoint URL
                String endpoint = '<your-fastapi-server-enpoint-url>/invokeAgent';
                httpReq.setEndpoint(endpoint);
                httpReq.setMethod('POST');
                httpReq.setHeader('Content-Type', 'application/json');

                // Construct JSON payload
                Map<String, Object> payload = new Map<String, Object>{
                    'agentId' => req.agentId,
                    'message' => req.message
                };

                httpReq.setBody(JSON.serialize(payload));

                // Send HTTP request
                HttpResponse httpRes = http.send(httpReq);

                res.status = httpRes.getStatus();
                res.responseBody = httpRes.getBody();

            } catch (Exception e) {
                res.status = 'Error';
                res.responseBody = e.getMessage();
            }

            responses.add(res);
        }

        return responses;
    }
}


```

2. **Add Remote Site Setting**

   * Go to **Setup → Security → Remote Site Settings**
   * Add your FastAPI server URL, e.g.:

     ```
     https://agentforce-bridge.example.com
     ```

---

## Agentforce Action Setup

1. **Create an Apex Action**

   * Create an **Apex Action** that invokes the invocable method created above.

2. **Attach to Agentforce Agent**

   * Navigate to your **Agentforce Agent Settings**.
   * Add the Apex Action to the desired Agent.
   * Configure it to forward messages to another Agentforce Agent using the FastAPI server.

---