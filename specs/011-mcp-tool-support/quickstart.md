# Quickstart: MCP and Tool Support

## Setting Up a Local Tool

1. Create a Python script in `backend/src/tools/weather.py`:
   ```python
   async def run(args: dict) -> dict:
       city = args.get("city")
       # Fetch weather...
       return {"temp": 22, "condition": "Sunny"}
   ```

2. Register the tool via API:
   ```bash
   curl -X POST http://localhost:8000/tools/local \
     -H "Content-Type: application/json" \
     -d '{
       "name": "get_weather",
       "description": "Get current weather for a city",
       "script_path": "weather.py"
     }'
   ```

## Setting Up an MCP Server

1. Register a standard MCP server (e.g., SQLite):
   ```bash
   curl -X POST http://localhost:8000/tools/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "server_name": "sqlite",
       "command": "python",
       "args": ["-m", "mcp_server_sqlite", "--db-path", "mydata.db"]
     }'
   ```

## Verifying Integration

1. List available tools: `GET /tools`
2. Run the agent and ask: "What is the weather in London?"
3. Check logs: `tail -f backend/logs/tools.log`
