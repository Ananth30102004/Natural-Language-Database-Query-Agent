# Natural Language Database Query Agent

An AI-powered database query agent that allows users to interact with relational databases using natural language instead of writing SQL queries manually.

Built using **Python, LangChain, Model Context Protocol (MCP), FastAPI, and SQLite**, the project demonstrates how LLM-powered agents can understand user questions, generate SQL queries, interact with databases through tools, and return structured results.

## Overview

Working with relational databases often requires users to understand SQL syntax, table structures, joins, and query conditions.

This project aims to simplify database interaction by allowing users to ask questions in plain English. The agent interprets the request, generates an appropriate SQL query, accesses database functionality through MCP tools, and returns the query results.

## Key Features

- **Natural Language to SQL:** Convert plain-English questions into SQL queries.
- **Agent Orchestration:** Use LangChain to manage the agent workflow.
- **MCP Integration:** Expose database operations through Model Context Protocol tools.
- **FastAPI Backend:** Provide HTTP endpoints for interacting with the agent.
- **SQLite Database:** Work with structured relational data.
- **Modular Architecture:** Separate API, agent messaging, and database tool functionality.

## Technology Stack

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Core application logic      |
| LangChain  | Agent orchestration         |
| MCP        | Database tool integration   |
| FastAPI    | Backend API                 |
| SQLite     | Relational database         |
| SQL        | Data retrieval and analysis |

## Architecture

```text
          User
           |
           v
   Natural Language Query
           |
           v
      FastAPI (api.py)
           |
           v
    LangChain Agent
           |
           v
      MCP Server
    (mcp_server.py)
           |
           v
     SQLite Database
       (erp_db.db)
           |
           v
      Query Results
           |
           v
       User Response
```

## Project Structure

```text
Natural-Language-Database-Query-Agent/
│
├── api.py             # FastAPI application
├── mcp_server.py      # MCP server and database tools
├── messages.py        # Agent messages and prompts
├── erp_db.db          # SQLite database
├── .env               # Environment configuration (not committed)
└── .gitignore         # Git exclusion rules
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ananth30102004/Natural-Language-Database-Query-Agent.git

cd Natural-Language-Database-Query-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

Install the Python packages required by the project:

```bash
pip install fastapi uvicorn langchain mcp
```

Install any additional model-provider or LangChain integration packages used in your implementation.

### 4. Configure environment variables

Create a `.env` file and add the environment variables required by your configured LLM provider.

Do not commit API keys or other credentials to GitHub.

### 5. Run the application

Start the MCP server:

```bash
python mcp_server.py
```

Start the FastAPI application in a separate terminal:

```bash
uvicorn api:app --reload
```

If your FastAPI application uses a different ASGI variable name, update the command accordingly.

Once running, access the API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Example Use Cases

Users can ask questions about their database in natural language, such as:

- Show the top five suppliers by total purchase order value.
- Find all pending purchase orders.
- Calculate the total procurement value.
- Identify suppliers with multiple purchase orders.
- Retrieve purchase order details for a particular supplier.

The agent translates the request into SQL and retrieves the corresponding database information.

## What This Project Demonstrates

- Building LLM-powered database agents.
- Connecting language models with external tools.
- Implementing MCP-based tool integration.
- Developing API-driven AI applications.
- Working with relational databases and SQL.
- Designing modular agent-based architectures.

## Future Improvements

- Add more advanced SQL validation and query safeguards.
- Improve handling of complex joins and ambiguous questions.
- Add query execution logging and monitoring.
- Implement database schema awareness.
- Add automated evaluation for SQL generation accuracy.
- Expand support for additional relational databases.

## Author

**Ananth Kumar**

B.Tech – Electronics and Communication Engineering

Interested in Agentic AI, LLM Applications, Enterprise Automation, and AI-powered systems.

[GitHub Profile](https://github.com/Ananth30102004)
