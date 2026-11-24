import os
import asyncio
import sys
from dataclasses import dataclass
from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from dotenv import load_dotenv
from google import genai
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient


SERVER_PATH = Path(__file__).parent / "mcp_server.py"

load_dotenv()

gem_api_key = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """You are a careful SQLite analyst.

Your job is to answer business questions using the ERP database.

Tool usage rules:
- Use list_tables to discover available database tables.
- Use describe_table to inspect table columns before writing SQL when necessary.
- Use run_select to execute SQL queries.
- Never assume table names or column names.
- Use only one SELECT query per tool call.
- Never execute INSERT, UPDATE, DELETE, ALTER, DROP, CREATE,
  REPLACE, or other database modification statements.
- Prefer explicit column names instead of SELECT *.
- Keep query results limited to 5 rows unless the user requests more.
- For aggregate questions, calculate totals directly in SQL.
- If SQL returns an error, inspect it and correct the query.
- If no records match, clearly state that no records were found.
- Never invent database values or claim results that the tools did not return.
- Base every factual answer on the retrieved database results.
- Explain the result clearly and concisely.
"""

async def Create_Agent():
    # 1. Connect to MCP server
        client = MultiServerMCPClient({
            "erp": {
                "command": sys.executable,
                "args": [str(SERVER_PATH)],
                "transport": "stdio",
            }
        })
    
        # 2. Retrieve MCP tools
        tools = await client.get_tools()
    
        # 3. Initialize Gemini
        model = init_chat_model(
            "gemini-3.5-flash-lite",
            model_provider="google_genai"
        )
    
        # 4. Create the LangChain agent
        agent = create_agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=tools,
        )

        return agent

async def ask_datapilot(agent,question: str):

     # 5. Execute the user's question
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        }
    )

    # 6. Extract the final answer
    final_content = result["messages"][-1].content

    if isinstance(final_content, str):
        answer = final_content

    elif isinstance(final_content, list):
        answer = "\n".join(
            block["text"]
            for block in final_content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    else:
        answer = str(final_content)

    return answer

async def main():

    agent = await Create_Agent()

    question = "Which Po_id has the highest total amount in the purchase_order table?"

    answer = await ask_datapilot(agent, question)

    print("\nDataPilot Answer:")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())