# Mix Tools SDK Examples

This directory contains examples demonstrating how to use the Mix Tools SDK with different LLM providers.

## Examples Overview

### 1. Basic Usage (`basic_usage.py`)
Demonstrates fundamental SDK operations:
- Health check
- Listing tools in different formats
- Basic tool execution

### 2. Anthropic Integration (`anthropic_example.py`)
Shows how to:
- Get tools formatted for Anthropic's Claude
- Pass tools to Claude API
- Handle tool responses correctly
- Execute tools with automatic result formatting

### 3. OpenAI Integration (`openai_example.py`)
Demonstrates:
- Getting tools formatted for OpenAI
- Using tools with GPT models
- Handling function calling
- Executing tools with automatic result formatting

## Prerequisites

```bash
pip install mix-tools-sdk anthropic openai
```

## Authentication

The SDK requires an API key for authentication. There are two ways to provide it:

1. **Environment Variable**
   ```bash
   export MIXTOOLS_API_KEY=your-api-key-here
   ```
   The SDK will automatically use the key from the `MIXTOOLS_API_KEY` environment variable.

2. **Constructor Parameter**
   ```python
   client = MixToolsClient(api_key="your-api-key-here")
   ```
   You can pass the API key directly when initializing the client.

Make sure you have the necessary API keys set up:
- `MIXTOOLS_API_KEY` for Mix Tools API authentication
- `OPENAI_API_KEY` for OpenAI examples
- `ANTHROPIC_API_KEY` for Anthropic examples

## Key Concepts

### 1. Tool Formats
The SDK supports different tool formats for both tool definitions and execution results:
```python
# Get tools in specific format
tools = await client.list_tools(format="anthropic")

# Execute tool with result in specific format
result = await client.execute_tool(
    tool_name="weather",
    properties={"city": "Boston"},
    format="anthropic",
    tool_call_id="call_123"
)
```

Supported formats:
- `default`: Raw tool format
- `anthropic`: Format compatible with Claude's tool use
- `openai`: Format compatible with OpenAI's function calling
- `ollama`: Format compatible with Ollama's tool use

### 2. Tool Execution Flow

1. **Get Available Tools**
   ```python
   async with MixToolsClient() as client:
       tools = await client.list_tools(format="desired_format")
   ```

2. **Pass Tools to LLM**
   ```python
   # For Anthropic
   response = client.messages.create(
       model="claude-3-sonnet-20240229",
       tools=tools["tools"],
       messages=[{"role": "user", "content": "your prompt"}]
   )

   # For OpenAI
   response = client.chat.completions.create(
       model="gpt-4-turbo-preview",
       tools=tools["tools"],
       messages=[{"role": "user", "content": "your prompt"}]
   )
   ```

3. **Handle Tool Calls and Execute Tools**
   ```python
   # For Anthropic
   if hasattr(content_block, 'type') and content_block.type == 'tool_use':
       result = await client.execute_tool(
           content_block.name,
           content_block.input,
           format="anthropic",
           tool_call_id=content_block.id
       )

   # For OpenAI
   if response.choices[0].message.tool_calls:
       tool_call = response.choices[0].message.tool_calls[0]
       result = await client.execute_tool(
           tool_call.function.name,
           json.loads(tool_call.function.arguments),
           format="openai",
           tool_call_id=tool_call.id
       )
   ```

The SDK automatically formats tool results according to each provider's requirements, so there's no need to manually format the responses.

### 3. Error Handling
Both examples include proper error handling for:
- Tool execution errors
- API communication errors
- Argument parsing errors (especially for OpenAI's JSON arguments)

## Best Practices

1. **Always Use Async Context Managers**
   ```python
   # Using environment variable
   async with MixToolsClient() as client:
       # Your code here

   # Or with explicit API key
   async with MixToolsClient(api_key="your-api-key-here") as client:
       # Your code here
   ```

2. **Use Format Parameters**
   - Specify format when listing tools to get provider-specific schemas
   - Use format and tool_call_id when executing tools for proper result formatting
   - Let the SDK handle provider-specific formatting requirements

3. **Maintain Conversation Context**
   - Keep track of the full conversation history
   - Include both tool calls and their results
   - Pass the complete context for follow-up responses

4. **Error Handling**
   - Implement try-catch blocks around tool execution
   - Validate tool arguments before execution
   - The SDK will format errors appropriately for each provider

## Running the Examples

Each example can be run directly:

```bash
python examples/basic_usage.py
python examples/anthropic_example.py
python examples/openai_example.py
```

Make sure you have the necessary API keys set up:
- `OPENAI_API_KEY` for OpenAI examples
- `ANTHROPIC_API_KEY` for Anthropic examples
