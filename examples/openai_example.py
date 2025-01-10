import asyncio
import json
from openai import OpenAI
from mix_tools_sdk import MixToolsClient

async def get_tools_for_openai():
    """Fetch tools formatted for OpenAI"""
    async with MixToolsClient() as client:
        # Get tools in OpenAI format
        tools = await client.list_tools(format="openai")
        return tools["tools"]

async def handle_tool_use(tool_name: str, tool_id: str, properties: dict):
    """Execute a tool and format the response for OpenAI"""
    async with MixToolsClient() as client:
        try:
            result = await client.execute_tool(tool_name, properties)
            return {
                "role": "tool",
                "tool_call_id": tool_id,
                "content": str(result)
            }
        except Exception as e:
            return {
                "role": "tool",
                "tool_call_id": tool_id,
                "content": f"Error: {str(e)}"
            }

async def main():
    try:
        # First, get the tools in OpenAI format
        tools = await get_tools_for_openai()
        
        # Initialize OpenAI client
        client = OpenAI()
        
        # Example conversation with tools
        messages = [
            {
                "role": "user",
                "content": "What's the weather like in San Francisco?"
            }
        ]
        
        # Create chat completion with tools
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls
        })
        
        # Handle tool calls
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                # Extract tool information
                tool_name = tool_call.function.name
                tool_id = tool_call.id
                # Safely parse JSON arguments
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    print(f"Error parsing tool arguments: {e}")
                    continue
                
                # Execute tool and get result
                tool_result = await handle_tool_use(tool_name, tool_id, tool_args)
                messages.append(tool_result)
                
                # Get final response with tool result
                final_response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages
                )
                print(f"GPT's final response: {final_response.choices[0].message.content}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
