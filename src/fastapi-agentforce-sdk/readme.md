# Custom FastAPI Server for Cross-Org Agentforce Agent-to-Agent Communication

This documentation provides instructions for setting up a **Custom FastAPI Server** to facilitate **cross-org Agentforce agent-to-agent communication** using the **Agentforce Python SDK**. The server allows Salesforce agents to securely communicate across Salesforce orgs without data duplication, leveraging API-driven interactions.

---

## Prerequisites

Before setting up the server, ensure the following are available:

1. **Salesforce Org** with Agentforce enabled.
2. **Active Agentforce Agent** in the org.
3. **Salesforce User** with permissions to invoke the agent and required access rights for integration.
4. **Python 3.10+ environment** for running the FastAPI server.
5. **Agentforce Python SDK** installed (`pip install agentforce-sdk` or equivalent).

---

## Getting Started

### Environment Variables

The server requires the following environment variables for authentication and secure communication:

| Variable         | Description               |
| ---------------- | ------------------------- |
| `UNAME`          | Salesforce username       |
| `PASSWORD`       | Salesforce password       |
| `SECURITY_TOKEN` | Salesforce security token |

> **Tip:** Store credentials securely using environment management tools or secret managers.

---

### Server Inputs & Outputs

#### Inputs

| Parameter   | Type | Description                  |
| ----------- | ---- | ---------------------------- |
| `agentName` | str  | API name of the target agent |
| `message`   | str  | Message content to send      |

#### Outputs

| Parameter    | Type | Description                           |
| ------------ | ---- | ------------------------------------- |
| `message`    | str  | Response message from the agent       |
| `session_id` | str  | Unique session identifier for request |

---

## Apex Integration

### Invocable Apex Method

Create an **Invocable Apex Method** to send requests to the FastAPI server.

```java

public class InvokeAgent 
{
    public class Request
    {
        @InvocableVariable
		public String agentName;
        @InvocableVariable
        public String message;
    }
    
    public class Response
    {
        @InvocableVariable
        public String message;
        @InvocableVariable
        public String session_id;
    }
    
	@InvocableMethod
    public static List<Response> invokeAgent(List<Request> requests)
    {
        
        List<Response> responses = new List<Response>();
        
        for(Request req: requests)
        {
            Http http = new Http();
            HttpRequest httpreq = new HttpRequest();
            httpreq.setEndpoint('<your-server-endpoint-url>/send_message');
            httpreq.setHeader('Content-Type', 'application/json');
            httpreq.setTimeout(120000);
            httpreq.setMethod('POST');
            httpreq.setBody(JSON.serialize(new Map<String,Object>{
                    'agentName' => req.agentName,
                    'message' => req.message
            }));
            
            HttpResponse res = http.send(httpreq);
            
            if(res.getStatusCode() == 200)
            {
                Map<String,Object> jsonResponse = (Map<String, Object>)JSON.deserializeUntyped(res.getBody());
                Response result = new Response();
                result.message = (String)jsonResponse.get('message');
                result.session_id = (String)jsonResponse.get('session_id');
                responses.add(result);
            }
        }
        
        return responses;
        
    }
}

```

---

### Remote Site Settings

* Add the FastAPI server URL to **Salesforce Remote Site Settings** to allow outbound HTTP requests.
* This ensures secure and authorized communication between Apex and the external FastAPI server.

---

## Agentforce Action Setup

1. Create an **Apex Action** that invokes the custom Apex method.
2. Attach the action to an **Agentforce Agent** to enable communication with agents in other orgs.
3. Once configured, agents can forward user queries across orgs seamlessly.

---

## Best Practices

* **Use environment variables** or secret managers for credentials.
* **Validate inputs** to prevent injection or malformed requests.
* **Monitor logs** for anomalies or failed requests.
* **Enable rate limiting** if multiple orgs communicate simultaneously.
* **Keep dependencies updated** to avoid security vulnerabilities.

---