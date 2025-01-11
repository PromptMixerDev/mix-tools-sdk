import asyncio
import logging
import os
from mix_tools_sdk import MixToolsClient

# Example API key - in practice this would be securely stored
EXAMPLE_API_KEY = "your-api-key-here"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Method 1: Using environment variable
    os.environ["MIXTOOLS_API_KEY"] = EXAMPLE_API_KEY
    async with MixToolsClient() as client:
        logger.info("Using client with API key from environment variable")
        # ... rest of the code with first client

    # Method 2: Providing API key directly
    async with MixToolsClient(api_key=EXAMPLE_API_KEY) as client:
        logger.info("Using client with API key provided in constructor")
        try:
            # Check API health
            health = await client.health_check()
            logger.info("API health status: %s", health["status"])

            # List tools with different filters and formats
            logger.info("Fetching tools with various filters...")
            
            # List all tools
            tools = await client.list_tools()
            logger.debug("All tools: %s", tools)

            # Filter tools by tag
            search_tools = await client.list_tools(tags="search")
            logger.debug("Search tools: %s", search_tools)

            # Filter tools by multiple tags
            academic_search_tools = await client.list_tools(tags=["search", "academic"])
            logger.debug("Academic search tools: %s", academic_search_tools)

            # Filter tools by toolkit
            arxiv_tools = await client.list_tools(toolkit="arxiv")
            logger.debug("ArXiv toolkit tools: %s", arxiv_tools)

            # Combine filters with format
            openai_search_tools = await client.list_tools(
                format="openai",
                tags="search"
            )
            logger.debug("OpenAI format search tools: %s", openai_search_tools)

            # Example: Execute text transform tool
            logger.info("Executing text transform tool...")
            result = await client.execute_tool(
                "text_transform",
                {
                    "text": "hello world",
                    "operation": "upper"
                }
            )
            logger.info("Tool execution result: %s", result)

        except Exception as e:
            logger.error("An error occurred: %s", str(e), exc_info=True)
            raise

if __name__ == "__main__":
    asyncio.run(main())
