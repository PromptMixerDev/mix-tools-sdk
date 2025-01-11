import os
from typing import Dict, Any, Optional, Literal, List, Union
import httpx

ToolFormat = Literal["default", "openai", "anthropic", "ollama"]


class MixToolsClient:
    """Client for interacting with Mix Tools API"""

    def __init__(self, base_url: str = "https://api.mix.tools", api_key: Optional[str] = None):
        """
        Initialize the client

        Args:
            base_url: Base URL of the Mix Tools API
            api_key: Optional API key for authentication. If not provided, will look for MIXTOOLS_API_KEY environment variable
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv("MIXTOOLS_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either through constructor or MIXTOOLS_API_KEY environment variable")
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def list_tools(
        self,
        format: Optional[ToolFormat] = None,
        tags: Optional[Union[str, List[str]]] = None,
        toolkit: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List available tools with optional filtering

        Args:
            format: Optional format to return tools in (default, openai, anthropic, ollama)
            tags: Optional tag or list of tags to filter tools by. Tools must have all specified tags.
            toolkit: Optional toolkit name to filter tools by

        Returns:
            Dict containing list of tools in specified format
        """
        params = {}
        if format:
            params["format"] = format
        if tags:
            # Convert single tag to list for consistent handling
            tag_list = [tags] if isinstance(tags, str) else tags
            params["tags"] = ",".join(tag_list)
        if toolkit:
            params["toolkit"] = toolkit
        response = await self.client.get(f"{self.base_url}/tools", params=params)
        response.raise_for_status()
        return response.json()

    async def execute_tool(
        self,
        tool_name: str,
        properties: Dict[str, Any],
        format: Optional[ToolFormat] = None,
        tool_call_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool with given properties

        Args:
            tool_name: Name of the tool to execute
            properties: Dictionary of property names and values
            format: Optional format to return result in (default, openai, anthropic, ollama)
            tool_call_id: Optional tool call ID for formats that require it

        Returns:
            Dict containing the tool execution result in specified format
        """
        params = {"api_key": self.api_key}
        if format:
            params["format"] = format
        if tool_call_id:
            params["tool_call_id"] = tool_call_id

        response = await self.client.post(
            f"{self.base_url}/tools/{tool_name}",
            params=params,
            json=properties
        )
        response.raise_for_status()
        return response.json()

    async def health_check(self) -> Dict[str, str]:
        """Check API health status"""
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
