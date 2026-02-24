# Agentforce STDIO MCP Server

The **Agentforce STDIO MCP Server** allows seamless communication with **any Agentforce Agent** in **any Salesforce Org** using the **MCP (Multi-Client Protocol)**. It is compatible with MCP clients such as **GitHub Copilot, Claude Desktop, Gemini**, and more.

This server enables developers and users to programmatically interact with Salesforce Agentforce agents from external clients, facilitating cross-org automation and real-time agent communication.

---

## Prerequisites

Before setting up the server, ensure the following are installed and configured:

* **Python 3.10+**
* **Node.js and npm**
* An **MCP client** (e.g., GitHub Copilot, Claude Desktop, Gemini)
* A **Salesforce Org** with an active **Agentforce Agent**

---

## Server Configuration

### MCP Server Arguments

The server requires the following arguments to connect to Salesforce:

| Argument        | Description                    |
| --------------- | ------------------------------ |
| `username`      | Salesforce username            |
| `password`      | Salesforce user password       |
| `securityToken` | Salesforce user security token |

These arguments can be provided when starting the server or stored securely in environment variables.

---

### Server Inputs

The MCP server accepts the following inputs from connected MCP clients:

| Input       | Type | Description                             |
| ----------- | ---- | --------------------------------------- |
| `agentName` | str  | API Name of the target Agentforce Agent |
| `message`   | str  | Query or message to send to the agent   |

**Example Query:**

```json
{
  "agentName": "Agentforce_Service_Agent",
  "message": "Get the account targets of Acme Corporation."
}
```

The server will forward this request to the specified agent and return the response via the MCP client.

---

## NPM Package

The server is also available as an **npm package**:

[https://www.npmjs.com/package/@mohitharsh/agentforcemcp](https://www.npmjs.com/package/@mohitharsh/agentforcemcp)

This package provides:

* Pre-configured setups for multiple MCP clients (GitHub, Claude, Gemini, etc.)
* Example usage scripts and configuration files
* Instructions for integrating with different MCP clients

Follow the instructions on the npm page to set up and configure the server for your preferred client.

---
