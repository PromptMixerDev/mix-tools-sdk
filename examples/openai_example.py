import asyncio
import json
from openai import OpenAI
from mix_tools_sdk import MixToolsClient


async def main():
    try:
        # Initialize clients
        client = OpenAI()
        
        async with MixToolsClient() as tools_client:
            # Get tools in OpenAI format
            tools_response = await tools_client.list_tools(format="openai")
            tools = tools_response["tools"]

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
                    # Parse tool arguments
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Execute tool with OpenAI format
                    tool_result = await tools_client.execute_tool(
                        tool_call.function.name,
                        tool_args,
                        format="openai",
                        tool_call_id=tool_call.id
                    )
                    messages.append(tool_result)  # Result already formatted for OpenAI

                # Get final response with tool result
                final_response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages
                )
                print(f"Final response: {final_response.choices[0].message.content}")

    except json.JSONDecodeError as e:
        print(f"Error parsing tool arguments: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
