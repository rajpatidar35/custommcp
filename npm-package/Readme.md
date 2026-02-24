# Agentforce MCP (STDIO Server)

**Agentforce MCP** is an **MCP (Model Context Protocol)** server that enables any MCP-compatible client (like **GitHub Copilot** or **Claude Desktop**) to connect directly with **Agentforce Agents** hosted on Salesforce.

This package bridges your local MCP client with the Salesforce Agentforce platform via **STDIO**. Once connected, your MCP client can query or perform actions through your configured Salesforce Agent — all in real time.

---

## 🚀 Features

* 🔌 **Seamless STDIO integration** with MCP clients
* 🔐 **Salesforce authentication** via username, password, and security token
* ⚙️ **Agent-based invocation** for flexible interaction
* 🧩 **Lightweight, CLI-ready NPM package** (no local setup required)

---

## 🧠 Prerequisites

Before using this package, ensure you have:

* A valid **Salesforce account**
* An **active Agentforce Agent** in your org
* Your **Salesforce credentials**:

  * `username`
  * `password`
  * `securityToken`
  * `agentName`
* > Python, Node.js and npm installed

---

### 🧩 GitHub Copilot MCP Configuration

Add the following entry to your **`mcp.json`**:

```json
{
  "servers": {
    "AgentforceStdio": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@mohitharsh/agentforcemcp",
        "--username",
        "<your-username>",
        "--password",
        "<your-password>",
        "--securityToken",
        "<your-security-token>",
        "--agentName",
        "<agent-api-name>"
      ]
    }
  },
  "inputs": []
}
```

---

### 💬 Claude Desktop MCP Configuration

Add the following entry to your **`mcp.json`** (usually located in the Claude app data directory):

```json
{
  "mcpServers": {
    "AgentforceStdio": {
      "description": "Connect to Agentforce Agent",
      "command": "npx",
      "args": [
        "-y",
        "@mohitharsh/agentforcemcp",
        "--username",
        "<your-username>",
        "--password",
        "<your-password>",
        "--securityToken",
        "<your-security-token>",
        "--agentName",
        "<agent-api-name>"
      ]
    }
  }
}
```

---

## 🧭 Command-Line Arguments

| Argument          | Description                                    | Required | Example                     |
| ----------------- | ---------------------------------------------- | -------- | --------------------------- |
| `--username`      | Salesforce username for authentication         | ✅        | `--username john@doe.com`   |
| `--password`      | Salesforce password for authentication         | ✅        | `--password myPass123`      |
| `--securityToken` | Salesforce security token for authentication   | ✅        | `--securityToken aBc123XyZ` |
| `--agentName`     | Agentforce Agent API Name                      | ✅        | `--agentName Salesforce_Copilot` |


> ⚠️ **Note:** The Agentforce Agent must be *activated* and accessible in your Salesforce org.

---


## 💡 Practical Example (Claude Desktop)

Below is a real example of the **Agentforce MCP server** working inside **Claude Desktop**, showing how Claude communicates with a Salesforce Agent via the MCP server:

> **User:** *"get account targets of Genepoint"*

The MCP server then sends this query to Salesforce, and the Agentforce Agent responds with structured insights:

> **Claude:**

```
The Copilot_for_Salesforce agent provided the following information about GenePoint’s account targets:

Account Targets for GenePoint:

1. Reduce delivery time by 30% through route optimization
   • Recommended action: Analyze current delivery routes and implement advanced routing software using real-time data.

2. Launch a new AI product line by the third quarter
   • Recommended action: Establish a clear timeline and allocate resources for timely development and launch.

These strategies focus on enhancing operational efficiency and market competitiveness for GenePoint.
```

This demonstrates how you can **query Salesforce data or agent-driven insights directly from your MCP client** without needing to log into Salesforce manually.

---

## 🧑‍💻 Author

**P. Mohit Harsh**
AI/ML Engineer •
🔗 [GitHub](https://github.com/Mohit-Harsh/AgentforceMCP)

---

## 🪪 License

MIT License © 2025 P. Mohit Harsh

---

