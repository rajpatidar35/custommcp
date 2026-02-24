# 🧩 Agentforce MCP Integration Server

This repository provides a unified solution for integrating **Model Context Protocol (MCP)** clients and **REST API** applications with **Agentforce Agents** using the **Agentforce Python SDK**.

It includes two core components:

1. **MCP Server** – Enables any MCP-compatible client to communicate directly with an Agentforce Agent.
2. **FastAPI Server** – Offers RESTful API endpoints for invoking the Agentforce Agent programmatically.

Both servers are built to ensure seamless connectivity, secure authentication, and consistent performance across integration channels.

---

## 📘 Overview

The repository implements two key servers designed for different modes of communication:

* **MCP Server**
  Enables MCP clients to connect to Agentforce Agents using the standardized Model Context Protocol. This allows real-time interaction and dynamic tool access through supported MCP clients and inspectors.

* **FastAPI Server**
  Provides RESTful access to Agentforce Agents, making it easy to integrate into existing systems or applications using simple HTTP requests.

Both implementations utilize the **Agentforce Python SDK** to communicate with Salesforce and the Agentforce backend, ensuring reliability and consistency.

---

## ⚙️ Setup Instructions

### 1. Repository Setup

Clone the repository and configure the required environment variables:

```bash
git clone [https://github.com/rajpatidar35/custommcp]
cd custommcp
```


> ⚠️ **Note:** Ensure these credentials correspond to a valid Salesforce user with Agentforce access.

---

### 2. Dependency Installation

Install all required Python dependencies using:

```bash
pip install -r requirements.txt
```

This will install all necessary libraries for both MCP and FastAPI servers, including the Agentforce Python SDK.

---

## 🚀 Running the Servers

### 🧠 Start MCP Server

To start the MCP server (used for MCP clients and inspectors):

```bash
python ./src/streamable-http/serverllm.py
```

The MCP server will initialize and listen for incoming MCP client connections.

---

### 🌐 Start FastAPI Server

To run the FastAPI server for REST API access:

```bash
fastapi dev ./src/fastapi/server.py
```

This launches a development instance of the FastAPI application, exposing REST endpoints that interact with Agentforce Agents.

---

## 🔍 Inspector Server (Optional)

To test and debug the MCP server using the **MCP Inspector** tool:

1. Start the Inspector server:

   ```bash
   npx @modelcontextprotocol/inspector
   ```
2. Open the Inspector web interface (default port: `http://localhost:5173` or as shown in the console).
3. Connect to your running MCP server using the host URL:

   ```
   https://localhost:8000/mcp
   ```
4. Navigate to the **Tools** tab to explore and test the available MCP tools.

---



