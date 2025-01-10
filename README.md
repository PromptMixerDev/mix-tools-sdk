# Mix Tools SDK

A Python SDK for interacting with the Mix Tools API. This SDK provides a simple interface to list and execute tools in various formats including OpenAI, Anthropic, and Ollama.

## Installation

```bash
pip install mix-tools-sdk
```

Or with Poetry:

```bash
poetry add mix-tools-sdk
```

## Features

- Async-first design using `httpx`
- Support for multiple tool formats (default, OpenAI, Anthropic, Ollama)
- Context manager support for proper resource cleanup
- Comprehensive error handling
- Logging support

## Usage

```python
import asyncio
import logging
from mix_tools_sdk import MixToolsClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize client with custom base URL (optional)
    async with MixToolsClient(base_url="http://localhost:8000") as client:
        # Check API health
        health = await client.health_check()
        logger.info("API health status: %s", health["status"])

        # List tools in OpenAI format
        tools = await client.list_tools(format="openai")
        logger.info("Available tools: %s", tools)

        # Execute a tool
        result = await client.execute_tool(
            "text_transform",
            {
                "text": "hello world",
                "operation": "upper"
            }
        )
        logger.info("Tool execution result: %s", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### MixToolsClient

The main client class for interacting with the Mix Tools API.

#### Methods

- `async health_check() -> Dict[str, str]`
  - Check the API health status
  - Returns: `{"status": "healthy"}`

- `async list_tools(format: Optional[ToolFormat] = None) -> Dict[str, Any]`
  - List all available tools
  - Args:
    - `format`: Optional format to return tools in ("default", "openai", "anthropic", "ollama")
  - Returns: Dictionary containing list of tools in specified format

- `async execute_tool(tool_name: str, properties: Dict[str, Any]) -> Dict[str, Any]`
  - Execute a tool with given properties
  - Args:
    - `tool_name`: Name of the tool to execute
    - `properties`: Dictionary of property names and values
  - Returns: Dictionary containing the tool execution result

## Error Handling

The SDK uses `httpx.HTTPStatusError` for HTTP-related errors. All methods will raise appropriate exceptions when errors occur:

- 404: Tool not found
- 400: Invalid tool properties
- 500: Server error

Example error handling:

```python
from httpx import HTTPStatusError

async with MixToolsClient() as client:
    try:
        result = await client.execute_tool("nonexistent_tool", {})
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.error("Tool not found")
        else:
            logger.error("HTTP error occurred: %s", str(e))
```

## Development

1. Clone the repository
2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## License

MIT
