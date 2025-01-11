import asyncio
import logging
import os
from anthropic import Anthropic
from mix_tools_sdk import MixToolsClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize Mix Tools client
    mix_tools_api_key = os.getenv("MIXTOOLS_API_KEY", "your-mix-tools-api-key")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "your-anthropic-api-key")

    async with MixToolsClient(api_key=mix_tools_api_key) as tools_client:
        try:
            # Get tools in Anthropic format
            tools_response = await tools_client.list_tools(format="anthropic")
            tools = tools_response["tools"]  # Extract just the tools array
            
            logger.info("Available tools: %s", tools)

            # Initialize Anthropic client
            anthropic = Anthropic(api_key=anthropic_api_key)

            # Example conversation with tools
            messages = [
                {
                    "role": "user",
                    "content": "What's the weather like in San Francisco?"
                }
            ]

            # Create message with tools
            response = anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,  # Pass the tools we got from Mix Tools SDK
                messages=messages
            )

            logger.info("Claude's response: %s", response.content)

            # Handle tool usage
            for content_block in response.content:
                # Check if this is a tool use block
                if hasattr(content_block, 'type') and content_block.type == 'tool_use':
                    logger.info("Tool use detected - Name: %s, ID: %s, Args: %s",
                              content_block.name, content_block.id, content_block.input)

                    # Execute tool with Anthropic format
                    tool_result = await tools_client.execute_tool(
                        content_block.name,
                        content_block.input,
                        format="anthropic",
                        tool_call_id=content_block.id
                    )

                    logger.info("Tool execution result: %s", tool_result)

                    # Add Claude's response and tool result to conversation
                    messages.extend([
                        {
                            "role": "assistant",
                            "content": response.content
                        },
                        tool_result  # API returns result already formatted for Anthropic
                    ])

                    # Get final response from Claude with tool result
                    final_response = anthropic.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1024,
                        tools=tools,
                        messages=messages
                    )
                    logger.info("Claude's final response: %s", final_response.content)

        except Exception as e:
            logger.error("An error occurred: %s", str(e), exc_info=True)
            raise

if __name__ == "__main__":
    asyncio.run(main())
