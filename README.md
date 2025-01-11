# Mix Tools SDK

A Python SDK for interacting with the Mix Tools API. This SDK provides a simple interface to list and execute tools in various formats including OpenAI, Anthropic, and Ollama.

Visit [mix.tools](https://mix.tools) for the main website and [api.mix.tools](https://api.mix.tools) for API documentation.

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
    async with MixToolsClient() as client:
        # Check API health
        health = await client.health_check()
        logger.info("API health status: %s", health["status"])

        # List tools with various filters
        # Get all search-related tools
        search_tools = await client.list_tools(tags="search")
        logger.info("Search tools: %s", search_tools)

        # Get academic search tools
        academic_tools = await client.list_tools(tags=["search", "academic"])
        logger.info("Academic search tools: %s", academic_tools)

        # Get all tools from the ArXiv toolkit
        arxiv_tools = await client.list_tools(toolkit="arxiv")
        logger.info("ArXiv toolkit tools: %s", arxiv_tools)

        # Combine filters with format
        openai_search_tools = await client.list_tools(
            format="openai",
            tags="search"
        )
        logger.info("OpenAI format search tools: %s", openai_search_tools)

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

- `async list_tools(format: Optional[ToolFormat] = None, tags: Optional[Union[str, List[str]]] = None, toolkit: Optional[str] = None) -> Dict[str, Any]`
  - List available tools with optional filtering
  - Args:
    - `format`: Optional format to return tools in ("default", "openai", "anthropic", "ollama")
    - `tags`: Optional tag or list of tags to filter tools by. Tools must have all specified tags.
    - `toolkit`: Optional toolkit name to filter tools by
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
