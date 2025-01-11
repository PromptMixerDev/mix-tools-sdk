import asyncio
from anthropic import AnthropicBedrock
from mix_tools_sdk import MixToolsClient

async def main():
    # Initialize Mix Tools client
    async with MixToolsClient(api_key="your-api-key-here") as tools_client:
        # Get tools in Anthropic format
        tools = await tools_client.list_tools(format="anthropic")
        tools = tools["tools"]  # Extract just the tools array

        print("Available tools:", tools)

        # Initialize Anthropic client
        anthropic_client = AnthropicBedrock(
            aws_access_key="YOUR_AWS_ACCESS_KEY",  # Replace with your AWS access key
            aws_secret_key="YOUR_AWS_SECRET_KEY",  # Replace with your AWS secret key
            aws_region="us-west-2",  # Replace with your AWS region
        )

        # Example conversation with tools
        messages = [
            {
                "role": "user",
                "content": "What's the weather like in Boston?"
            }
        ]

        # Create message with tools
        response = anthropic_client.messages.create(
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            max_tokens=1024,
            tools=tools,  # Pass the tools we got from Mix Tools SDK
            messages=messages
        )

        print(f"\n\n🤖 Claude's response: {response}")
        print(f"\n📝 Response content: {response.content}")

        # Handle tool usage
        for content_block in response.content:
            # Check if this is a tool use block
            if hasattr(content_block, 'type') and content_block.type == 'tool_use':
                print(f"\n🔧 Tool use detected:")
                print(f"   Name: {content_block.name}")
                print(f"   ID: {content_block.id}")
                print(f"   Args: {content_block.input}")

                # Execute tool with Anthropic format
                tool_result = await tools_client.execute_tool(
                    content_block.name,
                    content_block.input,
                    format="anthropic",
                    tool_call_id=content_block.id
                )

                print(f"\n🔧 Tool result: {tool_result}")

                # Add Claude's response and tool result to conversation
                messages.extend([
                    {
                        "role": "assistant",
                        "content": response.content
                    },
                    tool_result  # API returns result already formatted for Anthropic
                ])

                # Get final response from Claude with tool result
                final_response = anthropic_client.messages.create(
                    model="anthropic.claude-3-sonnet-20240229-v1:0",
                    max_tokens=1024,
                    tools=tools,
                    messages=messages
                )
                print(f"\n🤖 Claude's final response: {final_response.content}")


if __name__ == "__main__":
    asyncio.run(main())
